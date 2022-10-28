import datetime


def log(msg):
    file = open('log.txt', 'a', encoding='utf-8')
    file.write(f'Дата: {datetime.datetime.now().time()}\nID пользователя: {msg.from_user.id}\n'
               f'Сообщение пользователя: {msg.text}\n')
    file.close()


def log1(msg, answer):
    file = open('log1.log', 'a', encoding='utf-8')
    file.write(f'Дата: {datetime.datetime.now().date()}\nВремя: {datetime.datetime.now().time()}\nID пользователя: {msg.from_user.id}\n'
               f'Сообщение пользователя: {msg.text}\nСообщение от бота: {answer}\n')
    file.close()

