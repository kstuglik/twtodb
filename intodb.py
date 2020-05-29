#execute: 
#   python3 intodb.py append data/*
#               or
#   python3 intodb.py "append+folder" data

from pymongo import MongoClient
from pprint import pprint
import pymongo
import datetime
import json
import pymongo
import sys
import os

mongoDBUrlLocalHost = "mongodb://127.0.0.1:27017"
client = MongoClient(mongoDBUrlLocalHost)
db = client["tfits"]
collection = db[ "tfits" ]
users = db[ "users" ]


def insert_review(review):
    result = collection.insert(review)


def get_all_from_collection():
    return collection.find()


def get_match_from_collection(key,value):
    return collection.find({key : value})


def add_tweet(item, retweeted_me):
    if "retweeted_status" in item:
        retweet = item["retweeted_status"].copy()
    else:
        retweet = None
    
    hashtags = {}
    # Add hashtags in tweet
    for h in item["entities"]["hashtags"]:
        # Make hashtags lowercase
        hashtags[h["text"].lower()] = 1

    if retweet:
        # Add hashtags from orginal tweet
        for h in retweet["entities"]["hashtags"]:
            # Make hashtags lowercase
            hashtags[h["text"].lower()] = 1

    result = {"_id": item["id"],
            "tweet":item,
            "retweet": True if retweet else False,
            "hashtags": list(hashtags)}
    user = item["user"].copy()
    # leave only user id
    result["tweet"]["user"] = user["id"]
    if retweet:
        result["tweet"]["retweeted_status"] = retweet["id"]
    # if this is retweet, it may have quote status but not quoted_status field
    if item["is_quote_status"] and "quoted_status" in item:
        # there is already field quoted_status_id
        quoted = item["quoted_status"].copy() 
        result["tweet"]["quoted_status"] = None
    else:
        quoted = None

    # Add tweet to db
    try:
        exist = collection.find({"_id": item["id"]}).next()
        exist = exist["tweet"]
        update = {"$set": {}}
        # Update these fields, if current tweet or my retweet
        # has greater value
        fields = ["favorite_count", "retweet_count"]
        for f in fields:
            if item[f] > exist[f] or retweeted_me[f] > exist[f]:
                if item[f] > retweeted_me[f]:
                    update["$set"][f] = item[f]
                else:
                    update["$set"][f] = retweeted_me[f]
        if len(update["$set"]) > 0:
            collection.update({"_id": item["id"]}, update)

    except StopIteration as e:
        # if tweet doesn't exist add it
        collection.insert_one(result)

    # Add information about user to db
    try:
        exist = users.find({"_id": user["id"]}).next()
        exist = exist["user"]
        update = {"$set": {}}
        # Update these fields, if user in tweet has higher value
        fields = ["followers_count", "friends_count",
                 "favourites_count", "statuses_count"]
        for f in fields:
            if user[f] > exist[f]:
                update["$set"][f] = user[f]
        if len(update["$set"]) > 0:
            users.update({"_id": user["id"]}, update)
    except StopIteration as e:
        # if user doesn't exist insert it
        users.insert_one({"_id": user["id"], "user": user})

    # if this is retweet add it
    if retweet:
        add_tweet(retweet, item)
    # if it is qoute of another tweet, add quoted
    if quoted:
        add_tweet(quoted, quoted)


def import_into_db(append, data_s):
    
    if append:
        answer = 'y'
    else:
        answer = input("IMPORT DATA FROM JSON INTO MONGODB? [y/n]:\t")
    if(answer.lower() == 'y'):

        try:
            if append:
                answer2 = 'n'
            else:
                answer2 = input("REMOVE PREVIOUS DATA FROM MONGODB? [y/n]:\t")
            if(answer2.lower() == 'y'):
                db.tfits.remove()
                 
        except Exception as e:
            print("you cannot remove items from a collection that does not exist!")
        
        
        for item in data_s:
            # pass as self retweeted, it simplyfies add_tweet
            add_tweet(item, item)
            # because of structure of _all_* files (combinedTags.py)
            # it is necessary to use this code:
            # add_tweet(data_s[item], data_s[item])
            
    if append:
        answer3 = 'n'
    else:
        answer3 = input("display the entered data? [y/n]:\t")
    if(answer3.lower() == 'y'):
        for item in collection.find():
            print(item) 
    return

if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print ("Usage:", sys.argv[0], " [append] file ...")
        print ("append -- with this argument add tweets, not print theme, skip duplicates.")
        exit()

    append = False
    files = sys.argv[1:]
    if sys.argv[1] == "append":
        append = True
        files = sys.argv[2:]

    if sys.argv[1] == "append+folder":
        append = True
        folder = sys.argv[2]
        files = os.listdir(folder)
        files = [folder + "/" + f for f in files] 

    for f in files:
        try:
            print("Load tweets from: ", f)
            with open(f) as data_file:
                data = json.load(data_file)
            import_into_db(append, data)

        except Exception as e:
            print("["+f+"] Exception: %s"%e)

