import sqlite3  # работа с sqlite
import uuid  # рандомное хеширование
import hashlib  # хеширование
import re  # регулярные выражения
from prettytable import PrettyTable  # вывод таблицы
import os  # для работы с консолью

# Для отправки по почте
import smtplib  # для работы с SMTP (почта)
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
from email.mime.text import MIMEText  # Текст/HTML


# --- Блок функций --- #

#функции хеширования
def hash_password(password):
    # uuid используется для генерации случайного числа
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

#функции проверки правильности ввода
def is_data_true(data, array_of_data):
    while data not in array_of_data:
        print('Введены неверные данные!')
        data = input('Повторите ввод: ')
    return data

def is_fio_true(text, t):
    re.sub(r'\s+', ' ', text)  #удалит лишние пробелы
    if re.sub(r'\s', '', text) == '' and t != 'patronymic': return None
    for i in range(len(text)):
        if not(text[i].isalpha() or text[i] == '-' or text[i] == ' ' or text[i]==''):
            return None
        if (text[i-1]==' ' or text[i-1]=='' or text[i-1]=='-' or i==0) and text[i].isalpha():
            text = text[:i] + text[i].upper() + text[i+1:]
    return re.sub(r'\s+', ' ', text)

def is_telephone_true(text):
    re.sub(r'\s', '', text)
    return bool(re.fullmatch("^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$", text))


def is_pass_true(text):
    if not(bool(re.fullmatch("^.{8,}$", text))):
        print('\nПароль должен содержать минимум 8 символов!')
        return False
    if not(bool(re.fullmatch("^.*[A-Z]+.*$", text))):
        print('\nВ пароле должна быть как минимум одна заглавная буква!')
        return False
    if not (bool(re.fullmatch("^.*[a-z]+.*$", text))):
        print('\nВ пароле должна быть как минимум одна строчная буква!')
        return False
    if not (bool(re.fullmatch("^.*\d+.*$", text))):
        print('\nВ пароле должна быть как минимум одна цифра!')
        return False
    if not (bool(re.fullmatch(r"^.*[\.\$\^\{\[\(\|\)\*\+\?\\]+.*$", text))):
        print('\nВ пароле должен быть как минимум один специальный символ!')
        return False
    return True

# --- Блок программы --- #

db = sqlite3.connect('server_git.db')
sql = db.cursor() # курсор нужен для того, чтобы вообще работь с базой данных: мы будем добавлять объекты, удалять их и тд

# создадим таблицу
sql.execute("""CREATE TABLE IF NOT EXISTS users (
    фамилия VARCHAR(32),
    имя VARCHAR(32),
    отчество VARCHAR(32),
    телефон text,
    email text,
    логин text not null,
    пароль text,
    пароль_скрытый text,
    primary key (логин)
)""") # IF NOT EXISTS - создать таблицу, если ОНА НЕ СОЗДАНА

db.commit() # подтвердили создание таблицы

