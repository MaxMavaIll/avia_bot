import requests, logging, json

url = 'https://aviasim.com.ua/wp-json/avia/order/get_dates'

def get_dates() -> json:
    get = requests.get(url=url)
    # logging.info(f"\nRequest ----#{get.status_code}#----\n")
    data = json.loads(get.text)
    # data = get.text
    return data