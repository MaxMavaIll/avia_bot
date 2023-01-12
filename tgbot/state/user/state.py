from aiogram.dispatcher.filters.state import StatesGroup, State

class Write(StatesGroup):
    """States for checker creating form"""

    get_name = State()
    nomber = State()
    email = State()
    edit_name = State()
    edit_nomber = State()
    edit_email = State()



# EXEMPLE
# class exemple(StatesGroup):
#     """States for checker creating form"""

#     get = State()
#     write = State()