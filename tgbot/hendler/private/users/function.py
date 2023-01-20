import phonenumbers, logging, datetime
from email_validator import validate_email, EmailNotValidError
import config


async def create_count_people(data: str=None):
    # data.setdefault('count_people', {})
    if data['count_people'] == {}:
        data['count_people']['name'] = ''
        data['count_people']['nomber'] = ''
        data['count_people']['email'] = ''
        data['count_people']['day'] = ''
        data['count_people']['time'] = []
        data['count_people']['duration'] = []
        data['count_people']['price'] = ''
        data['count_people']['comment'] = ''
        data['count_people']['gift'] = ''


async def check_nomber(nomberf: list = '') -> bool:
    list_spaces = [' ', '-']
    nomber = nomberf['nomber']
    if len(nomber) < 10:
        return False 
    
    elif nomber[0] == "3":
        nomber = "+" + nomber

    elif nomber not in "+38":
        nomber = "+38" + nomber

    for i in list_spaces:
        nomber = nomber.replace(i, '')
        
    nomberf['nomber'] = nomber

    nomber = phonenumbers.parse(nomber)

    return phonenumbers.is_possible_number(nomber)
    
    
async def check_email(email: str = '') -> bool:
    try:
        email = validate_email(email)
        email = email.email
        logging.debug(f'email: {email}')
        return True
    
    except EmailNotValidError as errorMsg:
        logging.error(f'{str(errorMsg)}')
        return False

async def get_free_time(day: int = None):
    # return day
    return False

def time(time: list = [], duration: list = []) -> str:
    message = ""
    # time.sort()
    # duration.
    first = datetime.datetime.utcfromtimestamp(time[0]).hour
    last = first
    for index in range(len(time)):
        
        t = datetime.datetime.utcfromtimestamp(time[index]).hour

        if duration[index] == '60':
            first = last = t
            if time[index] == time[-1]:
                message += f'{t}:00-{t+1}:00'
                break
            message += f'{first}:00-{last+1}:00, '
        

        # if t - last == 1:
        #     last += 1 

        # elif t - last >= 2:
        #     message += f'{first}:00-{last+1}:00, '
        #     first = last = t

        
        elif duration[index] == '30':
            first = last = t
            if time[index] == time[-1]:
                message += f'{t}:00-{t}:30'
                break
            message += f'{first}:00-{last}:30, '

    return message

def get_amount( list = [], duration: list = []) -> int:
    sum = 0
    for index in range(len(list)):
        if duration[index] == config.agree_time[0]:
            sum += config.amount[0]
        if duration[index] == config.agree_time[1]:
            sum += config.amount[1]

    return sum

def gift(gift: str = None):
    if gift == 'on':
        return "Так"
    return "Ні"