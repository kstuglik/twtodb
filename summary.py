from analize import *
from settings import *  #z pliku settings brane są nazwy-hashtagi
import inspect
import time
from datetime import datetime


def get_var_name(var):
    for fi in reversed(inspect.stack()):
        names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
        if len(names) > 0:
            return names[0]


def get_user_count_from_list(lista,user_id):
    for item in lista:
        if str(item["_id"]) == str(user_id):
            return item["count"]


def get_summary_user_tweets_number(top_n):

    lista1 = list(tweets_per_user())
    lista2 = list(all_tweets_per_user())
    lista3 = list(retweets_per_user())

    print("\n"+"UŻYTKOWNICY Z NAJWIEKSZA ILOSCIA ORYGINALNYCH TWEETOW".center(100,"=") + "\n")
    counter = top_n

    for item in lista1:
        if counter > 0 and item["count"] > 5:
            lista2_temp = get_user_count_from_list(lista2,item["_id"])
            lista3_temp = get_user_count_from_list(lista3,item["_id"])

            user = get_user_by_id(item["_id"])
            print(
                "".center(100,"*") + "\n" +
                user["user"]["name"] +"\n"+
                "orginal_tweets:\t" +    str(item["count"]).ljust(20, " ")+"\t"+
                "all_tweets:\t"     +   str(lista2_temp).ljust(20, " ")+"\t"+
                "how_often_retweeted:\t"    +   str(lista3_temp).ljust(20, " ")
            )
            counter -= 1


    print("\n"+"UŻYTKOWNICY NAJCZESCIEJ RETWEETOWANI".center(100,"=") + "\n")
    counter = top_n
    for item in lista3:
        if counter > 0 and item["count"] > 5:
            count_from_lista1 = get_user_count_from_list(lista1,item["_id"])
            count_from_lista2 = get_user_count_from_list(lista2,item["_id"])
            if count_from_lista2 > 4:
                user = get_user_by_id(item["_id"])
                print(
                    "".center(100,"*") + "\n" +
                    user["user"]["name"] +"\n"+
                    "how_often_retweeted:\t"+str(item["count"]).ljust(20, " ")+"\t"+
                    "all_tweets:\t"+str(count_from_lista2).ljust(20, " ")+"\t"+
                    "orginal_tweets:\t" +str(count_from_lista1).ljust(20, " ") +"\n"
                )

                counter -= 1


def get_summary_tweets_by_hashtags():
    dict_sum_htags = {}

    for htag in hashtags:
        if htag not in dict_sum_htags:
            dict_sum_htags[htag] = {}

        if htag == "Holownia2020":
            sprawdzam = list(find_tweets_with_hashtag("Holownia2020|Hołownia2020"))
        if htag == "Biedron2020":
            sprawdzam = list(find_tweets_with_hashtag("Biedron2020|Biedroń2020"))
        else:
            sprawdzam = list(find_tweets_with_hashtag(htag))

        temp_original = 0
        temp_retweet = 0

        for item in sprawdzam:
            if item["retweet"] == False:
                temp_retweet += 1
            else:
                temp_original += 1
        
        dict_sum_htags[htag]["all"] = temp_original + temp_retweet
        dict_sum_htags[htag]["original"] = temp_original
        dict_sum_htags[htag]["retweet"] = temp_retweet

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

        if htag == "Holownia2020":
            sprawdzam = list(find_tweets_with_hashtag("Holownia2020|Hołownia2020"))
        if htag == "Biedron2020":
            sprawdzam = list(find_tweets_with_hashtag("Biedron2020|Biedroń2020"))
        else:
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


def get_summary_advanced():

    print("\n"+"DETEILED SUMMARY".center(100,"="))

    summary = get_summary_tweets_by_hashtags()

    all_tweets      = 0
    all_originals   = 0
    all_retweeted   = 0

    for key,value in summary.items():
        all_tweets      +=  value["all"]
        all_originals   +=  value["original"]
        all_retweeted   +=  value["retweet"]     
       

    # PART 1
    print("\n"+"| ZESTAWIENIE GLOBALNE |".center(100,    "=") + "\n")
    print(
        "#hashtag".ljust(30,    " ")    +   "\t"    +
        "all".ljust(10,         " ")    +   "\t[%]".ljust(4, " ")   +   "\t"+
        "original".ljust(10,    " ")    +   "\t[%]".ljust(4, " ")   +   "\t"+
        "retweeted".ljust(10,   " ")    +   "\t[%]".ljust(4, " ")
    )

    for key, value in summary.items():
        print(
        key.ljust(30, " ")+"\t"+
        str(        value["all"]).ljust(10,         " ")    +"\t"+  
        str(round(  value["all"]/all_tweets*100,2))         +"\t"+
        str(        value["original"]).ljust(10," ")        +"\t"+  
        str(round(  value["original"] /all_originals*100,2))+"\t"+
        str(        value["retweet"]).ljust(10, " ")        +"\t"+  
        str(round(  value["retweet"]/all_retweeted*100,2))
        )

    print("\n"+"| ZESTAWIENIE LOKALNE |".center(100,    "=") + "\n")
    print(
        "#hashtag".ljust(30,    " ")    +   "\t"    +
        "all".ljust(10,         " ")    +   "\t"    +
        "original".ljust(10,    " ")    +   "\t[%]".ljust(4, " ")   +   "\t"+
        "retweeted".ljust(10,   " ")    +   "\t[%]".ljust(4, " ")
    )

    for key, value in summary.items():
        print(
        key.ljust(30, " ")+"\t"+
        str(        value["all"]).ljust(10,         " ")    +"\t"+  
        str(        value["original"]).ljust(10," ")        +"\t"+  
        str(round(  value["original"] /value["all"]*100,2))+"\t"+
        str(        value["retweet"]).ljust(10, " ")        +"\t"+  
        str(round(  value["retweet"]/value["all"]*100,2))
        )


def get_summary_basic():

    print("\n"+"BASIC SUMMARY".center(100,    "*") + "\n")

    all_tweet = count_all_tweets()
    all_origin_tweet = count_tweets()
    all_retweeted = all_tweet - all_origin_tweet
    
    print(
        "ALL TWEETS".ljust(10,          " ")    +   "\t"    +
        "ORIGINAL TWEETS".ljust(10,     " ")    +   "\t[%]".ljust(4, " ")   +   "\t"+
        "RETWEETED".ljust(10,           " ")    +   "\t[%]".ljust(4, " ")   +   "\n"+
        str(        all_tweet).ljust(10,         " ")   +   "\t"+  
        str(        all_origin_tweet).ljust(10," ")     +   "\t"+  
        str(round(  all_origin_tweet/all_tweet*100,2))  +   "\t"+
        str(        all_retweeted).ljust(10, " ")       +   "\t"+  
        str(round(  all_retweeted/all_tweet*100,2))
    )


if __name__ == "__main__":

    # get_summary_basic()
    # get_summary_advanced()

    get_summary_user_tweets_number(5)

    # pprint(get_summary_htags_by_day())
    # create_xls_summary_htags_by_day()

    #STANDARDOWE WYWOŁANIA
    # print(count_tweets())
    # print(get_user_by_id("2239021813"))
    # print(get_tweet_by_id("12590612384341975"))
    # print(get_which_retweet(tweet))
    # print(count_tweets())
    # print(count_all_tweets())


    # for t_user in tweets_per_user():
    #     print(t_user["_id"])

    # for t_user in all_tweets_per_user():
    #     print(t_user["_id"])

    # for rt_user in retweets_per_user():
    #     print(rt_user["_id"])

