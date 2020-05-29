from analize import *
from settings import *  #z pliku settings brane są nazwy-hashtagi
import inspect
import time
from datetime import datetime
import operator


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

    lista4 = [] # lista id najbardziej aktywnych użytkowników(z oryginalnymi tweetami)

    print("\n"+"UŻYTKOWNICY Z NAJWIEKSZA ILOSCIA ORYGINALNYCH TWEETOW".center(100,"=") + "\n")
    counter = top_n

    print(
        ("user_name").ljust(40, " ")+
        ("orginal_tweets: ").ljust(20, " ")+
        ("all_tweets:").ljust(20, " ")+
        ("how_often_retweeted:").ljust(20, " ")+"\n"
    )

    for item in lista1:
        if counter > 0 and item["count"] > 5:
            lista2_temp = get_user_count_from_list(lista2,item["_id"])
            lista3_temp = get_user_count_from_list(lista3,item["_id"])

            user = get_user_by_id(item["_id"])
            print(
                (user["user"]["name"]).ljust(40, " ")+
                str(item["count"]).ljust(20, " ")+"\t"+
                str(lista2_temp).ljust(20, " ")+"\t"+
                str(lista3_temp).ljust(20, " ")
            )
            counter -= 1
            lista4.append(item["_id"])


    print("\n"+"UŻYTKOWNICY NAJCZESCIEJ RETWEETOWANI".center(110,"=") + "\n")
    counter = top_n

    print(
        ("user_name").ljust(40, " ")+
        ("how_often_retweeted:").ljust(30, " ")+
        ("all_tweets:").ljust(20, " ")+
        ("orginal_tweets: ").ljust(20, " ")+"\n"
    )

    for item in lista3:
        if counter > 0 and item["count"] > 5:
            count_from_lista1 = get_user_count_from_list(lista1,item["_id"])
            count_from_lista2 = get_user_count_from_list(lista2,item["_id"])
            if count_from_lista2 > 4:
                user = get_user_by_id(item["_id"])
                print(
                    (user["user"]["name"]).ljust(40, " ")+
                    str(item["count"]).ljust(30, " ")+"\t"+
                    str(count_from_lista2).ljust(20, " ")+"\t"+
                    str(count_from_lista1).ljust(20, " ")
                )

                counter -= 1


    d = {} 

    print("\n"+"UŻYTKOWNICY NAJCZESCIEJ RETWEETOWANI - SZCZEGÓŁY".center(140,"=") + "\n")
    print(
        ("user_name").ljust(40, " ")+
        ("followers_count: ").ljust(20, " ")+
        ("friends_count:").ljust(20, " ")+
        ("listed_count:").ljust(20, " ")+
        ("favourites_count:").ljust(20, " ")+
        ("statuses_count:").ljust(20, " ")+ "\n"
    )
    for user_id in lista4:

        item = get_user_by_id(user_id)
        d[user_id] = {"name":item["user"]["name"],"suma":0}

        print(
            item["user"]["name"].ljust(40, " ")+
            str(item["user"]["followers_count"]).ljust(20, " ")+
            str(item["user"]["friends_count"]).ljust(20, " ")+
            str(item["user"]["listed_count"]).ljust(20, " ")+
            str(item["user"]["favourites_count"]).ljust(20, " ")+
            str(item["user"]["statuses_count"]).ljust(20, " ")
        )

        l = get_tags_used_by_user(user_id)
        suma = {} 
        for group in l: 
            for h in group["_id"]: 
                h = h.lower() 
                if h in suma: 
                    suma[h] += group["count"] 
                else: 
                    suma[h] = group["count"] 
        d[user_id]["suma"] = suma                                                                                                                             

    
    i = 1
    for k,v in d.items():
        print(str(i)+") "+(v["name"]).center(50, "*"))
        pprint(sorted(v["suma"].items(), key=operator.itemgetter(-1),reverse=True)[0:10])
        i += 1
        

def get_summary_tweets_by_hashtags():
    dict_sum_htags = {}

    for htag in hashtags:
        if htag not in dict_sum_htags:
            dict_sum_htags[htag] = {}

        if htag == "Holownia2020":
            sprawdzam = list(find_tweets_with_hashtag("Holownia2020|Hołownia2020"))
        elif htag == "Biedron2020":
            sprawdzam = list(find_tweets_with_hashtag("Biedron2020|Biedroń2020"))
        else:
            sprawdzam = list(find_tweets_with_hashtag(htag))

        temp_original = 0
        temp_retweet = 0

        for item in sprawdzam:
            if item["retweet"]:
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
        elif htag == "Biedron2020":
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

    for key,value in sorted(slownik.items()):
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

    print("ALL USERS: "+str(get_all_users_count()))
    print("ALL TWEETS: "+ str(get_all_tweets_count()))


if __name__ == "__main__":

    get_summary_basic()
    get_summary_advanced()

    get_summary_user_tweets_number(10)

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

