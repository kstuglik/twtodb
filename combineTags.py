#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import sys
import json

hashtags = [
    'WyboryPrezydenckie2020',
    'wyboryprezydenckie',
    'Biedron2020',
    'Bosak2020',
    'Duda2020',
    'Holownia2020',
    'Kidawa2020',
    'Kosiniak2020',
    'WyboryKorespondencyjne',
    'wybory2020'
]

slownik = { i : {} for i in hashtags }
lista = os.listdir("data")


for item in hashtags:
    C = {}
    for file in lista:
        if item in file:
            try:
                with open('data/'+file) as json_file:
                    C = json.load(json_file)
                for t in C:
                    slownik[item][t["id"]] = t
            except ValueError:
                print('Decoding JSON has failed for: %s'%file)

for key, value in slownik.items():
    with open("combine/_all_"+key+".json", 'w') as outfile:
        json.dump(value, outfile, indent=4, sort_keys=True)


nowy = {}
sum = 0

for key, value in slownik.items():
    prev = sum
    sum = 0
    for item in value:
        if item not in nowy:
            nowy[item] = 0
        nowy[item] += 1
    sum = len(nowy)
    razem = sum - prev
    print("#%s: %d tweetow"%(key,razem))

print("wszystkich tweetow jest: %d"%len(nowy))