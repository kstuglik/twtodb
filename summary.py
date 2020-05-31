from analize import *
from settings import *  #z pliku settings brane są nazwy-hashtagi
import inspect
import time
from datetime import datetime
import operator
import matplotlib.pyplot as plt
import matplotlib
import argparse
import tqdm


def fix_hashtag_for_regex(h):
    if h == "Holownia2020":
        return "Holownia2020|Hołownia2020"
    elif h == "Biedron2020":
        return "Biedron2020|Biedroń2020"
    else:
        return h


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

        sprawdzam = list(find_tweets_with_hashtag(fix_hashtag_for_regex(htag)))

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

        sprawdzam = list(find_tweets_with_hashtag(fix_hashtag_for_regex(htag)))

        for item in sprawdzam:

            dataformat = prepare_data_format_from_tweet(item["tweet"]["created_at"])
            if dataformat not in slownik_aktywnosci_dziennej:
                slownik_aktywnosci_dziennej[dataformat] = {}

            if htag not in slownik_aktywnosci_dziennej[dataformat]:
                slownik_aktywnosci_dziennej[dataformat][htag] = {"sum":0}

            slownik_aktywnosci_dziennej[dataformat][htag]["sum"] += 1

    return slownik_aktywnosci_dziennej


def create_xls_summary_htags_by_day(output_file="output.csv"):
    slownik = get_summary_htags_by_day()
    f = open(output_file, "w")
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


def pair_hashtag_matrix():
    cross_arr = {}
    for h in hashtags:
        cross_arr[h] = {}
        print("Counting tweets with hashtag " + h)
        cross_arr[h][h] = find_tweets_with_hashtag(
                            fix_hashtag_for_regex(h), count=True)

    for i in range(len(hashtags)):
        h1 = hashtags[i]
        for h2 in hashtags[i+1:]:
            print("Counting tweets with hashtags " + h1 + " " + h2)
            c = find_tweets_with_multiple_hashtags(
                    [fix_hashtag_for_regex(h1),
                     fix_hashtag_for_regex(h2)],
                    count=True)
            cross_arr[h1][h2] = c
            cross_arr[h2][h1] = c

    return cross_arr


def plot_hashtag_matrix(pair_matrix, hashtags_list, percent=False,
                        logscale=True, out_file=None):
    hlen = len(hashtags_list)
    a = [[0] * hlen for i in range(hlen)]
    for h1, i, h2, j in ((h1, i, h2, j)
            for i, h1 in enumerate(hashtags_list)
            for j, h2 in enumerate(hashtags_list)):
        a[i][j] = pair_matrix[h1][h2]
    if percent:
        for i in range(hlen):
            for j in range(hlen):
                if j != i:
                    a[i][j] /= a[i][i] * 0.01
            a[i][i] = 100
        title = "Liczba tweetów z hashtagami XY / liczba tweetów z hashtagiem Y * 100%"
    else:
        title = "Liczba tweetów z hashtagami X i Y"

    fig = plt.figure(figsize=(10,10))
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    if logscale:
        res = ax.imshow(a, cmap=plt.cm.jet, interpolation='nearest',
                        norm =matplotlib.colors.LogNorm())
    else:
        res = ax.imshow(a, cmap=plt.cm.jet, interpolation='nearest')

    for x in range(hlen):
        for y in range(hlen):
            ax.annotate(str(round(a[x][y], 1)), xy=(y,x),
                    horizontalalignment='center',
                    verticalalignment='center')

    cb = fig.colorbar(res)
    plt.xticks(range(hlen), hashtags_list, rotation='vertical')
    plt.yticks(range(hlen), hashtags_list)
    plt.title(title)
    plt.xlabel("hashtag X")
    plt.ylabel("hashtag Y")
    plt.tight_layout()
    if out_file:
        #save to the file
        plt.savefig(out_file, format='png')
    else:
        #if there is no output file print plot to the screen
        plt.show()


