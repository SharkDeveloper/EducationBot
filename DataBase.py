from difflib import get_close_matches
from math import trunc
from aiohttp import client
import pymongo



client = pymongo.MongoClient("mongodb://Admin:12345687@telegrambot.qqtgh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.telegrambot

collection = db.BotUsers

def get(key):
    return collection.find_one(key)

def set(id,value):
    a=dict(value)   
    collection.update_one({"id":id},{"$set":a},True)

def set_note(id,key,value):
    collection.update_one({"id":id},{"$addToSet":{key:value}})

def creat_sub(id,key):
    collection.update_one({"id":id},{"$addToSet":{key:""}})

def create_doc(key):
    collection.insert_one({"id":str(key)})


