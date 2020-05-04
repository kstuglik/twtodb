import os
import sys
import json
import time
from datetime import datetime


def create_json_with_YYYYMMDD_key():
    slownik_aktywnosci_dziennej = {}

    wszystkie_tweety_razem = {}

    path = "combine"
    lista_plikow_z_lokalizacji = [f for f in os.listdir(path) if f.endswith('.json')]

    # print(len(lista_plikow_z_lokalizacji))

    for file in lista_plikow_z_lokalizacji:
        print(path+"/"+file)

        try:
            with open(path+"/"+file) as json_file:
                C = json.load(json_file)
            for k,v in C.items():
                
                time_struct = time.strptime(v['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
                date = datetime.fromtimestamp(time.mktime(time_struct))
                dataformat = str(date.year)+"-"+str(date.month).zfill(2)+"-"+str(date.day).zfill(2)

                if dataformat not in slownik_aktywnosci_dziennej:
                    slownik_aktywnosci_dziennej[dataformat] = {}
                if v['id'] not in slownik_aktywnosci_dziennej[dataformat]:
                    slownik_aktywnosci_dziennej[dataformat][v['id']] = {}

                slownik_aktywnosci_dziennej[dataformat][v['id']] = v

        except ValueError:
            print('Decoding JSON has failed for: %s'%file)



    with open("_all_tw_by_yyyymmdd.json", 'w') as outfile:
        json.dump(slownik_aktywnosci_dziennej, outfile, indent=4, sort_keys=True)


    print(len(slownik_aktywnosci_dziennej))


def create_json_with_USERID_key():
    slownik_aktywnosci_dziennej = {}

    wszystkie_tweety_razem = {}

    path = "combine"
    lista_plikow_z_lokalizacji = [f for f in os.listdir(path) if f.endswith('.json')]

    # print(len(lista_plikow_z_lokalizacji))

    for file in lista_plikow_z_lokalizacji:
        print(path+"/"+file)

        try:
            with open(path+"/"+file) as json_file:
                C = json.load(json_file)

            for k,v in C.items():
                
                userid = v['user']['id']
                
                if userid not in slownik_aktywnosci_dziennej:
                    slownik_aktywnosci_dziennej[userid] = {}

                if v['id'] not in slownik_aktywnosci_dziennej[userid]:
                    slownik_aktywnosci_dziennej[userid][v['id']] = {}

                slownik_aktywnosci_dziennej[userid][v['id']] = v

        except ValueError:
            print('Decoding JSON has failed for: %s'%file)


    
    with open("_all_tw_by_user.json", 'w') as outfile:
        json.dump(slownik_aktywnosci_dziennej, outfile, indent=4, sort_keys=True)


    print(len(slownik_aktywnosci_dziennej))

create_json_with_USERID_key()