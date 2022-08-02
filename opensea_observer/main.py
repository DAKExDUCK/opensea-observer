import json
import os
from time import sleep
import traceback
import telebot
import dotenv

from bot.functions.functions import clear_MD
from opensea_observer.functions import get_buttons
from .parser import get_info

dotenv.load_dotenv()


def notifier():
    bot = telebot.TeleBot(os.getenv('TOKEN'), parse_mode='MarkdownV2')

    list_of_collections = []
    with open('users.json') as file:
        data = json.load(file)
        users = data.get('users', [])
        for user in users:
            for collection in user['collections']:
                if collection['name'] not in list_of_collections:
                    list_of_collections.append(collection)

    for collection in list_of_collections:
        values = get_info(collection['name'])
        if values:
            name, payment_token, floor_price, floor_price_usd = values
            user_arr = list(filter(lambda x: collection in x["collections"], users))
            if len(user_arr) != 0:
                for user in user_arr:
                    difference = 0
                    if 'last_floor_price_usd' in collection:
                        if collection['last_floor_price_usd'] > floor_price_usd:
                            difference = round(((collection['last_floor_price_usd'] - floor_price_usd)/collection['last_floor_price_usd'] * 100), 2)
                        else:
                            difference = round(((floor_price_usd - collection['last_floor_price_usd'])/collection['last_floor_price_usd'] * 100), 2)
                        if difference > 0:
                            difference_str = f"\+{str(difference)}"
                    else:
                        user['collections'][user['collections'].index(
                                    list(filter(lambda x: x["name"]==collection['name'], user['collections']))[0])
                                    ]['last_floor_price_usd'] = floor_price_usd
                            
                        with open('users.json', 'w') as file:
                            json.dump(data, file)
                    if 'last_floor_price_usd' in collection:
                        text = (f"[{name}](https://opensea.io/collection/{collection['name']})\n\n"
                                f"Floor price: {clear_MD(floor_price)} {payment_token}"
                                f" / {clear_MD(round(floor_price_usd, 2))} $"
                                f" / {clear_MD(difference_str)}%")
                    else:
                        text = f"[{name}](https://opensea.io/collection/{collection['name']})\n\nFloor price: {clear_MD(floor_price)} {payment_token} / {clear_MD(round(floor_price_usd, 2))} $"

                    try:
                        if difference < -5 or difference > 5:
                            user['collections'][user['collections'].index(
                                    list(filter(lambda x: x["name"]==collection['name'], user['collections']))[0])
                                    ]['last_floor_price_usd'] = floor_price_usd
                        
                            markup = get_buttons(collection)
                            bot.send_message(user['chat_id'], text, reply_markup=markup)
                    except Exception:
                        ...
                        print(traceback.format_exc())


def main():
    # sleep(2 * 60)
    try:
        while 1:
            notifier()
            sleep(30 * 60)
    except Exception:
        print(traceback.format_exc())
        sleep(30 * 60)
        main()