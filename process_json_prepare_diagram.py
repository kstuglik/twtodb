import os
import sys
import json
import time
from datetime import datetime
from operator import itemgetter 
from collections import OrderedDict           


def convert_js_to_xls_all_multiple_tags():
    path_to_file = "_all_tw.json"

    try:
        with open(path_to_file) as json_file:
            slownik_tw = json.load(json_file)

    except ValueError:
        print('Decoding JSON has failed for: %s'%file)

    with open("_dane_do_wykresu_1.xls", 'w') as outfile:
        outfile.write("DATE;TWEETS")
        for k,v in slownik_tw.items():
            outfile.write("%s;%d\n"%(k,len(v)))


def convert_js_to_xls_single_tags():
    
    lista_plikow_z_lokalizacji = os.listdir("_dane_all")

    for file in lista_plikow_z_lokalizacji:
        path_to_file = "_dane_all/"+file
        try:
            with open(path_to_file) as json_file:
                slownik_tw = json.load(json_file)

        except ValueError:
            print('Decoding JSON has failed for: %s'%file)

        with open("_dane_do_wykresu_"+file+".xls", 'w') as outfile:
            outfile.write("DATE;TWEETS;\n")
            for k,v in slownik_tw.items():
                outfile.write("%s;%d;\n"%(k,len(v)))


def check_result_for_day():
    with open("_dane_all/_dane_all_Duda2020.json.json") as json_file:
        slownik_tw = json.load(json_file)

        print(len(slownik_tw['2020-05-01']))


def check_acticity_users():
    path_to_file = "_all_tw_by_user.json"

    try:
        with open(path_to_file) as json_file:
            slownik_tw = json.load(json_file)
        print(len(slownik_tw))
            slownik = {}

            for k, v in slownik_tw.items():
                slownik[k] = len(v)

            N = 200
            res = dict(sorted(slownik.items(), key = itemgetter(1), reverse = True)[:N]) 
            
            # printing result 
            print("The top N value pairs are  " + str(res))

            with open("top"+str(N)+".json", 'w') as outfile:
                json.dump(res, outfile, indent=4)

    except ValueError:
        print('Decoding JSON has failed for: %s'%file)



def check_tags():
    top_n_file = "top200.json"
    N = 10

    slownik_wynikowy = {}

    try:
        slownik= {}

        with open(top_n_file) as json_file:
            slownik_top_N = json.load(json_file)

        users_id_list = list(slownik_top_N.keys())
        users_id_list = users_id_list[0:N]

        for user_id in users_id_list:
            slownik_wynikowy[user_id] = {"#":{}}

        all_tw_by_user_file = "_all_tw_by_user.json"

        with open(all_tw_by_user_file) as json_file:
            all_tw_by_user_dict = json.load(json_file)
            
        for user_id in users_id_list[0:N]:
            temp = {}
            for k,v in all_tw_by_user_dict[user_id].items():
                if len(v["entities"]["hashtags"]):
                    for item in  v["entities"]["hashtags"]:
                        hasht = item["text"]
                        if hasht not in slownik_wynikowy[user_id]["#"]:
                            slownik_wynikowy[user_id]["#"][hasht] = 0
                        slownik_wynikowy[user_id]["#"][hasht] += 1    

            # slownik_wynikowy[user_id]["#"] = sorted(slownik_wynikowy[user_id]["#"].items(), key = lambda kv:(kv[1],kv[0]), reverse=True)
        
        for k,v in slownik_wynikowy.items():
            sort_orders = OrderedDict(sorted(v["#"].items(), key=lambda x:x[1], reverse=True))
            
            with open("hashtags_in_use_by_"+k+".json", 'w') as outfile:
                json.dump(sort_orders, outfile,indent=1, ensure_ascii=False)

        


    except ValueError:
        print('Decoding JSON has failed for: %s'%file)


# check_tags()