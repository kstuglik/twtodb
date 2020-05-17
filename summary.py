from analize import *
#z pliku settings brane są nazwy-hashtagi
from settings import *
import inspect


def get_var_name(var):
        """
        Gets the name of var. Does it from the out most frame inner-wards.
        :param var: variable to get name from.
        :return: string
        """
        for fi in reversed(inspect.stack()):
            names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
            if len(names) > 0:
                return names[0]


def get_summary_hashtag_number():
    print("**********ALL_TWEETS_WITH_HASHTAG*************")
    all_items = 0
    for item in hashtags:
        ile = 0
        ile = len(list(find_tweets_with_hashtag(item)))
        all_items += ile
        print(
            item.ljust(20, ' ')+"\t"+
            str(ile).ljust(20, ' ')
        ))


def get_user_by_id_from_list(lista,user_id):
    for item in lista:
        if str(item["_id"]) == str(user_id):
            return item["count"]


def get_summary_user_tweets_number(top_n):
    orginal_tweets = list(tweets_per_user())
    tweets_and_retweets = list(all_tweets_per_user())
    how_many_times_user_was_retweeted = list(retweets_per_user())

    # Nie wiem za bardzo czemu.. 
    # print(get_user_by_id_from_list(how_many_people_retweeted,"421399352"))

    get_user_summary(orginal_tweets,tweets_and_retweets,how_many_times_user_was_retweeted,top_n)
    get_user_summary(how_many_times_user_was_retweeted,orginal_tweets,tweets_and_retweets,top_n)
    get_user_summary(tweets_and_retweets,orginal_tweets,how_many_times_user_was_retweeted,top_n)


def get_user_summary(lista1,lista2,lista3,top_n):

    print("**************************************")
    print(
        "USER_ID".ljust(20, ' ')+"\t"+
        get_var_name(lista1).ljust(20, ' ')+"\t"+
        get_var_name(lista2).ljust(20, ' ')+"\t"+
        get_var_name(lista3).ljust(20, ' ')
    )

    for item in lista1[:top_n]:
        lista2_temp = get_user_by_id_from_list(lista2,item["_id"])
        lista3_temp = get_user_by_id_from_list(lista3,item["_id"])
        print(
            str(item["_id"]).ljust(20, ' ')+"\t"+
            str(item["count"]).ljust(20, ' ')+"\t"+
            str(lista2_temp).ljust(20, ' ')+"\t"+
            str(lista3_temp).ljust(20, ' ')
        )


def get_summary_all_tweets():
    print("TWEETS without RETWEETS:\t%d"%(count_tweets()))
    print("TWEETS with RETWEETS:\t%d"%(count_all_tweets()))


if __name__ == "__main__":

    #WYWOLŁANIA DLA SUMMARY
    get_summary_hashtag_number()
    get_summary_user_tweets_number(5)
    get_summary_all_tweets()

    #STANDARDOWE WYWOŁANIA
    # print(count_tweets())
    # print(get_user_by_id(id_user))
    # print(get_tweet_by_id(id_tweet))
    # print(get_titter_user(tweet))
    # print(get_which_retweet(tweet))
    # print(count_tweets())
    # print(count_all_tweets())


    # for t_user in tweets_per_user():
    #     print(t_user["_id"])

    # for t_user in all_tweets_per_user():
    #     print(t_user["_id"])

    # for rt_user in retweets_per_user():
    #     print(rt_user["_id"])

