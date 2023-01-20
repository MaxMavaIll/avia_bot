import logging
from datetime import timedelta,time as tm, datetime as dt

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="Відправитись в політ", callback_data="write")
    builder.button(text="Подивитися розклад", url="https://aviasim.com.ua/order")
    builder.button(text="Новини", callback_data="news")
    builder.button(text="Зв'язатися з косультантами", callback_data="help")
    builder.adjust(2)

    return builder.as_markup()


def list_back(args: list, func: str, back: str, last_choice='' ):
    builder = InlineKeyboardBuilder()

    for num in range(len(args)):
        builder.add( InlineKeyboardButton(text=args[num], callback_data=f"{func}&{args[num]}") )

    builder.adjust(4)
    builder.row(InlineKeyboardButton(text="Menu", callback_data="menu"), InlineKeyboardButton(text="Back", callback_data=f'{back}{last_choice}'))


    return builder.as_markup()
    

def to_menu(back: bool = False, text:str = 'Back', back_to: str = 'Back'):
    builder = InlineKeyboardBuilder()
    builder.button(text="Меню", callback_data="menu")

    if back and text:
        builder.button(text=text, callback_data=back_to)
    builder.adjust(2)

    return builder.as_markup()


def list_days(args: list ):
    builder = InlineKeyboardBuilder()

    for num in args:
        now = dt.utcnow()
        next_day = (now + timedelta(days=num)).day
        builder.add( InlineKeyboardButton(text=next_day, callback_data=f"day&{num}") )

    builder.adjust(4)
    builder.row(InlineKeyboardButton(text="Menu", callback_data="menu"), InlineKeyboardButton(text="назад", callback_data=f'back&email'))

    return builder.as_markup()


def list_hours(day: dt = None, time_work: list = None, choose_time: list = [], back: bool = False):
    builder = InlineKeyboardBuilder()

    menu = [
                InlineKeyboardButton(text=f"Меню", callback_data=f"menu"),
                InlineKeyboardButton(text=f"Вибрати інший день", callback_data=f"back&day"),
                InlineKeyboardButton(text=f"Далі", callback_data=f"hour&next")
                ]
    
    # if now.day is day.day:
    #     # available_time = range(now.hour+2, time_work[-1]+1)
    #     for time_hour in time_work:
            
    #         time = time_hour
    #         output = time.strftime("%H:%M")
    #         output_t = time.timestamp()

    #         if time not in choose_time:
    #             builder.add( InlineKeyboardButton(text=f"{output}", callback_data=f"hour&{output_t}")) 
            
    # else:
    for time_hour in time_work:
        output = time_hour.strftime("%H:%M")
        output_t = time_hour.timestamp()

        if output_t not in choose_time:
            builder.add( InlineKeyboardButton(text=f"{output}", callback_data=f"hour&{output_t}") )
    
    if back:
        menu.insert(2, InlineKeyboardButton(text="Видалити вибраний час", callback_data=f"hour&clear"))
        # builder.button(text="Видалити вибраний час", callback_data=f"hour&clear")

    builder.adjust(4)
    builder.row(*menu)
    # builder.row(InlineKeyboardButton(text="Menu", callback_data="menu"), InlineKeyboardButton(text="Back", callback_data=f'{back}{last_choice}'))

    return builder.as_markup()

def enter_haft_hour():
    builder = InlineKeyboardBuilder()
    time = [
        InlineKeyboardButton(text=f"30хв", callback_data=f"hour&30"),
        InlineKeyboardButton(text=f"60хв", callback_data=f"hour&60"),
    ]
    menu = [
                InlineKeyboardButton(text=f"Меню", callback_data=f"menu"),
                InlineKeyboardButton(text=f"Вибрати інший день", callback_data=f"back&day"),
                InlineKeyboardButton(text=f"Далі", callback_data=f"hour&next")
                ]

    builder.row(*time)
    builder.row(*menu)
    return builder.as_markup()

