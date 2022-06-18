import asyncio
from email import message
from lib2to3.pgen2 import token
import logging
from aiogram import Bot, Dispatcher, executor, types
import DataBase
from EduBot_States import CreateandAdd_states
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.mongo import MongoStorage
import schedule
import calendar,datetime
import aioschedule
from boto.s3.connection import S3Connection
import os

TelegramBot_token = os.environ.get("TELEGRAMBOT_TOKEN")
#MongoDB_token = S3Connection(os.environ['MONGODB_URI'])
#token = S3Connection("TELEGRAMBOT_TOKEN")
print(TelegramBot_token)
# Объект бота
bot = Bot(token=TelegramBot_token)
#Подключение БД
storage = MongoStorage(uri=MongoDB_token)  
# Диспетчер для бота
dp = Dispatcher(bot,storage=storage)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="random")
async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="random_value"))
    await message.answer("Нажмите на кнопку, чтобы бот отправил число от 1 до 10", reply_markup=keyboard)


trash = [] #просто существует ,чтобы предавать данные (костыль)

# Хэндлер на команду /help /start
@dp.message_handler(commands=["help","start"])
async def helper(message: types.Message):
    print(1)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button1 =types.KeyboardButton("Новая заметка")
    keyboard.add(button1)
    DataBase.set(message.chat.id,message.chat)
    await message.answer("Привет!!\nЯ умею создавть текстовые заметки \nЧтобы создать напоминаия необходимо:\n 1)Создать новое занятие \n 2)Записать что надо сделать ",reply_markup=keyboard)    
    

@dp.message_handler(state = CreateandAdd_states.waiting_time)
async def waiting_time(message : types.Message,state:FSMContext):
    print(6)
    global trash
    for i in range(2,len(trash)):
        DataBase.set_note(message.chat.id,trash[0],trash[1],trash[i],message.text)
    trash.clear
    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    keybord.add(types.KeyboardButton("Создать еще одну заметку"))
    await message.answer("Заметка успешно создана!",reply_markup= keybord)
    await state.reset_state()
    await dp.storage.wait_closed()
    await state.finish()



@dp.message_handler(state = CreateandAdd_states.waiting_sub_for_note)
async def waiting_sub_for_note(message : types.Message,state:FSMContext):
    print(3)    
    await message.answer("Введите что надо сделать")
    await CreateandAdd_states.waiting_note.set()
    global trash
    trash.append(message.text)  # DataBase.get({"id":message.chat.id,message.text:""})



@dp.message_handler(state = CreateandAdd_states.waiting_note)
async def waiting_note_name(message : types.Message,state:FSMContext):
    print(4)
    global trash
    trash.append(message.text)
    
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Понедельник",callback_data="Monday")
    button2 = types.InlineKeyboardButton(text="Вторник",callback_data="Tuesday")
    button3 = types.InlineKeyboardButton(text="Среда",callback_data="Wednesday")
    button4 = types.InlineKeyboardButton(text="Четверг",callback_data="Thursday")
    button5 = types.InlineKeyboardButton(text="Пятница",callback_data="Friday")
    button6 = types.InlineKeyboardButton(text="Суббота",callback_data="Saturday")
    button7 = types.InlineKeyboardButton(text="Воскресенье",callback_data="Sunday")

    keyboard.add(button1,button2,button3,button4,button5,button6,button7)
    await message.answer("Когда напомнить?",reply_markup=keyboard)
    await state.reset_state()
    await dp.storage.wait_closed()
    await state.finish()
   
@dp.callback_query_handler(text = ["Monday","Tuesday","Wednesday", "Thursday" ,"Friday", "Saturday","Sunday"])
async def weekday_handler(call: types.CallbackQuery):
    await call.answer(call.data)
    global trash
    trash.append(call.data)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Указать время напоминания)"))
    await call.message.answer("Новый день недели добавлен.\nДалее вам следует указать время напоминания",reply_markup=keyboard)

    

@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
    print("CallBack")
    await call.message.answer("CallBack")

@dp.message_handler()
async def new_sub(message:types.Message, state:FSMContext):
    DataBase.set(message.chat.id,message.chat)
    if message.text == "Новая заметка" or message.text == "Создать еще одну заметку":
        print(2)
        await message.answer("Введите название занятия")
        await CreateandAdd_states.waiting_sub_for_note.set()
    elif message.text == "Указать время напоминания)":    
        keybord = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        keybord.add(types.KeyboardButton("17:00"),types.KeyboardButton("08:00"),types.KeyboardButton("12:00"))
        await message.answer("Во сколько? Выберите из предложенных вариантов или введите свой в формате ЧЧ:ММ",reply_markup=keybord)
        await CreateandAdd_states.waiting_time.set()
    else:
        await message.answer("Сообщенеи не распознано!")
        await helper(message)


#########################################################
#проверка напоминаний 
async def Notification_checker():
    now = datetime.datetime.now()
    data = DataBase.get({"weekday":calendar.day_name[now.weekday()],"time":now.time().isoformat(timespec="minutes")})
    if data != None:
        print(data.get("chat_id"),data.get("subject")+"\n"+data.get("Description"))
        print("Notific sended")
        msg = data.get("subject")+"\n"+data.get("Description")
        await bot.send_message(data.get("chat_id"),msg)
        if data.get("chat_id") != 639454374 and data.get("weekday") != calendar.day_name[0]:
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
    #Запуск цикла с проверкой событий (Тайм менеджер)
    #Time_manager.run_continuously()
    # Запуск бота
    executor.start_polling(dp, skip_updates=True,on_startup=on_startup)
    
