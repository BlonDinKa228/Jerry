import logging
import random
from main2 import Sticker, API_TOKEN, Lol, Axir,kb
from asyncio import sleep
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import time


# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Салем \nЯ Джерри"
                         "\n/help")

@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    await message.answer("Этот бот - эксперемент \nИграй и радуйся "
                         "\nВ режиме 'Против Джерри', кубик сначала кидает Джерри а потом вы"
                         "\n/score - оценить"
                         "\n/game - выбрать игру")

@dp.message_handler(commands=["score"])
async def score(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    bt1 = InlineKeyboardButton(text="Да",
                               callback_data="Yes")
    bt2 = InlineKeyboardButton(text="Нет",
                               callback_data="No")
    keyboard.add(bt1,bt2)
    await bot.send_message(chat_id=message.from_user.id,
                           text="Нравится вам мой бот?\n"
                              "(правильный ответ слева)",
                           reply_markup=keyboard)
    await message.delete()

@dp.callback_query_handler(text="Yes")
async def score_callback1(callback: types.CallbackQuery):
    await callback.answer("Красава, я в тебе не сомневался")
@dp.callback_query_handler(text="No")
async def score_callback2(callback: types.CallbackQuery):
    await callback.answer("Неправильный ответ")


@dp.message_handler(commands=["game"])
async def game(message: types.Message):
    await message.answer("В какую игру будем играть?", reply_markup=kb)
    await message.delete()


@dp.message_handler(Text(equals="Казик"))
async def kasik(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    bt1 = InlineKeyboardButton(text="Пожертвовать 1 шиколадку",
                               callback_data="1")
    bt2 = InlineKeyboardButton(text="Я жлоба абосанная",
                               callback_data="lox")
    keyboard.add(bt1, bt2)
    await bot.send_message(chat_id=message.from_user.id,
                           text="Так, чтобы войти в казик, вам нужно заплатить",
                           reply_markup=keyboard)

@dp.callback_query_handler(text="1")
async def kasik_1(callback: types.CallbackQuery):
    await callback.answer(show_alert=True,
                          text="Казик еще не готов, но за чоколадку спасибо")
@dp.callback_query_handler(text="lox")
async def kasik_2(callback: types.CallbackQuery):
    await callback.answer(text="Я тебя услышал")


@dp.message_handler(Text(equals="Дартс"))
async def darts(message: types.Message):
    await message.answer("Попади в центр!")
    v = (await message.answer_dice(emoji="🎯"))
    g = v["dice"]["value"]
    time.sleep(3)
    if (g == 6):
        await bot.send_sticker(message.from_user.id, Axir)
    elif (g == 2) or (g == 3):
        await message.answer("Слабенько")
    elif (g == 4) or (g == 5):
        await message.answer("Почти")
    else:
        await message.answer("Ну ты и бот")
    await message.delete()


@dp.message_handler(Text(equals="Футбл"))
async def footbl(message: types.Message):
    v = (await message.answer_dice(emoji="⚽"))
    g = v["dice"]["value"]
    time.sleep(5)
    if(g == 3) or (g == 4) or (g == 5):
        await message.answer("Ты блю лок?")
    else:
        await message.answer("Попущ")
    await message.delete()


@dp.message_handler(Text(equals="Баскет"))
async def basket(message: types.Message):
    v = (await message.answer_dice(emoji="🏀"))
    g = v["dice"]["value"]
    time.sleep(5)
    if(g == 4) or (g == 5):
        await message.answer("Ашалеть")
    elif (g == 3):
        await bot.send_sticker(message.from_user.id, Lol)
    else:
        await message.answer("Попущ")
    await message.delete()


@dp.message_handler(Text(equals="Кубик"))
async def kub(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Угадай","Против Джерри"]
    button = ("Назад")
    keyboard.add(*buttons).add(button)
    await bot.send_message(message.from_user.id,f"{message.from_user.username}, Будешь угадывать или играть против меня?",
                         reply_markup=keyboard)

@dp.message_handler(Text(equals="Против Джерри"))
async def vs(message: types.Message):
    await message.answer("Крутите [кубики]!")
    time.sleep(1)
    bot = (await message.answer_dice(emoji="🎲"))
    bot = bot["dice"]["value"]
    time.sleep(5)
    user = (await message.answer_dice(emoji="🎲"))
    user = user["dice"]["value"]
    time.sleep(5)
    if bot < user:
        await message.answer("Джерри попущ")
    elif bot > user:
        await message.answer(f"{message.from_user.username} попущ")
    else:
        await message.answer("Вы все попущи!")

@dp.message_handler(Text(equals="Угадай"))
async def ugad(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["1", "2", "3", "4", '5', "6", "Назад"]
    keyboard.add(*buttons)
    await message.answer(text="Какое число загадали?",
                         reply_markup=keyboard)

@dp.message_handler(Text(equals="Назад"))
async def manu(message: types.Message):
    await message.answer(text="Ок",reply_markup=kb)

@dp.message_handler(content_types=["text"])
async def func(message: types.Message):
    if(message.text == "1"or"2"or"3"or"4"or'5'or"6"):
        v = (await message.answer_dice(emoji="🎲"))
        g = v["dice"]["value"]
        time.sleep(4)
        if(g == int(message.text)):
            await message.answer("Экстрасекс?")
        else:
            await message.answer("Лошня")
    else:
        await message.answer("Error")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)