#uruchamialem z python3
#
from pymongo import MongoClient
from pprint import pprint
import pymongo
import datetime
import json
import pymongo


mongoDBUrlLocalHost = "mongodb://127.0.0.1:27017"
client = MongoClient(mongoDBUrlLocalHost)
db = client["tfits"]
collection = db[ "tfits" ]


def insert_review(review):
    result = collection.insert(review)


def get_all_from_collection():
    return collection.find()


def get_match_from_collection(key,value):
    return collection.find({key : value})


def import_into_db(query, data_s):
    
    answer = input("IMPORT DATA FROM JSON INTO MONGODB? [y/n]:\t")
    if(answer.lower() == 'y'):

        try:
            answer2 = input("REMOVE PREVIOUS DATA FROM MONGODB? [y/n]:\t")
            if(answer2.lower() == 'y'):
                db.tfits.remove()
                 
        except Exception as e:
            print("you cannot remove items from a collection that does not exist!")
        
        # dla sprawdzenie czy zawartosc kolekcji w przypadku wybrania opcji usun zostala skasowana
        # for item in collection.find():
        #     print(item)

        # chce zapobiec sytuacji duplikowania tych samych id dlatego zamiast listy wybieram slownik
        #id TW jak klucz => tfits:{ TAG1 : { ID1 : {}, ID2 : {}, ...}, TAG2 ... }
        
        for item in data_s:
            result = {query:{}}
            key = str(item["id"])
            result[query] = {key:item}
            collection.insert_one(result)
    
    answer3 = input("display the entered data? [y/n]:\t")
    if(answer3.lower() == 'y'):
        for item in collection.find():
            print(item) 
    return

if __name__ == "__main__":

    with open("data/Biedron20202020-04-01-17-24-30.json") as data_file:
        data = json.load(data_file)

    import_into_db("Biedron2020", data)
    