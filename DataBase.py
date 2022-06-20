import calendar 
from aiohttp import client
import pymongo



client = pymongo.MongoClient("mongodb+srv://Admin:12345687@telegrambot.qqtgh.mongodb.net/?retryWrites=true&w=majority")
db = client.telegrambot

collection = db.BotUsers

def set(id,value):
    a=dict(value)   
    collection.update_one({"id":id},{"$set":a},True)



description = db.Description

def get(key):
    return description.find_one(key)
def get_many(key):
    return description.find(key)


def set_note(id,key,value,weekday,time):
    add_sub = {"chat_id":id,"subject":key,"Description":value,"weekday":weekday,"time":time}
    description.insert_one(add_sub)




def delete_notification(data):
    description.delete_many(data)

