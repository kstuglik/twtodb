#uruchamialem z python2
from time import gmtime
from datetime import datetime, timedelta
import sys
import json
from TwitterAPI import TwitterAPI

import re
import os

api = TwitterAPI("5l7mUZmFxS8VrSm1BqlkCGNJM",
                 "Q4XpEkK8sbnNF68ue4DRVXElfqHXWu15DBov9izNeOjQ55lRT7",
                 "1190551170076557312-dMYjta2WLhBmV5KEVd0PIbLvfUZAvN",
                 "ij1fjd72cd84Rn4gdJe2AYCj3Jj9ZRYDFu29JtRSLIwSz")


def prepare_request(query, since_id=None, max_id=None):
    req = dict()
    req['tweet_mode'] = 'extended'
    req['lang'] = 'pl'
    req['count'] = 100    # max number
    req['q'] = query

    if max_id is not None:
        req['max_id'] = max_id
    if since_id is not None:
        req['since_id'] = since_id

    return req


def get_tweets_from_api(query, since_id=None, max_id=None, h=None):
    tweets = []

    # if h specified then collect until tweet created at now - h hours
    if h is not None:
        n = datetime.now() - timedelta(hours=h)
        last = datetime.now()
    else:
        n = None
        last = None

    while h is None or last > n:
        print(str(n), ' ', str(last))
        request = prepare_request(query, since_id=since_id, max_id=max_id)
        try:
            response = api.request('search/tweets', request)
        except:
            # return collected tweets
            return tweets
        any_tweet = False
        for tweet in response:
            any_tweet = True
            tweets.append(tweet)
        
        if not any_tweet:
            # all tweets in requested range collected
            return tweets

        last = datetime.strptime(tweets[-1]['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        max_id = tweets[-1]['id'] - 1

    return tweets


def setNoneIfMinusOne(arg):
    if arg == "-1":
        return None
    else:
        return int(arg)


hashtags = [
    '#WyboryPrezydenckie2020',
    '#wyboryprezydenckie',
    '#Biedron2020',
    '#Bosak2020',
    '#Duda2020',
    '#Holownia2020',
    '#Kidawa2020',
    '#Kosiniakkamysz2020'
]


def update_last_first_id(new_content):
    try:
        prev_conent = {}

        if os.path.exists("last_first.json"):

            with open("last_first.json") as json_file:
                prev_conent = json.load(json_file)

            update_dict = {}

            for key, value in prev_conent.items():
                if key not in update_dict.keys():
                    update_dict[key] = {}
                update_dict[key] = value
            
            for key, value in new_content.items():
                if key not in update_dict.keys():
                    update_dict[key] = {}
                if key == "first_id" and new_content[key] > prev_conent[key]:
                    update_dict[key] = value
                if key == "last_id" and new_content[key] < prev_conent[key]:
                    update_dict[key] = value
            
            with open("last_first.json", 'w') as outfile:
                json.dump(update_dict, outfile, indent=4)

        else:
            with open("last_first.json", 'w') as outfile:
                json.dump(new_content, outfile) 

    except Exception as e:
        print("[update_save_last_first] Exception: %s"%e)


if __name__ == "__main__":
    if len(sys.argv) != 6 and len(sys.argv) != 1:
        print(
            "Usage:\n\n\t1)\tpython "+str(sys.argv[0])+" <start_id> <end_id> <time> <output_prefix> <query>\n"+
            "==>\t2)\tpython "+str(sys.argv[0])+"\n\n"+
            "\t<start_id>\t--\tfirst fetched tweet id\n"+
            "\t<end_id>\t--\tstop on fetching tweet id\n"+
            "\t<time>\t\t--\tstop on tweet created at now - time hours\n\n"+
            "-1 in fields: start_id, end_id, time is interpreted as None\n\n"+
            "TRY AGAIN"
        )
        sys.exit()

    # start_id = setNoneIfMinusOne(sys.argv[1])
    # end_id = setNoneIfMinusOne(sys.argv[2])
    # time = setNoneIfMinusOne(sys.argv[3])
    # output_prefix = sys.argv[4]
    # query = sys.argv[5]

    start_id = None
    end_id = None
    time = None

    # komunikat przekroczenia limitu wykonywanych zapytan w oknie 15min ma nr: 429
    # trzeba wprowadzic delay miedzy kolejnymi zapytaniami
    # trzeba dodac obsluge informacji z last_first.id dla danego tagu, by działo się to automatycznie

    for query in hashtags[]:

        output_prefix = str(query.replace("#",""))

        print(
            "Collect tweets from %s to %s, created not later then %s hours before\nSearch for: %s\nSave resaults to: %s" %(
                str(start_id),
                str(end_id),
                str(time),
                query,
                output_prefix
            )
        )

        tweets = get_tweets_from_api(query, since_id=end_id, max_id=start_id, h=time)

        remove_ms = lambda x:re.sub("\+\d+\s","",x)# Use re to get rid of the milliseconds.
        mk_dt = lambda x:datetime.strptime(remove_ms(x), "%a %b %d %H:%M:%S %Y")
        my_form = lambda x:"{:%Y-%m-%d-%H-%M-%S}".format(mk_dt(x))# Format datetime object.
        date_time = my_form(tweets[0]["created_at"])


        if len(tweets)>0:

            with open("data/"+output_prefix + date_time + ".json", 'w') as outfile:
                json.dump(tweets, outfile, indent = 4)
 
            content = {}
            content[query] = {"last_id": tweets[-1]['id'], "first_id": tweets[0]['id']}

            update_last_first_id(content)
