import json, datetime
from os.path import abspath, exists

def check_new_hour(last_data: dict, key: str|int):
    
    last_time = datetime.datetime.fromtimestamp(last_data["time"])
    now_time = datetime.datetime.now()

    if ( now_time.hour - last_time.hour) == 1:
        del last_data[key][0]

    
def check_existing_file(path_from_main_dir: str = ""):
    path_file = abspath(path_from_main_dir)
    if not exists(path_file):
        with open(path_file, "w") as file:
            json.dump({}, file)
   
    return True

def get_last_data():
    with open('data/last_data.json', "r") as file:
        last_data = json.load(file)
    
    return last_data

def new_registri_time(new_data: list):

    last_data = get_last_data()
    key = list(last_data.keys())[0]
    check_new_hour(last_data, key)
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

def create_dict(key, value):
    time = datetime.datetime.now()
    time = datetime.datetime.timestamp(time)
    a = dict()
    a[key] = value
    a["time"] = time
    return a