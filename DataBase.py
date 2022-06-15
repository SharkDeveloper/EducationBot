from calendar import week
from aiohttp import client
import pymongo



client = pymongo.MongoClient("mongodb+srv://Admin:12345687@telegrambot.qqtgh.mongodb.net/?retryWrites=true&w=majority")
db = client.telegrambot

collection = db.BotUsers

def set(id,value):
    a=dict(value)   
    collection.update_one({"id":id},{"$set":a},True)

def create_doc(key):
    collection.insert_one({"id":str(key)})


#set_note(1389812823,987,"")

#Timtable 
timetable = db.Subjects

def add_notification(chat_id,subject,descr,weekday):
    if weekday == "Понедельник":
        timetable.update_one({"Monday":[]},{"$addToSet":{"Monday":[chat_id,subject,descr]}},True)
    elif weekday == "Вторник":
        timetable.update_one({"Tuesday":[]},{"$addToSet":{"Tuesday":[chat_id,subject,descr]}},True)
    elif "Среда" in weekday:
        timetable.update_one({"Wednesay":[]},{"$addToSet":{"Wednesday":[chat_id,subject,descr]}},True)
    elif weekday == "Четверг":
        timetable.update_one({"Thursday":[]},{"$addToSet":{"Thursday":[chat_id,subject,descr]}},True)
    elif weekday == "Пятница":
        timetable.update_one({"Friday":[]},{"$addToSet":{"Friday":[chat_id,subject,descr]}},True)
    elif weekday == "Суббота":
        timetable.update_one({"Saturday":[]},{"$addToSet":{"Saturday":[chat_id,subject,descr]}},True)
    elif weekday == "Воскресенье":
        timetable.update_one({"Sunday":[]},{"$addToSet":{"Sunday":[chat_id,subject,descr]}},True)
    else:
        print("Такого для недели нет в базе")
        




description = db.Description

def get(key):
    return description.find_one(key)

def set_note(id,key,value,weekday):
    add_notification(id,key,value,weekday)
    add_sub = {"chat_id":id,"subject":key,"Description":value,"weekday":weekday}
    description.insert_one(add_sub)




#def delete_notification(chat_id,sub,descr):


set_note(1389812823,"1","12","Среда")