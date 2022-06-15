from calendar import week
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

def set_note(id,key,value,weekday,time):
    add_sub = {"chat_id":id,"subject":key,"Description":value,"weekday":weekday,"time":time}
    description.insert_one(add_sub)




def delete_notification(chat_id,sub,descr,weekday):
    description.delete_many({"chat_id":chat_id,"subject":sub,"Description":descr,"weekday":weekday})

#set_note(1389812823,"1","1","Среда","8:00")
#delete_notification(1389812823,"1","1","Среда")
def get_all_conunt_documents():
    return description.estimated_document_count()
