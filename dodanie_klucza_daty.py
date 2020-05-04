import os
import sys
import json
import time
from datetime import datetime

slownik_aktywnosci_dziennej = {}

wszystkie_tweety_razem = {}

path = "combine"
lista_plikow_z_lokalizacji = [f for f in os.listdir(path) if f.endswith('.json')]

# print(len(lista_plikow_z_lokalizacji))

for file in lista_plikow_z_lokalizacji:
    print(path+"/"+file)
    slownik_aktywnosci_dziennej.clear()
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



    with open("_dane"+file+".json", 'w') as outfile:
        json.dump(slownik_aktywnosci_dziennej, outfile, indent=4, sort_keys=True)


    print(len(slownik_aktywnosci_dziennej))

