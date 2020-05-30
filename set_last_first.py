#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import sys
import json
from settings import *
from pprint import pprint 


def set_last_first_id():

    slownik = { "#"+i.lower() : {"first_id":0,"last_id":0} for i in hashtags }

    list_of_files = os.listdir("data")


    for file in list_of_files:

        temp = "#" + (file.split("2020-"))[0].lower()
        try:
            with open('data/'+file) as json_file:
                file_content = json.load(json_file)

            for item in file_content:

                if item["id"] > slownik[temp]["first_id"]:
                    slownik[temp]["first_id"] = item["id"]   
                    if slownik[temp]["last_id"] == 0:
                        slownik[temp]["last_id"] = item["id"]

                if item["id"] < slownik[temp]["last_id"]:
                    slownik[temp]["last_id"] = item["id"]

        except ValueError:
            print('Decoding JSON has failed for: %s'%file)

    pprint(slownik)

    with open("last_first2.json", 'w') as outfile:
        json.dump(slownik, outfile, indent=4, sort_keys=True)


if __name__ == "__main__":
    set_last_first_id()