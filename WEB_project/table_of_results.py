# ипмпортируем билиотеку для работы с таблицами
import csv


# получение таблицы результатов
def get_info():
    winner_list = []
    # открытие файла
    with open('results.csv', "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        # проход по пользователям
        for user in reader:
            nickname = user[0]
            cities = int(user[1])
            pictures = int(user[2])
            # сохранение результатов в программе
            winner_list.append([nickname, cities + pictures])
    # сортировка
    winner_list = sorted(winner_list, key=lambda x: x[1])
    return winner_list[:3]


# обновление таблицы результатов
def add_information(user_nick, add_city=False, add_picture=False):
    # переменная, следящая есть ли пользователь в таблице или нет
    add = False
    new_table = []
    # открытие файла
    with open('results.csv', "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        # проход по пользователями
        for user in reader:
            nickname = user[0]
            cities = int(user[1])
            pictures = int(user[2])
            # если пользовтаель был, то увеличение данных
            if nickname == user_nick:
                add = True
                if add_city:
                    cities += 1
                if add_picture:
                    pictures += 1
            # добавление пользователя в таблицу
            new_table.append([nickname, cities, pictures])
    # если пользовтеля не было
    if not add:
        cities = 0
        pictures = 0
        if add_city:
            cities += 1
        if add_picture:
            pictures += 1
        # добавление нового пользователя
        new_table.append([user_nick, cities, pictures])

    # запись результата
    with open('results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(
            csvfile, delimiter=';', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
        for user in new_table:
            writer.writerow(user)
