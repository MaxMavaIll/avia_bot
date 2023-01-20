import asyncio, logging
import config
from datetime import datetime

from aiogram import Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from request.get_dates import get_day, get_time

from tgbot.state.user.state import *
from tgbot.hendler.private.users.router import user_router
from tgbot.hendler.private.users import function
from tgbot.keyboard.user.inline import *




@user_router.callback_query(text="write")
async def create_checker(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await function.create_count_people(data)
    await callback.message.edit_text("Для того щоб здійснити політ, Вам потрібно ввести деякі дані.\n\n"
                                     "Будь ласка, ведіть Ваше ім'я:", reply_markup=to_menu())
    logging.debug(f"1. {data}")
    await state.update_data(data)
    await state.set_state(Write.get_name)



@user_router.message(state=Write.get_name)
async def Get_name(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    name = message.text.title()
    data['count_people']['name'] = name

    await asyncio.sleep(1)
    await message.delete()
    await bot.edit_message_text("Будь ласка, ведіть Ваш номер телефону:", message.from_user.id, data['id'], reply_markup=to_menu(back=True, text='назад', back_to='back&name'))
    
    logging.debug(f"2. {data}")
    await state.update_data(data)
    await state.set_state(Write.nomber)

@user_router.message(state=Write.nomber)
async def Get_nomber(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    nomber = message.text
    data['count_people']['nomber'] = nomber

    await asyncio.sleep(1)
    await message.delete()

    if False : #not await function.check_nomber(data['count_people']):
        await bot.edit_message_text("Ваш номер телефону не відповідає стандартам\n"
                                "Введіть номер телефону ще раз:", message.from_user.id, data['id'], reply_markup=to_menu(back=True, text='спробувати ще раз', back_to='back&nomber') )
        return

    await bot.edit_message_text("Будь ласка, введіть Вашу електрону пошту:", message.from_user.id, data['id'], reply_markup=to_menu(back=True, text='назад', back_to='back&nomber'))

    logging.debug(f"3. {data}")
    await state.update_data(data)
    await state.set_state(Write.email)# if back == True else await state.set_state(Write.email)

@user_router.message(state=Write.email)
async def Get_email(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    email = message.text
    data['count_people']['email'] = email

    await asyncio.sleep(1)
    await message.delete()

    if False:#not await function.check_email(email):
        await bot.edit_message_text("Ваша пошта не відповідає стандарту\n"
                                "Будь ласка, введіть Вашу пошту ще раз:", message.from_user.id, data['id'], reply_markup=to_menu(back=True, text='спробувати ще раз', back_to='back&name'))
        return

    await bot.edit_message_text("Будь ласка, виберіть день:", message.from_user.id, data['id'], reply_markup=list_days(range(config.work_day)))
    logging.debug(f"4. {data}")
    await state.update_data(data)
    await state.set_state(None)


@user_router.callback_query(Text(text_startswith="day&"))
async def create_checker(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    logging.info(callback.data.split('&')[-1])
    now = datetime.utcnow()
    day = datetime(now.year, now.month, now.day, 0, 0) + timedelta(days=int(callback.data.split('&')[-1]))

    data['count_people']['day'] = day

    if not get_day(day):
        await callback.message.edit_text("Цей день зайнятий. Поверніться назат і виберіть інший.", reply_markup=to_menu(True, 'Вибрати інший день', 'back&day'))
        return 


    await callback.message.edit_text("Будь ласка, введіть час:", reply_markup=list_hours(day, get_time(day)))

    logging.debug(f"5. {data}")
    await state.update_data(data)

@user_router.callback_query(Text(text_startswith="hour&"))
async def create_checker(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    logging.info(callback.data.split('&')[-1])
    hour = callback.data.split('&')[-1]
    name = data['count_people']['name']
    nomber = data['count_people']['nomber']
    email = data['count_people']['email']
    day = data['count_people']['day']
    time = data['count_people']['time']
    duration = data['count_people']['duration']
    comment = data['count_people']['comment']
    gift = data['count_people']['gift']

    free_time = await function.get_free_time()
    if free_time is None:
        await callback.message.edit_text("Цей день вже зайнятий", reply_markup = to_menu())
        return

    if hour == "clear":
        duration.clear()
        time.clear()
        logging.info(f"{data, day, time}")
        await callback.message.edit_text(f"Будь ласка, виберіть час:",reply_markup=list_hours(day, get_time(day), time ))

    elif hour != 'next':
        logging.info(f"{data, day, time}")
        if hour in config.agree_time:

            duration.append(hour)  
            amount = function.get_amount(time, duration)
            await callback.message.edit_text(f"Ціна {amount} грн\nВибраний час: \n{function.time(time, duration)}", reply_markup=list_hours(day, get_time(day) , time, True ))
            return

        time.append(float(hour))      
        await callback.message.edit_text(f"Уточніть: ",reply_markup=enter_haft_hour())
        
    
    elif hour == 'next' and time == []:
        await callback.message.edit_text("<b>Ви не вибрали час!</b>\n"
                                         "Будь ласка, виберіть час:",
                                         reply_markup=list_hours(day, get_time(day) ))

    else:
        # await callback.message.edit_text("<b>Тут ти можеш добавити коментар (це не обов'язкове поле)</b>\n\n", 
        #                                 reply_markup= )

        data['count_people']['price'] = amount = function.get_amount(time, duration)
        output_day = day.strftime("%d.%m.%y")
        gift = function.gift(gift)
        await callback.message.edit_text("<b>Провірь введені дані</b>\n\n"
                                         f"Iм'я: <i>{name}</i>  \n"
                                         f"Число: <i>{output_day}</i>\n"
                                         f"Час: <i>{function.time(time, duration)}</i>\n"
                                         f"Email: <i>{email}</i>\n"
                                         f"Номер телефону: <i>{nomber}</i>\n"
                                         f"Загальна сума: {amount} грн\n"
                                         f"**Якщо бажаєте додати коментарій перейдіть в розділ 'Редагувати'**\n"
                                         f"Коментарій: {comment}\n"
                                         f"Подарунковий сертифікат: {gift}", reply_markup=check_input_data())

    logging.debug(f"6. {data}")

    await state.update_data(data)
    
@user_router.callback_query(Text(text_startswith="edit&"))
async def create_checker(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message = callback.data.split('&')[-1]
    day = data["count_people"]["day"]
    time = data["count_people"]["time"]
    duration = data["count_people"]["duration"]

    if message == 'edit':
        await callback.message.edit_text("Вибири що ти хочеш змінити", reply_markup=edit(data["count_people"], function.time(time, duration )))
    
    elif message == 'name':
        await callback.message.edit_text("Будь ласка ведіть нове ім'я:")
        await state.set_state(Write.edit_name)

    elif message == 'nomber':
        await callback.message.edit_text("Будь ласка ведіть новий номер телефону:")
        await state.set_state(Write.edit_nomber)

    elif message == 'email':
        await callback.message.edit_text("Будь ласка ведіть новий email:")
        await state.set_state(Write.edit_email)
    
    elif message == 'day':
        pass

    elif message == 'time':
        await callback.message.edit_text(f"Вибраний час: \n{function.time(time, duration)}", reply_markup=list_hours_edit(day, get_time(day)))

    




@user_router.callback_query(Text(text_startswith="pay&"))
async def create_checker(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.set_state()

    await callback.message.edit_text("Виберіть спосіб оплати", reply_markup=payment())


@user_router.callback_query(text="cash")
async def create_checker(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.set_state()

    await callback.message.edit_text("Дякую Вас записано!", reply_markup=to_menu())


@user_router.callback_query(Text(text_startswith="payment_card"))
async def create_checker(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.set_state()

    await callback.message.edit_text("Нажаль ця опція зараз не доступна", reply_markup=to_menu(back=True, text="Повернутися назад", back_to='pay&back'))


@user_router.callback_query(Text(text_startswith="back&"))
async def create_checker(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message = callback.data.split('&')[-1]
    if message == 'name':
        await callback.message.edit_text("Будь ласка, ведіть Ваше ім'я:", reply_markup=to_menu(back=True, text='назад', back_to='edit&edit'))
        await state.set_state(Write.get_name)
    
    elif message == 'nomber':
        await callback.message.edit_text("Будь ласка, ведіть Ваш номер телефону:", reply_markup=to_menu(back=True, text='назад', back_to='edit&edit'))
        await state.set_state(Write.nomber)
    
    elif message == 'email':
        await callback.message.edit_text("Будь ласка, введіть Вашу електрону пошту:", reply_markup=to_menu(back=True, text='назад', back_to='edit&edit'))
        await state.set_state(Write.email)

    elif message == 'day':
        data["count_people"]["time"].clear()
        data["count_people"]["duration"].clear()
        await callback.message.edit_text("Будь ласка, виберіть день:", reply_markup=list_days(range(config.work_day)))

    elif message == 'hour':
        pass