main_process = True
main_process_request = '0'
while(main_process):
    print('\n'
          '1-Просмотр пользователей\n'
          '2-Добавление пользователя\n'
          '3-Удаление/изменение пользователя\n'
          '4-Сортировка базы данных\n'
          '5-Отправка на e-mail сообщения пользователю\n'
          '0-Выход из программы')
    main_process_request = input('Ввод: ')
    #обработчик введенного значения
    main_process_request = is_data_true(main_process_request, ['1', '2', '3', '4', '5','0'])

    main_process_request_into = '-1'
    if main_process_request == '0': break

    # вывод таблицы
    if main_process_request == '1':

        # просчет количества пользователей в бд
        counter = 0
        for value in db.execute("SELECT * FROM users"):
            counter += 1

        print(f'    Введите количество пользователей для отображения информации о них (всего - {counter})')
        main_show_users_amount = int(input('    Ввод: '))

        # если введенное число больше максимума
        if main_show_users_amount > counter:
            main_show_users_amount = counter

        # красивый вывод таблицы sql
        os.system('clear')
        table = PrettyTable(['n', 'фамилия', 'имя', 'отчество', 'телефон', 'e-mail', 'логин'])
        id = 1
        for value in db.execute("SELECT * FROM users"):
            if main_show_users_amount == 0:
                break
            table.add_row([str(id)] + list(value[:6]))
            main_show_users_amount -= 1
            id += 1

        print(table)

    # добавление пользователя
    if main_process_request == '2':
        surname = input('    Фамилия: ')
        name = input('    Имя: ')
        patronymic = input('    Отчество: ')
        telephone = input('    Номер телефона в формате +7-(000)-000-00-00: ')
        email = input('    e-mail: ')
        user_login = input('    Логин: ')
        user_password = input('    Пароль: ')

        # проверка логина на пустоту
        while re.sub(r'\s', '', user_login) == '':
            user_login = input('        Введите логин: ')
        sql.execute("SELECT логин FROM users")  # выбрать столбец login в таблице users
        if user_login in [str(i[0]) for i in sql.fetchall()]:
            print('        Такая запись уже имеется!')
        else:
            # проверка пароля
            while is_pass_true(user_password) == False:
                user_password = input('        Введите пароль заново: ')

            # проверка ФИО
            while is_fio_true(surname, 'surname') == None:
                surname = input('        Введите фамилию заново в правильном формате: ')
            while is_fio_true(name, 'name') == None:
                name = input('        Введите Имя заново в правильном формате: ')
            while is_fio_true(patronymic, 'patronymic') == None:
                patronymic = input('        Введите Отчество заново в правильном формате: ')

            # проверка номера
            while is_telephone_true(telephone) == False:
                telephone = input('        Введите номер телефона в формате +7-(000)-000-00-00 заново: ')

            # проверка e-mail
            while bool(re.fullmatch("^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9]+(\.[A-Z|a-z]{2,}){1}$", email)) == False:
                email = input('        Введите email заново: ')

            #хеширование пароля
            hashed_password = hash_password(user_password)
            sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (surname, name, patronymic, telephone, email, user_login, hashed_password, user_password))
            db.commit()  # подтвердили действие
            print('            Зарегистрировано!')

            # if check_password(hashed_password, old_pass):
            #     print('Вы ввели правильный пароль')
            # else:
            #     print('Извините, но пароли не совпадают')

    if main_process_request == '3':
        while main_process_request_into != '0':
            print('    Изменить/удалить пользователя\n'
                  '    1-по фамилии-имени\n'
                  '    2-по логину\n'
                  '    3-по номеру телефона\n'
                  '    0-выход')

            main_process_request_into = input('    Ввод: ')
            is_data_true(main_process_request_into, ['1', '2', '3', '4', '0'])

            if main_process_request_into == '0': break

            if main_process_request_into == '1':
                surname = input('    Фамилия: ')
                name = input('    Имя: ')
                while is_fio_true(surname, 'surname') == None:
                    surname = input('    Введите фамилию заново в правильном формате: ')
                while is_fio_true(name, 'name') == None:
                    name = input('    Введите Имя заново в правильном формате: ')

                sql.execute("SELECT * FROM users WHERE фамилия = ? and имя = ?", (surname,name))
                all = sql.fetchall()
                global into_login
                if len(all) == 0: # если не найдено пользователей
                    print(rf'        Пользователь с фамилией {surname} и именем {name} не найден!')
                    continue
                if len(all) > 1: # если найденных пользователей больше 1
                    # красивый вывод таблицы найденных пользователей
                    table = PrettyTable(['n', 'фамилия', 'имя', 'отчество', 'телефон', 'e-mail', 'логин'])
                    id = 1
                    for i in range(len(all)):
                        table.add_row([str(id)] + list(all[i][:6]))
                        id += 1
                    print(table)
                    print('    Введите номер выбранного пользователя:')
                    into_request = input('    Ввод: ')
                    while not ('1' <= into_request <= str(len(all)+1)):
                        into_request = input('    Ввод: ')

                    # получили уникальный логин выбранного пользователя
                    into_login = all[int(into_request)-1][5]
                    all = all[int(into_request)-1]
                if len(all) == 1:
                    into_login = all[0][5]
                    all = all[0]

            if main_process_request_into == '2':
                temp_data = input('    Введите логин: ')
                while re.sub(r'\s', '', temp_data) == '':
                    temp_data = input('        Введите логин: ')
                sql.execute("SELECT логин FROM users")  # выбрать столбец login в таблице users
                if temp_data not in [str(i[0]) for i in sql.fetchall()]:
                    print('        Пользователя с таким логином нет!')
                    continue
                else:
                    into_login = temp_data
                sql.execute(f"SELECT * FROM users where логин == '{into_login}'")
                all = list(sql.fetchall()[0])

            if main_process_request_into == '3':
                temp_data = input('    Введите номер телефона: ')
                while is_telephone_true(temp_data) == False:
                    temp_data = input('    Введите номер телефона в формате +7-(000)-000-00-00 заново: ')

                sql.execute("SELECT * FROM users WHERE телефон = ?", (temp_data, ))
                all = sql.fetchall()
                if len(all) == 0:  # если не найдено пользователей
                    print(rf'        Пользователь с номером {temp_data} не найден!')
                    continue
                if len(all) > 1:  # если найденных пользователей больше 1
                    # красивый вывод таблицы найденных пользователей
                    table = PrettyTable(['n', 'фамилия', 'имя', 'отчество', 'телефон', 'e-mail', 'логин'])
                    id = 1
                    for i in range(len(all)):
                        table.add_row([str(id)] + list(all[i][:6]))
                        id += 1
                    print(table)
                    print('    Введите номер выбранного пользователя:')
                    into_request = input('    Ввод: ')
                    while not ('1' <= into_request <= str(len(all) + 1)):
                        into_request = input('    Ввод: ')

                    # получили уникальный логин выбранного пользователя
                    into_login = all[int(into_request) - 1][5]
                    all = all[int(into_request) - 1]
                if len(all) == 1:
                    into_login = all[0][5]
                    all = all[0]


            # проверка пароля
            print('    Для операции изменения/удаления нужно обладать правами доступа, поэтому')
            user_password = input('    Введите пароль: ')

            # проверка на соответствие пароля регулярным выражениям
            while is_pass_true(user_password) == False:
                user_password = input('    Введите пароль заново: ')

            if check_password(all[6], user_password) == False:
                print('    Пароль введен неверно, попробуйте в следующий раз!')
                continue
            #если сюда дошло, значит, пароль верный

            print('\n'
                  '    Выберите действие:\n'
                  '    1-изменить\n'
                  '    2-удалить\n')
            main_process_request_into_request = input(    'Ввод: ')
            is_data_true(main_process_request_into_request, ['1','2'])

            if main_process_request_into_request == '1':

                print('\n'
                      '        Что изменить?\n'
                      '        1-фамилию\n'
                      '        2-имя\n'
                      '        3-отчество\n'
                      '        4-телефон\n'
                      '        5-email\n'
                      '        6-пароль\n'
                      '        0 - выход')
                main_process_request_into_edit = input('        Ввод: ')
                is_data_true(main_process_request_into_edit, [str(i) for i in range(0,7)])
                while main_process_request_into_edit != '0':
                    if main_process_request_into_edit == '0':
                        continue

                    if main_process_request_into_edit == '1':
                        temp_data = input('        Новая фамилия: ')
                        while is_fio_true(temp_data, 'surname') == None:
                            temp_data = input('        Введите фамилию заново в правильном формате: ')
                        sql.execute(f"UPDATE users SET фамилия = '{temp_data}' WHERE логин = '{into_login}'")
                        db.commit()
                        print('        Успешно!')
                        main_process_request_into_edit = '0'

                    if main_process_request_into_edit == '2':
                        temp_data = input('        Новое имя: ')
                        while is_fio_true(temp_data, 'name') == None:
                            temp_data = input('        Введите имя заново в правильном формате: ')
                        sql.execute(f"UPDATE users SET имя = '{temp_data}' WHERE логин = '{into_login}'")
                        db.commit()
                        print('        Успешно!')
                        main_process_request_into_edit = '0'

                    if main_process_request_into_edit == '3':
                        temp_data = input('        Новое отчество: ')
                        while is_fio_true(temp_data, 'patronymic') == None:
                            temp_data = input('        Введите отчество заново в правильном формате: ')
                        sql.execute(f"UPDATE users SET отчество = '{temp_data}' WHERE логин = '{into_login}'")
                        db.commit()
                        print('        Успешно!')
                        main_process_request_into_edit = '0'

                    if main_process_request_into_edit == '4':
                        temp_data = input('        Новый номер телефона: ')
                        while is_telephone_true(temp_data) == False:
                            temp_data = input('        Введите номер телефона заново в правильном формате: ')
                        sql.execute(f"UPDATE users SET телефон = '{temp_data}' WHERE логин = '{into_login}'")
                        db.commit()
                        print('        Успешно!')
                        main_process_request_into_edit = '0'

                    if main_process_request_into_edit == '5':
                        temp_data = input('        Новый e-mail: ')
                        while bool(re.fullmatch("^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9]+(\.[A-Z|a-z]{2,}){1}$", temp_data)) == False:
                            temp_data = input('        Введите e-mail заново в правильном формате: ')
                        sql.execute(f"UPDATE users SET email = '{temp_data}' WHERE логин = '{into_login}'")
                        db.commit()
                        print('        Успешно!')
                        main_process_request_into_edit = '0'

                    if main_process_request_into_edit == '4':
                        temp_data = input('        Новый номер телефона: ')
                        while is_telephone_true(temp_data) == False:
                            temp_data = input('        Введите номер телефона заново в правильном формате: ')
                        sql.execute(f"UPDATE users SET телефон = '{temp_data}' WHERE логин = '{into_login}'")
                        db.commit()
                        print('        Успешно!')
                        main_process_request_into_edit = '0'

                    if main_process_request_into_edit == '5':
                        temp_data = input('        Новый e-mail: ')
                        while bool(re.fullmatch("^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9]+(\.[A-Z|a-z]{2,}){1}$", temp_data)) == False:
                            temp_data = input('        Введите e-mail заново в правильном формате: ')
                        sql.execute(f"UPDATE users SET email = '{temp_data}' WHERE логин = '{into_login}'")
                        db.commit()
                        print('        Успешно!')
                        main_process_request_into_edit = '0'

                    if main_process_request_into_edit == '6':
                        temp_data = input('        Новый пароль: ')
                        while is_pass_true(temp_data) == False:
                            temp_data = input('        Введите пароль заново в правильном формате: ')

                        # хеширование пароля
                        hashed_password = hash_password(temp_data)
                        sql.execute(f"UPDATE users SET пароль = '{hashed_password}', пароль_скрытый = '{temp_data}' WHERE логин = '{into_login}'")
                        db.commit()
                        print('        Успешно!')
                        main_process_request_into_edit = '0'

            if main_process_request_into_request == '2':
                print(f'        Вы точно хотите удалить пользователя {into_login}? Операцию нельзя отменить!\n'
                      f'        1-ДА\n'
                      f'        0-НЕТ')
                main_process_request_into_edit = input('        Ввод: ')
                if main_process_request_into_edit not in ['0', '1']:
                    print('Введено что-то непонятное, значит, это автоматически НЕТ')
                    main_process_request_into_edit = '0'
                if main_process_request_into_edit == '1':
                    sql.execute(f"DELETE FROM users WHERE логин = '{into_login}'")
                    db.commit()
                    print(f'        Пользователь {into_login} удален!')
                    break

    if main_process_request == '4':
        print('    Отсортировать базу данных по\n'
              '    1-по фамилии\n'
              '    2-по имени\n'
              '    3-по номеру телефона\n'
              '    0-выход')

        main_process_request_into = input('    Ввод: ')
        is_data_true(main_process_request_into, ['1', '2', '3', '0'])

        print('\n'
              '    1-по возрастанию\n'
              '    2-по убыванию\n')
        main_process_request_into_request = input('    Ввод: ')
        is_data_true(main_process_request_into_request, ['1', '2'])

        if main_process_request_into == '0': break

        if main_process_request_into == '1':
            if main_process_request_into_request == '1':
                ans = sql.execute("SELECT * FROM users ORDER BY фамилия;")
            if main_process_request_into_request == '2':
                ans = sql.execute("SELECT * FROM users ORDER BY фамилия DESC;")

        if main_process_request_into == '2':
            if main_process_request_into_request == '1':
                ans = sql.execute("SELECT * FROM users ORDER BY имя;")
            if main_process_request_into_request == '2':
                ans = sql.execute("SELECT * FROM users ORDER BY имя DESC;")

        if main_process_request_into == '3':
            if main_process_request_into_request == '1':
                ans = sql.execute("SELECT * FROM users ORDER BY телефон;")
            if main_process_request_into_request == '2':
                ans = sql.execute("SELECT * FROM users ORDER BY телефон DESC;")


        # просчет количества пользователей в бд
        counter = 0
        for value in db.execute("SELECT * FROM users"):
            counter += 1

        print(f'    Введите количество пользователей для отображения информации о них (всего - {counter})')
        main_show_users_amount = int(input('    Ввод: '))

        # если введенное число больше максимума
        if main_show_users_amount > counter:
            main_show_users_amount = counter

        # красивый вывод таблицы sql
        os.system('clear')
        table = PrettyTable(['n', 'фамилия', 'имя', 'отчество', 'телефон', 'e-mail', 'логин'])
        id = 1
        for value in ans:
            if main_show_users_amount == 0:
                break
            table.add_row([str(id)] + list(value[:6]))
            main_show_users_amount -= 1
            id += 1

        print(table)

    if main_process_request == '5':
        while main_process_request_into != '0':
            print('    Изменить/удалить пользователя\n'
                  '    1-по фамилии-имени\n'
                  '    2-по логину\n'
                  '    3-по номеру телефона\n'
                  '    0-выход')

            main_process_request_into = input('    Ввод: ')
            is_data_true(main_process_request_into, ['1', '2', '3', '4', '0'])

            if main_process_request_into == '0': break

            if main_process_request_into == '1':
                surname = input('    Фамилия: ')
                name = input('    Имя: ')
                while is_fio_true(surname, 'surname') == None:
                    surname = input('    Введите фамилию заново в правильном формате: ')
                while is_fio_true(name, 'name') == None:
                    name = input('    Введите Имя заново в правильном формате: ')

                sql.execute("SELECT * FROM users WHERE фамилия = ? and имя = ?", (surname, name))
                all = sql.fetchall()

                if len(all) == 0:  # если не найдено пользователей
                    print(rf'        Пользователь с фамилией {surname} и именем {name} не найден!')
                    continue
                if len(all) > 1:  # если найденных пользователей больше 1
                    # красивый вывод таблицы найденных пользователей
                    table = PrettyTable(['n', 'фамилия', 'имя', 'отчество', 'телефон', 'e-mail', 'логин'])
                    id = 1
                    for i in range(len(all)):
                        table.add_row([str(id)] + list(all[i][:6]))
                        id += 1
                    print(table)
                    print('    Введите номер выбранного пользователя:')
                    into_request = input('    Ввод: ')
                    while not ('1' <= into_request <= str(len(all) + 1)):
                        into_request = input('    Ввод: ')

                    # получили уникальный логин выбранного пользователя
                    into_login = all[int(into_request) - 1][5]
                    all = all[int(into_request) - 1]
                if len(all) == 1:
                    into_login = all[0][5]
                    all = all[0]

            if main_process_request_into == '2':
                temp_data = input('    Введите логин: ')
                while re.sub(r'\s', '', temp_data) == '':
                    temp_data = input('        Введите логин: ')
                sql.execute("SELECT логин FROM users")  # выбрать столбец login в таблице users
                if temp_data not in [str(i[0]) for i in sql.fetchall()]:
                    print('        Пользователя с таким логином нет!')
                    continue
                else:
                    into_login = temp_data
                sql.execute(f"SELECT * FROM users where логин == '{into_login}'")
                all = list(sql.fetchall()[0])

            if main_process_request_into == '3':
                temp_data = input('    Введите номер телефона: ')
                while is_telephone_true(temp_data) == False:
                    temp_data = input('    Введите номер телефона в формате +7-(000)-000-00-00 заново: ')

                sql.execute("SELECT * FROM users WHERE телефон = ?", (temp_data,))
                all = sql.fetchall()
                if len(all) == 0:  # если не найдено пользователей
                    print(rf'        Пользователь с номером {temp_data} не найден!')
                    continue
                if len(all) > 1:  # если найденных пользователей больше 1
                    # красивый вывод таблицы найденных пользователей
                    table = PrettyTable(['n', 'фамилия', 'имя', 'отчество', 'телефон', 'e-mail', 'логин'])
                    id = 1
                    for i in range(len(all)):
                        table.add_row([str(id)] + list(all[i][:6]))
                        id += 1
                    print(table)
                    print('    Введите номер выбранного пользователя:')
                    into_request = input('    Ввод: ')
                    while not ('1' <= into_request <= str(len(all) + 1)):
                        into_request = input('    Ввод: ')

                    # получили уникальный логин выбранного пользователя
                    into_login = all[int(into_request) - 1][5]
                    all = all[int(into_request) - 1]
                if len(all) == 1:
                    into_login = all[0][5]
                    all = all[0]

            addr_from = "project.uni.kubsu@gmail.com"  # Адресат

            addr_to = all[4]  # Получатель
            password = "kentrosaurus228"  # Пароль

            msg = MIMEMultipart()  # Создаем сообщение
            msg['From'] = addr_from  # Адресат
            msg['To'] = addr_to  # Получатель

            print('Введите тему сообщения (можно использовать эмодзи)')
            temp_data = input('    Ввод: ')
            msg['Subject'] = temp_data  # Тема сообщения

            print('Введите текст сообщения (можно использовать эмодзи)')
            temp_data = input('    Ввод: ')
            body = temp_data
            msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

            print('Производится отправка, пожалуйста, подождите...')
            server = smtplib.SMTP('smtp.gmail.com', 587)  # Создаем объект SMTP
            server.starttls()  # Начинаем шифрованный обмен по TLS
            server.login(addr_from, password)  # Получаем доступ
            server.send_message(msg)  # Отправляем сообщение
            server.quit()  # Выходим
            print('\nОтправлено!\n')

print('\nРаботы программы завершена!')