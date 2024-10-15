import time
import requests


TOKEN = '155298282:5YNJHMaLZqfIurWECcZ2gOHhrs3RXRIs41oNnvBQ'
BASE_URL  = f'https://tapi.bale.ai/bot{TOKEN}/'


def send_message(chat_id, text):
    url = BASE_URL + 'sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, json=data)
    print(response, 40 * '*')
    return response.json()


def process_update(update):
    from home.models import UserChatId
    chat_id = update['message']['chat']['id']
    if UserChatId.objects.filter(chat_id=chat_id).exists():
        pass
    else:
        UserChatId.objects.create(chat_id=chat_id)
    message_text = update['message']['text']

    send_message(chat_id, message_text)


def get_updates(offset=None):
    url = BASE_URL + 'getUpdates'
    params = {'offset': offset} if offset is not None else {}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()['result']

    return []


def main():
    offset = None

    while True:
        updates = get_updates(offset)

        for update in updates:
            process_update(update)

            offset = update['update_id'] + 1

        time.sleep(5)
