from asyncio import to_thread
import asyncio
from email import message
import logging
import time
#import Time_manager
from aiogram import Bot, Dispatcher, executor, types
import DataBase
from EduBot_States import CreateandAdd_states
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.mongo import MongoStorage
import schedule
import calendar,datetime
import aioschedule




# Объект бота
bot = Bot(token="1976410716:AAG7p5K2Hsb6rsYM2YBl0ihSnlMnKwUkFlY")
#Подключение БД
storage = MongoStorage(uri="mongodb+srv://Admin:12345687@telegrambot.qqtgh.mongodb.net/?retryWrites=true&w=majority")  
# Диспетчер для бота
dp = Dispatcher(bot,storage=storage)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)





# Хэндлер на команду /help /start
@dp.message_handler(commands=["help","start"])
async def helper(message: types.Message):
    print(1)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button1 =types.KeyboardButton("Новая заметка")
    keyboard.add(button1)
    await message.answer("Чтобы создать напоминаия необходимо:\n 1)Создать новое занятие \n 2)Записать что надо сделать",reply_markup=keyboard)

@dp.message_handler()
async def new_sub(message:types.Message, state:FSMContext):
    if message.text == "Новая заметка":
        print(2)
        await message.answer("Введите название занятия")
        await CreateandAdd_states.waiting_sub_for_note.set()
    else:
        await message.answer("Сообщенеи не распознано!")
        await helper(message)



    

@dp.message_handler(state = CreateandAdd_states.waiting_dayofweek)
async def waiting_dayofweek(message:types.Message,state:FSMContext):
    global trash
    
    print(5)
    await message.answer("Запомнил)")
    trash.append(message.text)
    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    keybord.add(types.KeyboardButton("17:00"),types.KeyboardButton("08:00"),types.KeyboardButton("12:00"))
    await message.answer("Во сколько?",reply_markup=keybord)
    await CreateandAdd_states.waiting_time.set()
    
data=dict()
#проверка напоминаний 
async def Notification_checker():
    print("time manager working")
    now = datetime.datetime.now()
    data = DataBase.get({"weekday":"Среда"})             #DataBase.get({"weekday":calendar.day_name[now.weekday()],"time":now.time().isoformat(timespec="minutes")})
    print("sjd;lfkaj")
    if data != None:
        print(data.get("chat_id"),data.get("subject")+"\n"+data.get("Description"))
        print("Notific sended")
        msg = data.get("subject")+"\n"+data.get("Description")
        await bot.send_message(data.get("chat_id"),msg)
#Отправление напоминаний
async def scheduler():
    aioschedule.every().second.do(Notification_checker)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())



@dp.message_handler(state = CreateandAdd_states.waiting_time)
async def waiting_time(message : types.Message,state:FSMContext):
    print(6)
    global trash
    DataBase.set_note(message.chat.id,trash[0],trash[1],trash[2],message.text)
    trash.clear
    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    keybord.add(types.KeyboardButton("Новая заметка"))
    await message.answer("Заметка успешно создана!",reply_markup= keybord)
    await state.reset_state()
    await dp.storage.wait_closed()
    await state.finish()

trash = [] #просто существует ,чтобы предавать данные (костыль)

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
    #DataBase.set_note(message.chat.id,trash,{message.text:""})
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    keyboard.add(types.KeyboardButton("Понедельник"),types.KeyboardButton("Вторник"),types.KeyboardButton("Среда"),types.KeyboardButton("Четверг"),types.KeyboardButton("Пятница"),types.KeyboardButton("Суббота"),types.KeyboardButton("Воскресенье"))
    await message.answer("Когда напомнить?",reply_markup=keyboard)
    await CreateandAdd_states.waiting_dayofweek.set()
   
@dp.message_handler(commands="random")
async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="random_value"))
    await message.answer("Нажмите на кнопку, чтобы бот отправил число от 1 до 10", reply_markup=keyboard)

@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
    print("CallBack")
    await call.message.answer("CallBack")




if __name__ == "__main__":
    #Запуск цикла с проверкой событий (Тайм менеджер)
    #Time_manager.run_continuously()
    # Запуск бота
    executor.start_polling(dp, skip_updates=True,on_startup=on_startup)
    