def check_input_data():
    builder = InlineKeyboardBuilder()
    menu = [InlineKeyboardButton(text=f"Меню", callback_data=f"menu"),
            InlineKeyboardButton(text=f"Відредагувати", callback_data=f"edit&edit"),
            InlineKeyboardButton(text=f"Далі", callback_data=f"pay&next")
            ]
    builder.row(*menu)
    return builder.as_markup()

def edit(data: dict=None, time: str = 'time'):
    builder = InlineKeyboardBuilder()
    edit = [
        InlineKeyboardButton(text=f"{data['name']}", callback_data=f"edit&name"),
        InlineKeyboardButton(text=f"{time}", callback_data=f"edit&time"),
        InlineKeyboardButton(text=f"{data['nomber']}", callback_data=f"edit&nomber"),
        InlineKeyboardButton(text=f"{data['email']}", callback_data=f"edit&email"),
    ]

    menu = [
        InlineKeyboardButton(text=f"Меню", callback_data=f"menu"),
        InlineKeyboardButton(text=f"Назад", callback_data=f"hour&next"),
            ]  
    builder.row(*edit)
    builder.row(*menu)
    return builder.as_markup()

def payment():
    builder = InlineKeyboardBuilder()

    menu = [
        InlineKeyboardButton(text=f"Оплатити картою", callback_data=f"payment_card"),
        InlineKeyboardButton(text=f"Оплатити готівкою на місті", callback_data=f"cash"),
            ]
    
    builder.row(*menu)
    return builder.as_markup()

def list_hours_edit(day: int = None, time_work: list = None, choose_time: list = [], back: bool = False):
    builder = InlineKeyboardBuilder()

    menu = [
                InlineKeyboardButton(text=f"Меню", callback_data=f"menu"),
                InlineKeyboardButton(text=f"Вибрати інший день", callback_data=f"back&day"),
                InlineKeyboardButton(text=f"Далі", callback_data=f"edit&edit")
                ]
    

    

    # t = tm(hour=time_work[0])
    
    # if day is now.day:
    #     available_time = range(now.hour+2, time_work[-1]+1)
    #     for time_hour in range(len(available_time)):
    #         time = (now + timedelta(hours=time_hour)).hour + 2

    #         if time not in choose_time:
    #             builder.add( InlineKeyboardButton(text=f"{time}:00", callback_data=f"hour&{time}")) 
            
    # else:
        
    #     for time_hour in range(len(time_work)+1):
    #         time =  time_work[0] + time_hour
    #         if time not in choose_time:
    #             builder.add( InlineKeyboardButton(text=f"{time}:00", callback_data=f"hour&{time}") )
    for time_hour in time_work:
        output = time_hour.strftime("%H:%M")
        output_t = time_hour.timestamp()

        if output_t not in choose_time:
            builder.add( InlineKeyboardButton(text=f"{output}", callback_data=f"hour&{output_t}") )
    
    if back:
        menu.insert(2, InlineKeyboardButton(text="Видалити вибраний час", callback_data=f"hour&clear"))

    if back == 'hour':
        menu.insert(2, InlineKeyboardButton(text="Видалити вибраний час", callback_data=f"hour&clear"))
        # builder.button(text="Видалити вибраний час", callback_data=f"hour&clear")

    builder.adjust(4)
    builder.row(*menu)
    # builder.row(InlineKeyboardButton(text="Menu", callback_data="menu"), InlineKeyboardButton(text="Back", callback_data=f'{back}{last_choice}'))

    return builder.as_markup()


#EXEMPLE)
# def exemple():
#     builder = InlineKeyboardBuilder()
    
#     builder.add(
#         InlineKeyboardButton(
#             text="stop",
#             callback_data="delete"
#         ), 
#         InlineKeyboardButton(
#             text="start",
#             callback_data="start"
#         )
#     )

#     return builder.as_markup()