"""This is only to print nicer help."""
class ArgumentDefaultsAndConstHelpFormatter(argparse.HelpFormatter):

    def _get_help_string(self, action):
        help = action.help
        if '%(default)' not in action.help:
            if action.default is not argparse.SUPPRESS:
                defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    help += ' (default: %(default)s)'
                if action.const and action.nargs:
                    help += ' (default if flag without arg: %(const)s)'
        return help


def user_uses_most_selected_tag():
    myDict = {}
    ul = user_list()

    for user_id in tqdm.cli.tqdm(ul, total=len(ul)):
        myDict[user_id] = {}
        l = get_tags_used_by_user(user_id)
        suma = {} 
        for group in l: 
            for h in group["_id"]: 
                h = h.lower() 
                if h in suma: 
                    suma[h] += group["count"] 
                else: 
                    suma[h] = group["count"] 
        myDict[user_id] = suma    
 
    result_tags = { i.lower() : {"user_id":0,"sum":0} for i in hashtags }

    for user_id,user_val in myDict.items():
        for key_tag, val_tag in user_val.items():
            for k in result_tags.keys():
                if key_tag.lower() == k:
                    if int(val_tag) > int(result_tags[k]["sum"]):
                        result_tags[k] = {"user_id":user_id,"sum":val_tag}

    pprint(result_tags)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
            description='Module for generating summary from tweets database.',
            formatter_class=ArgumentDefaultsAndConstHelpFormatter)

    parser.add_argument('-b', '--basic', action='store_true',
            help='Basic summary')
    parser.add_argument('-a', '--advanced', action='store_true',
            help='Advanced summary')
    parser.add_argument('-x', '--xls', nargs='?', const='test.csv',
            default=None, help='Generate number of tweets with hashtag per day in csv format')
    parser.add_argument('-u', '--users-tweets', nargs='?',
            const=10, default=None, type=int,
            help='Summary of most [users-tweets] active users')
    parser.add_argument('-d', '--htags-by-day', action='store_true',
            help='Print numer of tweets with hashtag per day')
    parser.add_argument('-m', '--matrix-count', nargs='?',
            const='../htag_matrix_count.png', default=None,
            help='Generate matrix plot of count of tweets with hashtags pairs. Results saved to file.')
    parser.add_argument('-p', '--matrix-percent', nargs='?',
            const='../htag_matrix_percent.png', default=None,
            help='Generate matrix plot of percent of tweets with hashtags pair compered to tweets of only one hashtag. Resault saved to file.')
    parser.add_argument('-c', '--matrix-candidats', nargs='?',
            const='../htag_matrix_percent_candidats.png', default=None,
            help='Generate matrix plot of percent of tweets with hashtags pair compered to tweets of only one hashtag. Only candidats hashtag is used (Duda2020, Bosak2020, etc.). Resault saved to file.')
    parser.add_argument('-i', '--interactive-matrix', action='store_true',
            help='Show generated plots in interactive mode.')
    parser.add_argument('-t', '--selected_tag', action='store_true',
            help='User with the most part of uses tag')

    args = parser.parse_args()

    if args.basic:
        get_summary_basic()
    if args.advanced:
        get_summary_advanced()
    
    if args.users_tweets:
        get_summary_user_tweets_number(args.users_tweets)

    if args.htags_by_day:
        pprint(get_summary_htags_by_day())
    if args.xls:
        create_xls_summary_htags_by_day(args.xls)
    
    if args.matrix_percent or args.matrix_count or args.matrix_candidats:
        # Create matrix of hashtags pairs
        cr_arr = pair_hashtag_matrix()
    if args.matrix_count:
        plot_hashtag_matrix(cr_arr, hashtags,
                            out_file=args.matrix_count)
    if args.matrix_percent:
        plot_hashtag_matrix(cr_arr, hashtags, percent=True,
                            out_file=args.matrix_percent)
    if args.matrix_candidats:
        # If hashtags list change, update this
        candidats = hashtags[2:9]
        plot_hashtag_matrix(cr_arr, candidats, percent=True,
                            out_file=args.matrix_candidats)
    if args.interactive_matrix:
        # show interactive plot
        plt.show()

    if args.selected_tag:
        user_uses_most_selected_tag()
   


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
    pass

