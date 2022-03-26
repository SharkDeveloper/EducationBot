
from email import message
from gc import callbacks
import logging
from pydoc import text
from aiogram import Bot, Dispatcher, executor, types
import DataBase
from EduBot_States import CreateandAdd_states
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.mongo import MongoStorage

# Объект бота
bot = Bot(token="1976410716:AAG7p5K2Hsb6rsYM2YBl0ihSnlMnKwUkFlY")
#Подключение БД
storage = MongoStorage(uri="mongodb+srv://Admin:12345687@telegrambot.qqtgh.mongodb.net/telegrambot?retryWrites=true&w=majority")  
# Диспетчер для бота
dp = Dispatcher(bot,storage=storage)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# Хэндлер на команду /help
@dp.message_handler(commands=["start"])
async def starter(message: types.Message):
    await message.answer("Введите название предмета")
    #вызов состояния 


@dp.message_handler(commands=["help"])
async def helper(message: types.Message):
    print(1)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button = types.KeyboardButton("Новый предмет")
    button1 =types.KeyboardButton("Новая заметка")
    keyboard.add(button,button1)
    await message.answer("Чтобы создать напоминаия необходимо:\n 1)Создать новый предмет \n 2)Записать дз/напоминает о дедлайне ",reply_markup=keyboard)

@dp.message_handler()
async def new_sub(message:types.Message, state:FSMContext):
    if message.text == "Новый предмет":
        print(2)
        await message.reply("Введите название предмета")
        DataBase.set(message.chat.id,message.chat)
        await CreateandAdd_states.waiting_sub.set()
    elif message.text == "Новая заметка":
        print(4)
        await message.answer("Введите название предмета")
        await CreateandAdd_states.waiting_sub_for_note.set()
    elif message.text == "След.занятие":
        DataBase.set_note(message.chat.id,trash,)

        await dp.storage.close()
        await dp.storage.wait_closed()
        await state.finish()
    elif message.text == "Другое...":
        await message.answer("Введите дату")
        await CreateandAdd_states.when_remind.set()
    elif message.text == "Создать расписание":
        await message.answer("Введите день недели")
        await CreateandAdd_states.waiting_dayofweek.set()
    else:
        await message.answer("Сообщенеи не распознано!")



    

@dp.message_handler(state = CreateandAdd_states.waiting_dayofweek)
async def waiting_dayofweek(message:types.Message,state:FSMContext):
    print(7)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button1 =types.KeyboardButton("Числитель")
    button2 = types.KeyboardButton("Знаменатель")
    button3 = types.KeyboardButton("Всегда")
    keyboard.add(button1,button2,button3)
    await message.answer("Запомнил)",reply_markup=keyboard)
    await state.reset_state()
    await dp.storage.close()
    await dp.storage.wait_closed()
    await state.finish()
    
@dp.message_handler(state = CreateandAdd_states.waiting_sub)
async def waiting_sub_name(message:types.Message,state:FSMContext):
    print(3)
    DataBase.creat_sub(message.chat.id,message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button1 =types.KeyboardButton("Новая заметка")
    button2 = types.KeyboardButton("Создать расписание")
    keyboard.add(button1,button2)
    await message.answer("Предмет успешно создан!",reply_markup=keyboard)
    



trash = "" #просто существует ,чтобы предавать данные (костыль)

@dp.message_handler(state = CreateandAdd_states.waiting_sub_for_note)
async def waiting_sub_note(message : types.Message,state:FSMContext):
    print(5)
    if DataBase.get({"id":message.chat.id,message.text:""}) == None:
        await message.answer("Такого предмета не существует.")
        await helper(message)
        #await dp.storage.close()
        #await dp.storage.wait_closed()
        #await state.finish()

    else:
        await message.answer("Введите текст заметки")
        await CreateandAdd_states.waiting_note.set()
        global trash
        trash = message.text  # DataBase.get({"id":message.chat.id,message.text:""})
        print(trash)

@dp.message_handler(state = CreateandAdd_states.when_remind)
async def when_remind(message : types.Message,state:FSMContext):
    print(8)
    await dp.storage.close()
    await dp.storage.wait_closed()
    await state.finish()

@dp.message_handler(state = CreateandAdd_states.waiting_note)
async def waiting_note_name(message : types.Message,state:FSMContext):
    print(6)
    global trash
    DataBase.set_note(message.chat.id,trash,{message.text:""})
    await message.answer("Заметка успешно создана!")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    keyboard.add(types.KeyboardButton("Понедельник"),types.KeyboardButton("Вторник"),types.KeyboardButton("Среда"),types.KeyboardButton("Четверг"),types.KeyboardButton("Пятница"),types.KeyboardButton("Суббота"),types.KeyboardButton("Воскресенье"))
    await message.answer("Когда напомнить?",reply_markup=keyboard)

#@dp.message_handler(text="След.занятие")
#async def next_lesson(message:types.Message,state:FSMContext):

    #чтото по добавлению в базу данных

    #await dp.storage.close()
    #await dp.storage.wait_closed()
    #await state.finish()
    
#@dp.message_handler(text="Другое...")
#async def next_lesson(message:types.Message,state:FSMContext):
    #await message.answer("Введите дату")
    #await CreateandAdd_states.when_remind.set()

#Новая заметка
#@dp.message_handler(text = "Новая заметка")
#async def note_name(message:types.Message):
    #print(4)
    #await message.answer("Введите название предмета")
    #await CreateandAdd_states.waiting_sub_for_note.set()


@dp.message_handler(commands="random")
async def cmd_random(message: types.Message):
    print(7)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="random_value"))
    await message.answer("Нажмите на кнопку, чтобы бот отправил число от 1 до 10", reply_markup=keyboard)

@dp.callback_query_handler(text="new_sub")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("CallBack")


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

