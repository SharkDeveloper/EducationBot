from aiogram.dispatcher.filters.state import StatesGroup,State

class CreateandAdd_states(StatesGroup):
    waiting_sub = State()
    waiting_sub_for_note = State()
    waiting_note = State()
    when_remind=State()
    waiting_dayofweek = State()
    #timetable
    
    