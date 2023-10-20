import telebot
from telebot import types

import DBworker as db

i = db.get_last_q_number()
myid = 2120704934
questions = []
bot = telebot.TeleBot("6353886477:AAFQNW07RktVWGmtnPtEwSsg4aEuX5AZP2k")


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Задать вопрос", callback_data="button_click")
    markup.add(button)
    print(message)
    bot.send_message(message.from_user.id, "Приветствуем, выберите действие", reply_markup=markup)
    db.add_user(message.from_user.id)


@bot.message_handler(commands=['make_admin'])
def start(message):
    try:
        print(int(message.text.split()[1]))
        if db.get_by_id(int(message.text.split()[1])):

            db.set_user_type(int(message.text.split()[1]), 404)
            bot.send_message(int(message.text.split()[1]), "Вы были назначены администратором")
    except Exception:
        bot.send_message(message.from_user.id, "Wrong data format")


#
# @bot.message_handler(content_types=['text'])
# def resend(message):


# elif db.get_user_type(message.from_user.id) == 404:
#     markup = types.InlineKeyboardMarkup()
#     button = types.InlineKeyboardButton(text="Ответить на вопросы", callback_data="answer_questions")
#     markup.add(button)
#     bot.send_message(message.from_user.id, "Выберите действие:", reply_markup=markup)
# elif db.get_user_type(message.from_user.id) == 405:
#     message_id = db.get_message_from_answerer(message.from_user.id)
#     db.set_question_answer(message_id, message.text)
#     bot.send_message(db.get_question_author(message_id), f"Ответ:\n{message.text}")
#     db.set_user_type(message.from_user.id, 404)
#     markup = types.InlineKeyboardMarkup()
#     button = types.InlineKeyboardButton(text="Ответить на вопросы", callback_data="answer_questions")
#     markup.add(button)
#     bot.send_message(message.from_user.id, "Выберите действие:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "button_click":
        bot.send_message(call.from_user.id, "Задайте ваш вопрос")
        db.set_user_type(call.from_user.id, 1)
    elif call.data == "answer_questions":
        question = db.get_question()
        bot.send_message(myid, f"Вопрос:\n{question[2]}")
        db.set_user_type(call.from_user.id, 405)
        db.set_current_answerer(question[0], call.from_user.id)


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.reply_to_message is not None and db.get_user_type(message.from_user.id) == 404:
        m_id = db.get_message_id_by_text(message.reply_to_message.text)
        print(m_id)
        db.set_question_answer(m_id, message.text)
        bot.send_message(db.get_question_author(m_id), f"Пришёл новый ответ!\n*Вопрос:* {db.get_text_by_message(m_id)}\n"
                                                       f"*Ответ:* {message.text}", parse_mode='Markdown')
    else:
        global i
        if db.get_user_type(message.from_user.id) == 1:
            db.add_question(message.from_user.id, message.text, i)
            i += 1
            db.set_user_type(message.from_user.id, 0)
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text="Задать вопрос", callback_data="button_click")
            markup.add(button)
            bot.send_message(message.from_user.id,
                             "Ваш вопрос был отправлен в службу поддержки, ожидайте ответа\nВыберите следующее действие:",
                             reply_markup=markup)
            for j in db.get_all_admins():
                bot.send_message(j[0], message.text)


bot.infinity_polling()
