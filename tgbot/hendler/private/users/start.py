import logging
from os.path import exists, abspath 

from aiogram import Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from tgbot.hendler.private.users.router import user_router
#from tgbot.state.user.state import 
from tgbot.keyboard.user.inline import menu

path_languague=abspath("data/languague.json")


@user_router.message(Command(commands=["start"]))
async def start( message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    data['count_people'] = {}

    if 'id' in data:
        await bot.delete_message(chat_id=message.from_user.id, message_id=data["id"])
    
    msg = await message.answer(f"Hallo user {message.from_user.first_name} {path_languague}!! ", reply_markup=menu())
    data['id'] = msg.message_id

    logging.debug(data)
    await state.update_data(data)
    await state.set_state(None)


@user_router.callback_query(text='menu')
async def start( callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    data['count_people'] = {}

    await callback.message.edit_text("Menu", reply_markup=menu())

    logging.debug(data)
    await state.update_data(data)
    await state.set_state(None)
