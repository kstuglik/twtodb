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


"""Get user who posted tweet from users database."""
def get_titter_user(tweet):
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


"""Find tweets with hashtag."""
def find_tweets_with_hashtag(hashtag):
    regex = re.compile("^" + hashtag + "$", re.IGNORECASE)

    return collection.find({"tweet.entities.hashtags.text": regex})

