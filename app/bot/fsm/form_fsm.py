from aiogram.fsm.state import State, StatesGroup

# Класи для FSM стану 

class Change_name_form(StatesGroup):
    change_name = State()

class Add_product_form(StatesGroup):
    waiting_for_url = State()
