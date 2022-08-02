from aiogram import types
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)


def add_delete_button(kb: types.inline_keyboard = None):
    if kb is None:
        kb = InlineKeyboardMarkup()
    del_btn = InlineKeyboardButton('Delete', callback_data=f'delete')
    kb.add(del_btn)

    return kb


def sub_on_collection(name, kb: types.inline_keyboard = None):
    if kb is None:
        kb = InlineKeyboardMarkup()
    del_btn = InlineKeyboardButton('Sub on collection', callback_data=f'sub {name}')
    kb.add(del_btn)

    return kb


def unsub_on_collection(name, kb: types.inline_keyboard = None):
    if kb is None:
        kb = InlineKeyboardMarkup()
    del_btn = InlineKeyboardButton('Unsub', callback_data=f'unsub {name}')
    kb.add(del_btn)

    return kb