import json
import os
from time import sleep
import traceback
import telebot
from telebot import types
import dotenv

from bot.functions.functions import clear_MD
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
                if collection not in list_of_collections:
                    list_of_collections.append(collection)

    for collection in list_of_collections:
        values = get_info(collection)
        if values:
            name, payment_token, floor_price, floor_price_usd = values
            user_arr = list(filter(lambda x: name in x["collections"], users))
            if len(user_arr) != 0:
                for user in user_arr:
                    text = f"[{name}](https://opensea.io/collection/{collection})\n\nFloor price: {clear_MD(floor_price)} {payment_token} / {clear_MD(floor_price_usd)} $"
                    try:
                        markup = types.InlineKeyboardMarkup()
                        unsub_button = types.InlineKeyboardButton(text='Unsub', callback_data=f'unsub {collection}')
                        del_button = types.InlineKeyboardButton(text='Delete', callback_data='delete')
                        markup.add(unsub_button)
                        markup.add(del_button)
                        bot.send_message(user['chat_id'], text, reply_markup=markup)
                    except Exception as exc:
                        ...
                        # traceback.format_exc(exc)


def main():
    # sleep(2 * 60)
    try:
        while 1:
            notifier()
            sleep(30 * 60)
    except Exception as exc:
        # traceback.format_exc(exc)
        sleep(30 * 60)
        main()