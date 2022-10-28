import telebot
from spy import log
from email import message

TOKEN = 'Insert the token of your bot here'

bot = telebot.TeleBot(TOKEN)

del_buttons = telebot.types.ReplyKeyboardRemove()

buttons1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons1.row(telebot.types.KeyboardButton('Сложение'),
             telebot.types.KeyboardButton('Вычитание'),
             telebot.types.KeyboardButton('Умножение'),
             telebot.types.KeyboardButton('Деление'))
buttons1.row(telebot.types.KeyboardButton('Ещё не определился'))

lst = []


@bot.message_handler(commands=['log'])
def hello(msg: telebot.types.Message):
    log(msg)
    file = open('log.txt', 'r', encoding='utf-8')
    f = file.read()
    file.close()
    bot.send_message(chat_id=msg.from_user.id,
                     text=f'Лог программы\n{f}',
                     reply_markup=del_buttons)


@bot.message_handler()
def hello(msg: telebot.types.Message):
    log(msg)
    bot.send_message(chat_id=msg.from_user.id,
                     text='Здравствуйте.\nВыберите режим работы калькулятора.',
                     reply_markup=buttons1)
    bot.register_next_step_handler(msg, answer)


@bot.message_handler()
def answer(msg: telebot.types.Message):
    log(msg)
    if msg.text == 'Сложение':
        try:
            bot.register_next_step_handler(msg, first_step_addition)
            bot.send_message(chat_id=msg.from_user.id,
                             text='Введите первое число.',
                             reply_markup=telebot.types.ReplyKeyboardRemove())
        except Exception as e:
            bot.reply_to(message, "Ошибка")
    elif msg.text == 'Вычитание':
        try:
            bot.register_next_step_handler(msg, first_step_subtraction)
            bot.send_message(chat_id=msg.from_user.id,
                             text='Введите первое число.',
                             reply_markup=del_buttons)
        except Exception as e:
            bot.reply_to(message, "Ошибка")
    elif msg.text == 'Умножение':
        try:
            bot.register_next_step_handler(msg, first_step_multiplication)
            bot.send_message(chat_id=msg.from_user.id,
                             text='Введите первое число.',
                             reply_markup=del_buttons)
        except Exception as e:
            bot.reply_to(message, "Ошибка")
    elif msg.text == 'Деление':
        try:
            bot.register_next_step_handler(msg, first_step_division)
            bot.send_message(chat_id=msg.from_user.id,
                             text='Введите первое число.',
                             reply_markup=del_buttons)
        except Exception as e:
            bot.reply_to(message, "Ошибка")
    elif msg.text == 'Ещё не определился':
        try:
            bot.send_message(chat_id=msg.from_user.id, text='Возвращайтесь, когда определитесь.',
                             reply_markup=del_buttons)
        except Exception as e:
            bot.reply_to(message, "Ошибка")
    else:
        try:
            bot.register_next_step_handler(msg, answer)
            bot.send_message(chat_id=msg.from_user.id, text='Пожалуйста, используйте кнопки.')

            bot.send_message(chat_id=msg.from_user.id, text='Выберите режим работы калькулятора.',
                             reply_markup=buttons1)
        except Exception as e:
            bot.reply_to(message, "Ошибка")


def first_step_addition(msg: telebot.types.Message):
    global lst
    if msg.text.isdigit():
        log(msg)
        lst.append(int(msg.text))
        bot.register_next_step_handler(msg, second_step_addition)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите второе число.',
                         reply_markup=del_buttons)
    else:
        log(msg)
        bot.register_next_step_handler(msg, first_step_addition)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите правильно первое число!',
                         reply_markup=del_buttons)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите первое число.',
                         reply_markup=del_buttons)


def second_step_addition(msg: telebot.types.Message):
    global lst
    if msg.text.isdigit():
        log(msg)
        lst.append(int(msg.text))
        res = sum(lst)
        bot.send_message(chat_id=msg.from_user.id, text=f'Ответ: {res}',
                         reply_markup=del_buttons)
    else:
        log(msg)
        bot.register_next_step_handler(msg, second_step_addition)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите правильно второе число!',
                         reply_markup=del_buttons)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите второе число.',
                         reply_markup=del_buttons)
    lst = []


def first_step_subtraction(msg: telebot.types.Message):
    global lst
    log(msg)
    if msg.text.isdigit():
        lst.append(int(msg.text))
        bot.register_next_step_handler(msg, second_step_subtraction)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите второе число.',
                         reply_markup=del_buttons)
    else:
        log(msg)
        bot.register_next_step_handler(msg, first_step_subtraction)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите правильно первое число!',
                         reply_markup=del_buttons)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите первое число.',
                         reply_markup=del_buttons)


def second_step_subtraction(msg: telebot.types.Message):
    global lst
    if msg.text.isdigit():
        log(msg)
        lst.append(int(msg.text))
        res = lst[0] - lst[1]
        bot.send_message(chat_id=msg.from_user.id, text=f'Ответ: {res}',
                         reply_markup=del_buttons)
    else:
        log(msg)
        bot.register_next_step_handler(msg, second_step_subtraction)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите правильно второе число!',
                         reply_markup=del_buttons)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите второе число.',
                         reply_markup=del_buttons)
    lst = []


def first_step_multiplication(msg: telebot.types.Message):
    global lst
    if msg.text.isdigit():
        log(msg)
        lst.append(int(msg.text))
        bot.register_next_step_handler(msg, second_step_multiplication)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите второе число.',
                         reply_markup=del_buttons)
    else:
        log(msg)
        bot.register_next_step_handler(msg, first_step_multiplication)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите правильно первое число!',
                         reply_markup=del_buttons)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите первое число.',
                         reply_markup=del_buttons)


def second_step_multiplication(msg: telebot.types.Message):
    global lst
    if msg.text.isdigit():
        log(msg)
        lst.append(int(msg.text))
        res = lst[0] * lst[1]
        bot.send_message(chat_id=msg.from_user.id, text=f'Ответ: {res}',
                         reply_markup=del_buttons)
    else:
        log(msg)
        bot.register_next_step_handler(msg, second_step_multiplication)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите правильно второе число!',
                         reply_markup=del_buttons)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите второе число.',
                         reply_markup=del_buttons)
    lst = []


def first_step_division(msg: telebot.types.Message):
    global lst
    if msg.text.isdigit():
        log(msg)
        lst.append(int(msg.text))
        bot.register_next_step_handler(msg, second_step_division)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите второе число.',
                         reply_markup=del_buttons)
    else:
        log(msg)
        bot.register_next_step_handler(msg, first_step_division)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите правильно первое число!',
                         reply_markup=del_buttons)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите первое число.',
                         reply_markup=del_buttons)


def second_step_division(msg: telebot.types.Message):
    global lst
    if msg.text.isdigit():
        log(msg)
        lst.append(int(msg.text))
        res = lst[0] / lst[1]
        bot.send_message(chat_id=msg.from_user.id, text=f'Ответ: {res}',
                         reply_markup=del_buttons)
    else:
        log(msg)
        bot.register_next_step_handler(msg, second_step_division)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите правильно второе число!',
                         reply_markup=del_buttons)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите второе число.',
                         reply_markup=del_buttons)
    lst = []


bot.polling(none_stop=True, timeout=100)
