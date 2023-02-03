import json, os
import logging, asyncio
from request.data import get_dates
from datetime import datetime 

from aiogram import Bot
from tgbot.config import load_config
from scheduler import funtion as f # new_registri_time, create_dict, check_existing_file, add_last_update_time, delete_previous_hour
# from aiogram.dispatcher.fsm.storage.redis import RedisStorage


path_save_file = "data/pack_for_send.json"
time_del_message = 60 * 60

#from schedulers.exceptions import raise_error

async def add_user_checker(bot: Bot):
    # check_existing_file("data/last_data.json")
    # with open('data/last_data.json', "r") as file:
    #     last_data = json.load(file)

    new_data = get_dates()
    env = load_config('.env')
    # keys = list(new_data["dates"].keys())[0]
    # new_data = new_data["dates"][key]
    new_datas = new_data["dates"]
    first_day = list(new_datas.keys())[0]
    second_day = list(new_datas.keys())[1]

    f.check_existing_file("data/last_data.json")
    f.del_old_day(first_day)
    f.add_new_day(new_datas)
    f.delete_previous_hour(first_day)

    for key, new_data in new_datas.items():


        if type(new_data) == type(dict()):
            logging.debug(f"new_data {type(new_data)}")
            new_data = list(new_data.values())

        logging.debug(f"new_data {new_data} {type(new_data)}")


        time = f.new_registri_time(new_data, key)
        if time:
            for t in time:
                t = datetime.utcfromtimestamp(t).strftime("%d.%m.%Y o %H:%M")
                m = env.tg_bot.admin_ids
                for id in env.tg_bot.admin_ids:
                    if id in env.tg_bot.get_all_time:
                        logging.info(f"I sent admin with id: {id}")
                        
                        text = f"""
                        Шановний клієнте, дякуємо за  замовлення польоту на авіасимуляторі <b>Боїнг 737</b>!\nЧекаємо Вас {t} за адресою: вул. Герцена, 35.\nБажаємо гарного відпочинку та приємних вражень! 
                        """
                        message_bot = await bot.send_message(id, text)
                    elif key in [first_day, second_day]:
                        logging.info(f"I sent admin with id: {id}")
                        first_day = await bot.send_message(id, f"Хтось записався на <b>{t}</b>")


                    # message_bot = await bot.send_message(id, f"Хтось записався на <b>{t}</b>")
                    # await asyncio.sleep(time_del_message)
                    # await bot.delete_message(chat_id=message_bot.chat.id, message_id=message_bot.message_id)
        else:
            logging.info(f"{key} it`s ok")


        f.create_dict(key, new_datas, new_data) # Перезапис 
        # delete_previous_hour(key)
    f.add_last_update_time(new_datas) # Додавання часу коли була зроблена запис
    # del_old_day()
    with open('data/last_data.json', "w") as file:
        json.dump(new_datas, file)

