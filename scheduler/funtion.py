import json, logging
import datetime
from os.path import abspath, exists
import pytz

def delete_previous_hour( first_day: str|int):
    last_data = get_last_data()
    now_time = datetime.datetime.now(pytz.timezone("Europe/Kyiv")) + datetime.timedelta(hours=1)
    
    for time in list(last_data[first_day]):
        time_d = datetime.datetime.utcfromtimestamp(time)
        logging.debug(f"now {now_time.hour} old {time_d.hour}")
        if (now_time.hour - time_d.hour) >= 1:
            print(first_day, time, last_data[first_day] )
            last_data[first_day].remove(time)
        
    write_last_data(last_data)
    

    # last_time = datetime.datetime.fromtimestamp(last_data["time"])
    # now_hour = now_time.hour
    # throught_ten_min = (now_time + datetime.timedelta(minutes=10)).hour

    # if ( throught_ten_min - now_hour) == 1:
    #     del last_data[key][0]

    
def check_existing_file(path_from_main_dir: str = ""):
    path_file = abspath(path_from_main_dir)
    if not exists(path_file):
        with open(path_file, "w") as file:
            json.dump({}, file)
        return False
   
    return True

def get_last_data():
    with open('data/last_data.json', "r") as file:
        last_data = json.load(file)
    
    return last_data

def write_last_data(data):
    with open('data/last_data.json', "w") as file:
        json.dump(data, file)
    

def new_registri_time(new_data: list, key: str):

    last_data = get_last_data()
    # key = list(last_data.keys())[0]
    if last_data != {}:
        # delete_previous_hour(last_data, key)
        last_data = last_data[key]

    mass = []
    for time in last_data:
        if time not in new_data:
            mass.append(time)
    
    return mass

def new_day(day: datetime):
    check_existing_file("data/last_data.json")
    last_data = get_last_data()
    if last_data == {} or day != list(last_data.keys())[0] :
        return False
    return True

def create_dict(key, all_data, value):
    # time = datetime.datetime.now()
    # time = datetime.datetime.timestamp(time)
    
    all_data[key] = value
    # a["time"] = time

def add_last_update_time(all_data: dict):
    time = datetime.datetime.now(pytz.timezone("Europe/Kyiv")) + datetime.timedelta(hours=1)
    time = datetime.datetime.timestamp(time)
    all_data["time"] = time

def add_new_day(new_data: list):
    last_data = get_last_data()
    time = last_data["time"]
    del last_data["time"]
    if type(new_data) == type(dict):
        new_data = list(new_data.values())
    key_last_data = list(last_data.keys())[-1]
    keys_new_data = list(new_data.keys())
    mass = []
    
    for index_last_day in range(1, len(new_data)+1):
        if keys_new_data[index_last_day * -1] == key_last_data:
            for index in range(1, index_last_day):
                last_data[mass[index * -1]] = new_data[mass[index * -1]] 
            last_data["time"] = time
            write_last_data(last_data)
            return
        else:
            mass.append(keys_new_data[index_last_day * -1])

def del_old_day(key: str):
    last_data = get_last_data()
    for day in list(last_data):
        if day != key:
            del last_data[day]
            
        elif day == key:
            write_last_data(last_data)
            return