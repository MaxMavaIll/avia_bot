import requests, json, logging
from datetime import datetime, timezone, timedelta

url = 'https://aviasim.com.ua/wp-json/avia/order/get_dates'

get = requests.get(url=url)




def get_dates() -> json:
    get = requests.get(url=url)
    logging.info(f"\nRequest ----#{get.status_code}#----\n")
    data = json.loads(get.text)
    # data = get.text
    return data


def get_day(day_dttm):
    data = get_dates()
    for day, time in data['dates'].items():

        day = datetime.utcfromtimestamp(int(day))
        logging.info(f"{day}, {day_dttm}, {day_dttm == day}")

        if day == day_dttm:
            
            logging.info(f"{time, type(time)}")
            if time == {} or time == []:
                return False
            
            return True

    

def get_time(day_dttm):
    data = get_dates()
    mass = []
    for day, times in data['dates'].items():
        day = datetime.utcfromtimestamp(int(day))
        logging.info(f"{day}, {day_dttm}, {type(times) == type({})}\n\n")
        if day == day_dttm:
            if type(times) == type({}):
                for key, time in times.items():
                    logging.info(f"time in ms {time}")
                    mass.append(datetime.fromtimestamp(time, timezone.utc ))
                return mass
            elif type(times) == type([]):
                for time in times:
                    logging.info(f"time in ms {time}")
                    mass.append(datetime.fromtimestamp(time, timezone.utc ))
                return mass


get = requests.get(url=url)
data = json.loads(get.text)
print(data['dates'])
# now = datetime.utcnow().timestamp()
# epoch = datetime(1970, 1, 1)
# posix_timestamp_millis = (now - epoch) // timedelta(milliseconds=1)
# print(posix_timestamp_millis)
# date = datetime.fromtimestamp(1673395200, timezone.utc ).strftime("%H:%M")
# print(date)# 1673470800



