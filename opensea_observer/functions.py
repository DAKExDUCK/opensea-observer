import requests
from telebot import types


def req(name):
    url = f"https://api.opensea.io/api/v1/collection/{name}"
    headers = {"Accept": "application/json"}
    r = requests.get(url, headers=headers)

    return r.status_code, r.json()


def get_buttons(collection):
    markup = types.InlineKeyboardMarkup()
    unsub_button = types.InlineKeyboardButton(text='Unsub', callback_data=f"unsub {collection['name']}")
    del_button = types.InlineKeyboardButton(text='Delete', callback_data='delete')
    markup.add(unsub_button)
    markup.add(del_button)

    return markup