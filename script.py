import telebot
from token_bot import TOKEN
import requests
import json
# from telebot import util
# import datetime
# from telebot import types
from random import randrange

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIDxWITCaZnaUelQ0SNlHMTrjd2klAmAAIBAQACVp29CiK-nw64wuY0IwQ')
    bot.send_message(message.chat.id, f'Привет <b>{message.from_user.username}</b>\nТы зачем сюда пришел?\n'
                                      f'Наверное хочешь телеграмм ботов создавать?', parse_mode='HTML')


@bot.message_handler(func=lambda m: m.text == 'да')
def func_yes(message):
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.id - 1, text='<b>Ты уверен</b>\n/da\n/net',
                          parse_mode='HTML')


@bot.message_handler(commands=['net'])
def func_net(message):
    doc = open('tochno.txt', 'rb')
    bot.send_message(message.chat.id, 'Ну ладно')
    bot.send_document(message.chat.id, doc)


@bot.message_handler(commands=['da'])
def func_da(message):
    start_keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Да', callback_data='btn1')
    btn2 = types.InlineKeyboardButton(text='Нет', callback_data='btn2')
    btn3 = types.InlineKeyboardButton(text='Нет', callback_data='btn3')
    start_keyboard.add(btn1, btn2, btn3)
    bot.reply_to(message, 'Подумай еще раз', reply_markup=start_keyboard)


@bot.callback_query_handler(func=lambda c: c.data)
def change_button(callback):
    start_keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Да', callback_data='btn1')
    btn2 = types.InlineKeyboardButton(text='Нет', callback_data='btn2')
    btn3 = types.InlineKeyboardButton(text='Нет', callback_data='btn3')
    l = [btn1, btn2, btn3]
    random.shuffle(l)
    start_keyboard.add(*l)
    x = random.choice(['btn1', 'btn2', 'btn3'])
    if x != callback.data and callback.data != 'btn4':
        try:
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text='Подумай еще раз', reply_markup=start_keyboard)
        except Exception as e:
            print(f'Произошла ошибка: {e}')

    elif x == callback.data:
        start_keyboard = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton(text='Нет', callback_data='btn1')
        btn4 = types.InlineKeyboardButton(text='Да', callback_data='btn4')
        btn3 = types.InlineKeyboardButton(text='Нет', callback_data='btn3')
        start_keyboard.add(btn1, btn4, btn3)
        try:
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text='Подумай еще раз', reply_markup=start_keyboard)
        except Exception as e:
                print(f'Произошла ошибка: {e}')

    elif callback.data == 'btn4':
        murkup = types.InlineKeyboardMarkup()
        btn5 = types.InlineKeyboardButton(text='Зайди сюда', url='https://7qp.github.io/telegram_bot/')
        murkup.add(btn5)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Хорошо',
                              reply_markup=murkup)
        bot.send_message(callback.message.chat.id, 'Хорошо', reply_markup=murkup)


@bot.message_handler(content_types=['photo'])
def func_photo(message):
    photo = open('photo.jpg', 'rb')
    bot.send_photo(message.chat.id, photo, 'Поздравляю, ты почти прошел проверку')
    sent = bot.send_message(message.chat.id, 'Введи свое имя в телеграмме')
    bot.register_next_step_handler(sent, check_func)


def check_func(message):
    message_save = message.text
    if message_save == message.from_user.username:
        murkup = types.InlineKeyboardMarkup()
        btn6 = types.InlineKeyboardButton(text='Ссылка', url='https://stepik.org/course/107302')
        murkup.add(btn6)
        bot.send_message(message.chat.id, 'Добро пожаловать!', reply_markup=murkup)
    else:
        bot.send_message(message.chat.id, 'Имя уаказанно не верно, в доступе отказано.')

bot.polling()