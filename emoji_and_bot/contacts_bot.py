import telebot
from email import message

TOKEN = 'Insert the token of your bot here'

bot = telebot.TeleBot(TOKEN)

del_buttons = telebot.types.ReplyKeyboardRemove()

buttons1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons1.row(telebot.types.KeyboardButton('Экспорт (формат 1)'),
             telebot.types.KeyboardButton('Экспорт (формат 2)'),
             telebot.types.KeyboardButton('Импорт'),
             telebot.types.KeyboardButton('Просмотр'))
buttons1.row(telebot.types.KeyboardButton('Выход'))


def export_with_commas():
    with open('contacts.txt', 'r', encoding='utf-8') as mf:
        lst = mf.readlines()
    s = ''
    for i, elem in enumerate(lst):
        if elem != '\n':
            s += elem.strip()+', '
        else:
            with open('contacts_formatted.txt', 'w', encoding='utf-8') as mf:
                mf.write(s + '\n')
    s = ''


@bot.message_handler(content_types=['document'])
def import_file(msg: telebot.types.Message):
    file = bot.get_file(msg.document.file_id)
    downloaded_file = bot.download_file(file.file_path)
    with open(msg.document.file_name, 'wb') as f_out:
        f_out.write(downloaded_file)
    bot.send_message(chat_id=msg.from_user.id,
                     text='Данные были импортированы.',
                     reply_markup=del_buttons)
    bot.register_next_step_handler(msg, answer)
    bot.send_message(chat_id=msg.from_user.id, text='Продолжим?',
                     reply_markup=buttons1)


@bot.message_handler(commands=['start'])
def hello(msg: telebot.types.Message):
    bot.send_message(chat_id=msg.from_user.id,
                     text='Здравствуйте.\nВыберите вариант работы с данными.',
                     reply_markup=buttons1)
    bot.register_next_step_handler(msg, answer)


@bot.message_handler(content_types=['document'])
def answer(msg: telebot.types.Message):
    if msg.text == 'Экспорт (формат 1)':
        try:
            bot.send_document(chat_id=msg.from_user.id, document=open('contacts.txt', 'rb'))
            bot.register_next_step_handler(msg, answer)
            bot.send_message(chat_id=msg.from_user.id, text='Продолжим?',
                             reply_markup=buttons1)
        except Exception as e:
            bot.reply_to(message, "Ошибка")
    elif msg.text == 'Экспорт (формат 2)':
        try:
            bot.register_next_step_handler(msg, export_with_commas())
            bot.send_document(chat_id=msg.from_user.id, document=open('contacts_formatted.txt', 'rb'))
            bot.register_next_step_handler(msg, answer)
            bot.send_message(chat_id=msg.from_user.id, text='Продолжим?',
                             reply_markup=buttons1)
        except Exception as e:
            bot.reply_to(message, "Ошибка")
    elif msg.text == 'Импорт':
        try:
            bot.register_next_step_handler(msg, import_file)
            bot.send_message(chat_id=msg.from_user.id,
                             text='Пожалуйста, загрузите файл.',
                             reply_markup=del_buttons)
        except Exception as e:
            bot.reply_to(message, "Ошибка")
    elif msg.text == 'Просмотр':
        try:
            with open('contacts.txt', 'r', encoding='utf-8') as mf:
                read = mf.read()
            bot.send_message(chat_id=msg.from_user.id,
                             text=f'{read}',
                             reply_markup=del_buttons)
            bot.register_next_step_handler(msg, answer)
            bot.send_message(chat_id=msg.from_user.id, text='Продолжим?',
                             reply_markup=buttons1)
        except Exception as e:
            bot.reply_to(message, "Ошибка")
    elif msg.text == 'Выход':
        try:
            bot.send_message(chat_id=msg.from_user.id, text='Всего доброго!', reply_markup=del_buttons)
        except Exception as e:
            bot.reply_to(message, "Ошибка")
    else:
        try:
            bot.register_next_step_handler(msg, answer)
            bot.send_message(chat_id=msg.from_user.id, text='Пожалуйста, используйте кнопки.')

            bot.send_message(chat_id=msg.from_user.id, text='Выберите режим вариант работы с данными.', reply_markup=buttons1)
        except Exception as e:
            bot.reply_to(message, "Ошибка")


bot.polling()
