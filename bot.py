import asyncio
from cgitb import text
from ctypes import resize
from email import message
from itertools import count
from lib2to3.pgen2 import token
import logging
from pydoc import describe
from re import sub
from unicodedata import name
from aiogram import Bot, Dispatcher, executor, types
from aiohttp import request
import DataBase
from EduBot_States import CreateandAdd_states
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.mongo import MongoStorage
import schedule
import calendar,datetime
import aioschedule
import os
from aiogram.utils.callback_data import CallbackData


TelegramBot_token = os.environ.get("TELEGRAMBOT_TOKEN")


MongoDB_token = os.environ.get('MONGODB_URI')




# Объект бота
bot = Bot(token=TelegramBot_token)
#Подключение БД
storage = MongoStorage(uri=MongoDB_token)  
# Диспетчер для бота
dp = Dispatcher(bot,storage=storage)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

#фабрика CallBack'ов
CallbackData_my_notification= CallbackData("my_notification", "InlineButtonNumber")

#функция для создане кнопки
def new_sub_button():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button1 =types.KeyboardButton("Создать новое напоминание")
    button2 =types.KeyboardButton("Мои напоминания")
    keyboard.add(button1,button2)
    return keyboard
#конвертация дней недели с англ на рус
def weekday_eng_to_rus(weekday):
    week = {
        "Monday":0,
        "Tuesday":1,
        "Wednesday":2, 
        "Thursday":3 ,
        "Friday":4, 
        "Saturday":5,
        "Sunday":6
    }
    week_ru=["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]
    return week_ru[week.get(weekday)]
#создане кнопок дней недели
def new_weekday_buttons():
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Понедельник",callback_data="Monday")
    button2 = types.InlineKeyboardButton(text="Вторник",callback_data="Tuesday")
    button3 = types.InlineKeyboardButton(text="Среда",callback_data="Wednesday")
    button4 = types.InlineKeyboardButton(text="Четверг",callback_data="Thursday")
    button5 = types.InlineKeyboardButton(text="Пятница",callback_data="Friday")
    button6 = types.InlineKeyboardButton(text="Суббота",callback_data="Saturday")
    button7 = types.InlineKeyboardButton(text="Воскресенье",callback_data="Sunday")

    keyboard.add(button1,button2,button3,button4,button5,button6,button7)
    return keyboard

# Хэндлер на команду /help /start
@dp.message_handler(commands=["help","start"])
async def helper(message: types.Message):
    print(1)
    
    DataBase.set(message.chat.id,message.chat)
    keyboard = new_sub_button()
    await message.answer("Привет!!\nЯ умею создавть текстовые заметки с напоминнием \nЧтобы создать новое напоминание необходимо:\n 1)Создать новое занятие \n 2)Записать что необходимо сделать ",reply_markup=keyboard)     



@dp.message_handler(state = CreateandAdd_states.waiting_sub_for_note)
async def waiting_sub_for_note(message : types.Message,state:FSMContext):
    print(3)    
    await message.answer("Введите что надо сделать")
    await CreateandAdd_states.waiting_note.set() 
    await state.set_data({"subject":message.text})
    

@dp.message_handler(state = CreateandAdd_states.waiting_note)
async def waiting_note_name(message : types.Message,state:FSMContext):
    print(4)
    await state.update_data({"Description":message.text})
    await state.update_data(count = 0)#счетчик введенных дней недели
    
    keyboard = new_weekday_buttons()
    await message.answer("Когда напомнить?",reply_markup=keyboard)

    await time_request(message)

    await CreateandAdd_states.waiting_time.set()

async def time_request(message):
    
    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    keybord.add(types.KeyboardButton("17:00"),types.KeyboardButton("08:00"),types.KeyboardButton("12:00"))
    await message.answer("Во сколько? Выберите из предложенных вариантов или введите свой в формате ЧЧ:ММ",reply_markup=keybord)
    
@dp.callback_query_handler(text = ["Monday","Tuesday","Wednesday", "Thursday" ,"Friday", "Saturday","Sunday"],state= CreateandAdd_states.waiting_time)
async def weekday_handler(call: types.CallbackQuery,state:FSMContext):
    count = await state.get_data()#счетчик введенных дней недели
    count=count.get("count")
    count = int(count)
    await state.update_data({f"weekday{count}": call.data})
    count+=1
    await state.update_data({"count":count})
    
    await call.message.answer("Добавлен новый день напоминания: "+weekday_eng_to_rus(call.data))



@dp.callback_query_handler(CallbackData_my_notification.filter())
async def callbacks(call: types.CallbackQuery, callback_data: dict,state:FSMContext):
    my_notification = await state.get_data()
    my_notification = my_notification.get(callback_data.get("InlineButtonNumber"))
    DataBase.delete_notification(my_notification)
    await call.message.answer("Напоминание удалено")

@dp.message_handler(state = CreateandAdd_states.waiting_time)
async def waiting_time(message : types.Message,state:FSMContext):
    print(6)
    user_data = await state.get_data()
    user_data = user_data.get("count")
    if user_data == 0:
        await message.answer("Введите день недели.")
        keyboard = new_weekday_buttons()
        await message.answer("Когда напомнить?",reply_markup=keyboard)
        await time_request(message)
    else:
        try:
            datetime.datetime.strptime(message.text, '%H:%M')
        except:
            await message.answer("Некоректно введено время.Пример: 05:24(ЧЧ:ММ)")
            await CreateandAdd_states.waiting_time.set()
            return 
        for i in range(0,user_data):
            user_data = await state.get_data()
            DataBase.set_note(message.chat.id,user_data.get("subject"),user_data.get("Description"),user_data.get(f"weekday{i}"),message.text)
        keybord = new_sub_button()
        await message.answer("Заметка успешно создана!",reply_markup= keybord)
        #await state.reset_state()
        #await dp.storage.wait_closed()
        await state.finish()

@dp.message_handler()
async def new_sub(message:types.Message, state:FSMContext):
    DataBase.set(message.chat.id,message.chat)
    if message.text == "Создать новое напоминание":
        print(2)
        await state.reset_data()
        await message.answer("Введите название занятия")
        await CreateandAdd_states.waiting_sub_for_note.set()
    elif message.text == "Мои напоминания":
        my_notification = DataBase.get_many({"chat_id":message.from_user.id})
        print(len([x for x in my_notification]))

        if len([x for x in my_notification]) != 0:
            keyboard = new_sub_button()
            await message.answer("У вас еще нет напоминаний",reply_markup=keyboard)
        else:
            for i,my_notification in enumerate(DataBase.get_many({"chat_id":message.from_user.id}),1):  #для просмотра имеющихся напоминаний
                keyboard = types.InlineKeyboardMarkup()
                #button = types.InlineKeyboardButton(text="Удалить",callback_data=CallbackData_my_notification.new( my_notification.get("chat_id"),my_notification.get("subject"), my_notification.get("Description"),my_notification.get("weekday"),my_notification.get("time").replace(':'," ") ))
                button = types.InlineKeyboardButton(text="Удалить",callback_data=CallbackData_my_notification.new(f"InlineButton{i}"))
                keyboard.add(button)
                await state.update_data({f"InlineButton{i}":{"chat_id":my_notification.get("chat_id"),
                                        "subject":my_notification.get("subject"),
                                        "Description":my_notification.get("Description"),
                                        "weekday":my_notification.get("weekday"),
                                        "time":my_notification.get("time")}})
                if my_notification.get("weekday") == "Tuesday":
                    await message.answer("Занятие:\n   "+my_notification.get("subject")+"\nЧто необходимо сделать:\n   "+my_notification.get("Description")+" во "+weekday_eng_to_rus(my_notification.get("weekday"))+" в "+my_notification.get("time"),reply_markup=keyboard)
                else:
                    await message.answer("Занятие:\n   "+my_notification.get("subject")+"\nЧто необходимо сделать:\n   "+my_notification.get("Description")+" в "+weekday_eng_to_rus(my_notification.get("weekday"))+" в "+my_notification.get("time"),reply_markup=keyboard)
    else:
        await message.answer("Сообщенеи не распознано!")
        await helper(message)








#########################################################
#проверка напоминаний 
async def Notification_checker():
    now = datetime.datetime.now()
    data = DataBase.get({"weekday":calendar.day_name[now.weekday()],"time":now.time().isoformat(timespec="minutes")})
    if data == None:
        print("Джонни,у нас проблемы")
    else:
        print("Notific sended")
        msg = data.get("subject")+"\n"+data.get("Description")
        await bot.send_message(data.get("chat_id"),msg)
        if data.get("chat_id") != 639454374:
            DataBase.delete_notification(data)
        
#Отправление напоминаний
async def scheduler():
    aioschedule.every().second.do(Notification_checker)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())
##########################################################


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True,on_startup=on_startup)
    
