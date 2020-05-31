# These are some useful queries into our mongo twitter db
# use "%load analize.py" in ipython for interactive use of these functions

from pymongo import MongoClient
from pprint import pprint
import pymongo
import datetime
import json
import pymongo
import sys
import re

mongoDBUrlLocalHost = "mongodb://127.0.0.1:27017"
client = MongoClient(mongoDBUrlLocalHost)
db = client["tfits"]
collection = db[ "tfits" ]
users = db[ "users" ]


# SEARCH BY: user_id, tweet_id, hashtag

"""Get user by id."""
def get_user_by_id(id_num):
    try:
        return users.find({"_id": id_num}).next()
    except StopIteration as e:
        return None


"""Get tweet by id."""
def get_tweet_by_id(id_num):
    try:
        return collection.find({"_id": id_num}).next()
    except StopIteration as e:
        return None


"""Find tweets with hashtag."""
def find_tweets_with_hashtag(hashtag, count=False):
    regex = re.compile("^" + hashtag + "$", re.IGNORECASE)

    q = {"hashtags": regex}

    if count:
        return collection.count_documents(q)

    return collection.find(q)


"""Find tweets containing multiple hashtags from list."""
def find_tweets_with_multiple_hashtags(hashtags_list, count=False):
    regex_list = []
    for h in hashtags_list:
        regex = re.compile("^" + h + "$", re.IGNORECASE)
        regex_list.append(regex)

    q = {"hashtags": {"$all": regex_list}}

    if count:
        return collection.count_documents(q)

    return collection.find(q)

# SEARCH IN TWEETS: author, if retweeted, number of tweets, number of tweets+retweets

"""Get user who posted tweet from users database."""
def get_twitter_user(tweet):
    return get_user_by_id(tweet["tweet"]["user"])


"""Get tweet from retweeted_status."""
def get_which_retweet(tweet):
    # This tweet is not retweet
    if not tweet["retweet"]:
        return None

    return get_tweet_by_id(tweet["tweet"]["retweeted_status"])


"""Count only tweets (without retweets)."""
def count_tweets():
     return collection.aggregate([{"$match": {"retweet": False}},
                                  {"$group": { "_id": None, "count": {"$sum":1}}}
                                 ]).next()["count"]


"""Count all tweets (include retweets)."""
def count_all_tweets():
     return collection.aggregate([{"$group": { "_id": None, "count": {"$sum":1}}}
                                 ]).next()["count"]


# USER-associated TWEETS: without retweets, with retweets, tweets+retweets

"""Orginal tweets per user (exclude retweets)."""
def tweets_per_user():
    return collection.aggregate([{"$match": {"retweet": False}},
                                 {"$group": { "_id": "$tweet.user",
                                              "count": {"$sum":1}}},
                                 {"$sort":{"count": -1}}
                                ])


"""All tweets per user (include retweets)."""
def all_tweets_per_user():
    return collection.aggregate([{"$group": { "_id": "$tweet.user",
                                              "count": {"$sum":1}}},
                                 {"$sort":{"count": -1}}
                                ])


"""Count number of retweets per user (how many times user was retweeted)."""
def retweets_per_user():
    return collection.aggregate([{"$match": {"retweet": False}},
                                 {"$group": { "_id": "$tweet.user",
                                              "count": {"$sum":"$tweet.retweet_count"}}},
                                 {"$sort":{"count": -1}}
                                ])

""" GET TAGS USED BY USER WITH USER_ID"""
def get_tags_used_by_user(user_id):
    return collection.aggregate([{"$match": {"tweet.user": user_id, "retweet": False}}, 
                                {"$group": { "_id": "$hashtags", 
                                        "count": {"$sum":1}}},
                                        {"$sort":{"count": -1}} 
                                ])


def get_all_users_count():
    d = users.aggregate([{"$group": {"_id": None, "count": {"$sum":1}}}]).next()
    return d["count"]


def get_all_tweets_count():
    d = collection.aggregate([{"$group": {"_id": None, "count": {"$sum":1}}}]).next()
    return d["count"]


def tweets_per_user_count_only_if_hashtag(hashtag):
    regex = re.compile("^" + hashtag + "$", re.IGNORECASE)
    return collection.aggregate([{"$match": {"retweet": False, "hashtags": regex}},
                                 {"$group": { "_id": "$tweet.user",
                                              "count": {"$sum":1}}},
                                 {"$sort":{"count": -1}}
                                ])


def get_user_id_from_name(screen_name):
    mydict = users.find()
    return [v["user"]["id"] for v in mydict if v["user"]["screen_name"]==screen_name]
