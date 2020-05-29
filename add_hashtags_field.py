from analize import *
# For nice progress bar
import tqdm

if __name__ == "__main__":
    # Find tweets and retweets without hashtags field
    to_update = collection.find({"hashtags": {"$exists": False}})
    to_update_count = collection.count_documents(
                            {"hashtags": {"$exists": False}})

    # loop over tweets, do tweet in to_update: if you don't want bar
    for tweet in tqdm.cli.tqdm(to_update, total=to_update_count):
        hashtags = {}
        # Add hashtags in tweet
        for h in tweet["tweet"]["entities"]["hashtags"]:
            # Make hashtags lowercase
            hashtags[h["text"].lower()] = 1

        # if it is retweet get orginal tweet
        if tweet["retweet"]:
            org_tweet = get_tweet_by_id(
                                    tweet["tweet"]["retweeted_status"])
            # Add hashtags from orginal tweet
            for h in org_tweet["tweet"]["entities"]["hashtags"]:
                hashtags[h["text"].lower()] = 1

        # Add hashtags field
        collection.update({"_id": tweet["_id"]},
                          {"$set": {"hashtags": list(hashtags)}})

