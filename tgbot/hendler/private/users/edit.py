import asyncio

from aiogram import Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery, InputMediaPhoto


from tgbot.state.user.state import *
from tgbot.hendler.private.users.router import user_router
from tgbot.hendler.private.users import function
from tgbot.keyboard.user.inline import *


@user_router.message(state=Write.edit_name)
async def Get_name(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    name = message.text.title()
    last_name = data['count_people']['name']
    new_name = name
    data['count_people']['name'] = name

    await asyncio.sleep(1)
    await message.delete()
    await bot.edit_message_text("Ім'я змінено\n"
                                f"<b>{last_name} -> {new_name}</b>",
                                message.from_user.id, data['id'], reply_markup=edit(data["count_people"], function.time(data["count_people"]["time"])))

@user_router.message(state=Write.edit_nomber)
async def Get_name(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    nomber = message.text.title()
    last_name = data['count_people']['nomber']
    new_name = nomber
    data['count_people']['nomber'] = nomber

    await asyncio.sleep(1)
    await message.delete()

    if not await function.check_nomber(data['count_people']):
        await bot.edit_message_text("Ваш номер телефону не відповідає стандартам\n"
                                "Введіть номер телефону ще раз:", message.from_user.id, data['id'], reply_markup=to_menu(back=True, text='спробувати ще раз', back_to='edit&nomber') )
        return

    await bot.edit_message_text("Номер змінений\n"
                                f"<b>{last_name} -> {new_name}</b>",
                                message.from_user.id, data['id'], reply_markup=edit(data["count_people"], function.time(data["count_people"]["time"])))

@user_router.message(state=Write.edit_email)
async def Get_name(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    email = message.text.title()
    last_name = data['count_people']['email']
    new_name = email
    data['count_people']['email'] = email

    await asyncio.sleep(1)
    await message.delete()

    if not await function.check_email(email):
        await bot.edit_message_text("Ваша пошта не відповідає стандарту\n"
                                "Будь ласка, введіть Вашу пошту ще раз:", message.from_user.id, data['id'], reply_markup=to_menu(back=True, text='спробувати ще раз', back_to='edit&email'))
        return
        
    await bot.edit_message_text("Email змінено\n"
                                f"<b>{last_name} -> {new_name}</b>", 
                                message.from_user.id, data['id'], reply_markup=edit(data["count_people"], function.time(data["count_people"]["time"])))
