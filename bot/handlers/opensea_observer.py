import json
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import exceptions

from bot.functions.functions import clear_MD
from bot.functions.rights import is_Admin, is_admin
from bot.handlers.logger import logger
from bot.keyboards.default import add_delete_button, sub_on_collection
from opensea_observer.parser import get_info


async def get(message: types.Message):
    try:
        arguments = message.get_args().split()
    except exceptions.MessageTextIsEmpty:
        message.reply("Please add name of collection.\n\n '''/get cryptopunks subwayrats'''", parse_mode='MarkdownV2')
    else:
        for arg in arguments:
            values = get_info(arg)
            if values:
                name, payment_token, floor_price, floor_price_usd = values
                text = f"[{name}](https://opensea.io/collection/{name})\n\nFloor price: {clear_MD(floor_price)} {payment_token} / {clear_MD(floor_price_usd)} $"
                await message.answer(text, parse_mode='MarkdownV2', reply_markup=add_delete_button(sub_on_collection(name)))


async def sub_on_colllection(query: types.CallbackQuery):
    collection_name = query.data.split()[-1]
    try:
        with open('users.json') as file:
            data = json.load(file)
            users = data.get('users', [])
            user_arr = list(filter(lambda x: x["chat_id"]==query.from_user.id, users))
            if user_arr == []:
                new_user = {
                    "chat_id": query.from_user.id,
                    "full_name": query.from_user.full_name,
                    "collections": [collection_name]
                    }
                users.append(new_user)
            else:
                user = user_arr[0]
                if collection_name not in user['collections']:
                    user['collections'].append(collection_name)
        with open('users.json', 'w') as file:
            json.dump(data, file)
        await query.answer('Done!')
    except Exception as exc:
        logger.error(exc)
        await query.answer("Error")


def register_handlers_opensea(dp: Dispatcher):
    dp.register_message_handler(get, commands="get", state="*")

    dp.register_callback_query_handler(
        sub_on_colllection,
        lambda c: 'sub' in c.data,
        state="*"
    )
