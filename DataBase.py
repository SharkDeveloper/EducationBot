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

def set_note(id,key,value,weekday,time):
    """if weekday == "Понедельник":
        weekday = calendar.day_name[0]
        
    elif weekday == "Вторник":
        weekday = calendar.day_name[1]
        
    elif "Среда" in weekday:
        weekday = calendar.day_name[2]
        
    elif weekday == "Четверг":
        weekday = calendar.day_name[3]
        
    elif weekday == "Пятница":
        weekday = calendar.day_name[4]
        
    elif weekday == "Суббота":
        weekday = calendar.day_name[5]
        
    elif weekday == "Воскресенье":
        weekday = calendar.day_name[6]
        
    else:
        print("Такого для недели нет в базе")"""
    add_sub = {"chat_id":id,"subject":key,"Description":value,"weekday":weekday,"time":time}
    description.insert_one(add_sub)




def delete_notification(data):
    description.delete_many(data)


