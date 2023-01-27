import json, os
import logging, asyncio
from request.data import get_dates
from datetime import datetime 

from aiogram import Bot
from tgbot.config import load_config
from scheduler.funtion import new_registri_time, new_day, create_dict
# from aiogram.dispatcher.fsm.storage.redis import RedisStorage


path_save_file = "data/pack_for_send.json"

#from schedulers.exceptions import raise_error

async def add_user_checker(bot: Bot):
    # check_existing_file("data/last_data.json")
    # with open('data/last_data.json', "r") as file:
    #     last_data = json.load(file)

    new_data = get_dates()
    env = load_config('.env')
    keys = list(new_data["dates"].keys())[0]
    new_data = new_data["dates"][keys]

    

    if type(new_data) == type(dict()):
        logging.info(f"new_data {type(new_data)}")
        new_data = list(new_data.values())

    logging.info(f"new_data {new_data} {type(new_data)}")


    if new_day(keys):
        time = new_registri_time(new_data)

        if time:
            for t in time:
                t = datetime.utcfromtimestamp(t).strftime("%H:%M")
                for id in env.tg_bot.admin_ids:
                    logging.info(f"I sent admin with id: {id}")
                    message_bot = await bot.send_message(id, f"Хтось записався на {t}")
                    await asyncio.sleep(5)
                    await bot.delete_message(chat_id=message_bot.chat.id, message_id=message_bot.message_id)
        else:
            id = env.tg_bot.admin_ids
            logging.info(f"\n\nit`s ok\n")
        # for time in new_data:
        #     time = datetime.utcfromtimestamp(time)
        #     logging.info(f"time {time}")

    data = create_dict(keys, new_data)
    with open('data/last_data.json', "w") as file:
        json.dump(data, file)

    # for i in 

    # for id in env.tg_bot.admin_ids:
    #     await bot.send_message(id, f"Mama {data}")
