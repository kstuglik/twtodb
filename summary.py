from analize import *
#z pliku settings brane są nazwy-hashtagi
from settings import *
import inspect
import time
from datetime import datetime


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


def get_user_by_id_from_list(lista,user_id):
    for item in lista:
        if str(item["_id"]) == str(user_id):
            return item["count"]


def get_summary_user_tweets_number(top_n):
    orginal_tweets = list(tweets_per_user())
    tweets_and_retweets = list(all_tweets_per_user())
    retweeted = list(retweets_per_user())

    # Nie wiem za bardzo czemu.. 
    # print(get_user_by_id_from_list(how_many_people_retweeted,"421399352"))

    get_user_summary(orginal_tweets,tweets_and_retweets,retweeted,top_n)
    get_user_summary(retweeted,orginal_tweets,tweets_and_retweets,top_n)
    get_user_summary(tweets_and_retweets,orginal_tweets,retweeted,top_n)


def get_user_summary(lista1,lista2,lista3,top_n):

    print("***************************************************************************************")
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


def get_summary_tweets_by_hashtags():
    dict_sum_htags = {}

    for tag in hashtags:
        if tag not in dict_sum_htags:
            dict_sum_htags[tag] = {}

        sprawdzam = list(find_tweets_with_hashtag(tag))

        temp_original = 0
        temp_retweet = 0

        for item in sprawdzam:
            if item['retweet'] == False:
                temp_retweet += 1
            else:
                temp_original += 1
        
        dict_sum_htags[tag]["all"] = temp_original + temp_retweet
        dict_sum_htags[tag]["original"] = temp_original
        dict_sum_htags[tag]["retweet"] = temp_retweet

    return dict_sum_htags


def prepare_data_format_from_tweet(tweet_data_format):
    time_struct = time.strptime(tweet_data_format, "%a %b %d %H:%M:%S +0000 %Y")

    date = datetime.fromtimestamp(time.mktime(time_struct))
    dataformat = str(date.year)+"-"+str(date.month).zfill(2)+"-"+str(date.day).zfill(2)

    return dataformat


def get_summary_htags_by_day():
    slownik_aktywnosci_dziennej = {}

    for htag in hashtags:
        print("get_summary_htags_by_day for: #"+str(htag))
        sprawdzam = list(find_tweets_with_hashtag(htag))
        for item in sprawdzam:
 
            dataformat = prepare_data_format_from_tweet(item["tweet"]["created_at"])
            if dataformat not in slownik_aktywnosci_dziennej:
                slownik_aktywnosci_dziennej[dataformat] = {}

            if htag not in slownik_aktywnosci_dziennej[dataformat]:
               slownik_aktywnosci_dziennej[dataformat][htag] = {"sum":0}

            slownik_aktywnosci_dziennej[dataformat][htag]["sum"] += 1

    return slownik_aktywnosci_dziennej


def create_xls_summary_htags_by_day():
    slownik = get_summary_htags_by_day()
    f = open("test.csv", "a")
    f.write("DATE;")
    for htag in hashtags:
        f.write(htag+";")
    f.write("\n")

    for key,value in slownik.items():
        if key > "2020-03-30":
            f.write(key+";")
            for htag in hashtags:
                if htag not in value:
                    f.write("0;")
                else:
                    f.write(str(value[htag]["sum"])+";")
                    
            f.write("\n")

    f.close()


def get_summary():
    print("TWEETS without RETWEETS:\t%d"%(count_tweets()))
    print("TWEETS with RETWEETS:\t%d"%(count_all_tweets()))

    summary = get_summary_tweets_by_hashtags()

    all_tw_rtw = 0

    for key,value in summary.items():
        all_tw_rtw += value["all"]


    print(
        "#hashtag".ljust(30, ' ')+"\t"+
        "all".ljust(10, ' ')+"\t"+
        "[%]".ljust(4, ' ')+"\t"+
        "original".ljust(10, ' ')+"\t"+
        "[%]".ljust(4, ' ')+"\t"+
        "retweeted".ljust(10, ' ')+"\t"+
        "[%]".ljust(4, ' ')
    )

    for key, value in summary.items():
        print(
        key.ljust(30, ' ')+"\t"+
        str(value["all"]).ljust(10, ' ')+"\t"+str(round(value["all"]/all_tw_rtw*100,2))+"\t"+
        str(value["original"]).ljust(10, ' ')+"\t"+str(round(value["original"]/value["all"]*100,2))+"\t"+
        str(value["retweet"]).ljust(10, ' ')+"\t"+str(round(value["retweet"]/value["all"]*100,2))
        )


if __name__ == "__main__":

    #WYWOLŁANIA DLA SUMMARY
    get_summary()
    get_summary_user_tweets_number(5)

    # pprint(get_summary_htags_by_day())
    # create_xls_summary_htags_by_day()

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

