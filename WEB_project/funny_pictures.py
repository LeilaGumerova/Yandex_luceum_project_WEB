# подключение библиотек для бота
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import telebot

# токен бота
from Bot_Token import TOKEN

# вспомотаельные в программе библиотеки
import random
import logging
import os

# импорт части кода, для обновления результатов
from table_of_results import add_information

# бот
bot = telebot.TeleBot(TOKEN, parse_mode='html')

# логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

# подключение клавиатур
base_pictures_keyboard = [['/cats', '/dogs', '/others', '/add']]  # основная
add_pictures_keyboard = [['/add_cat', '/add_dog', '/add_other', '/back']]  # для добавления картинок
cat_keyboard = [['/next_cat', '/back']]  # для котов
dog_keyboard = [['/next_dog', '/back']]  # для обак
other_keyboard = [['/next_other', '/back']]  # для других

base_pictures_markup = ReplyKeyboardMarkup(base_pictures_keyboard, one_time_keyboard=False)
add_pictures_markup = ReplyKeyboardMarkup(add_pictures_keyboard, one_time_keyboard=False)
cat_markup = ReplyKeyboardMarkup(cat_keyboard, one_time_keyboard=False)
dog_markup = ReplyKeyboardMarkup(dog_keyboard, one_time_keyboard=False)
other_markup = ReplyKeyboardMarkup(other_keyboard, one_time_keyboard=False)


# случайная картинка из папки
def choice_picture(folder):
    os.chdir(f"memes/{folder}")
    chosen = random.choice(os.listdir())
    return chosen


# добавление картинки в папку
def add_picture(folder, picture):
    os.chdir(f"memes/{folder}")
    new_name = f"{folder[:-1]} ({max([int(el[el.index('(') + 1:el.index(')')]) for el in os.listdir()]) + 1})" + ".jpg"
    with open(new_name, 'wb') as new_file:
        new_file.write(picture)


# возврат в корневую папку
def return_to_folder():
    way = os.getcwd()
    for_return = '\\'.join(str(way).split("\\")[:-2])
    os.chdir(for_return)


# начальное приветствие
async def funny_pictures(update, context):
    # если категория не задана, то добавляется к другим
    context.user_data['category'] = 'other'

    # ввывод приветствия
    await update.message.reply_text('Привет! Пошли смотреть классные картинки!')
    await update.message.reply_text(
        "/cats: про котиков, /dogs: про собачек, /other: другие, /add: добавить свою картинку",
        reply_markup=base_pictures_markup)


# картинки кошек
async def cats(update, context):
    # выводимая картинка
    picture = choice_picture("cats")
    # вывод картинок
    await context.bot.sendPhoto(update.message.chat.id, picture)
    # возврат в папку, из папки, в которую зашли при выборе картинки
    return_to_folder()
    # клавиатура
    await update.message.reply_text("/next_cat: следующая, /back: вернуться к меню",
                                    reply_markup=cat_markup)


# картинки собак
async def dogs(update, context):
    # выводимая картинка
    picture = choice_picture("dogs")
    # вывод картинок
    await context.bot.sendPhoto(update.message.chat.id, picture)
    # возврат в папку, из папки, в которую зашли при выборе картинки
    return_to_folder()
    # клавиатура
    await update.message.reply_text("/next_dog: следующая, /back: вернуться к меню",
                                    reply_markup=dog_markup)


# картинки не кошек и не собак
async def others(update, context):
    # выводимая картинка
    picture = choice_picture("others")
    # вывод картинок
    await context.bot.sendPhoto(update.message.chat.id, picture)
    # возврат в папку, из папки, в которую зашли при выборе картинки
    return_to_folder()
    # клавиатура
    await update.message.reply_text("/next_other: следующая, /back: вернуться к меню",
                                    reply_markup=other_markup)


# добавить картинку
async def add(update, context):
    # если категория не выбрана, то в другие
    context.user_data['category'] = 'others'
    # инструкция по добавлению картинки
    await update.message.reply_text("Выберите категорию")
    await update.message.reply_text("Затем отправьте картинку")
    # клавиатура
    await update.message.reply_text("/add_cat: котики, /add_dog: собачки, /add_other: другие, /back: вернуться к меню",
                                    reply_markup=add_pictures_markup)


# добавляем к кошкам
async def add_cat(update, context):
    context.user_data['category'] = 'cats'


# добавляем к собакам
async def add_dog(update, context):
    context.user_data['category'] = 'dogs'


# добавляем к другим
async def add_other(update, context):
    context.user_data['category'] = 'others'


# добавляем фото
async def add_photo(update, context):
    # сообщение
    mes = update.message
    # фото
    fileID = mes.photo[-1].file_id
    file_info = bot.get_file(fileID)
    # сохранить фото
    downloaded_file = bot.download_file(file_info.file_path)
    # добавляем картинку
    add_picture(context.user_data['category'], downloaded_file)
    # возвращение в корневую папку
    return_to_folder()
    # обновление активности пользователя
    add_information(mes.from_user.username, add_picture=True)


# подключение боту комманд
def main_funny_pictures(application):
    # приветствие
    application.add_handler(CommandHandler("funny_pictures", funny_pictures))

    # картинка кота
    application.add_handler(CommandHandler("cats", cats))
    application.add_handler(CommandHandler("next_cat", cats))

    # картинка собаки
    application.add_handler(CommandHandler("dogs", dogs))
    application.add_handler(CommandHandler("next_dog", dogs))

    # другая картинка
    application.add_handler(CommandHandler("others", others))
    application.add_handler(CommandHandler("next_other", others))

    # вернуться
    application.add_handler(CommandHandler("back", funny_pictures))

    # добавление картинки
    application.add_handler(CommandHandler("add", add))

    # выбор какой картинки
    application.add_handler(CommandHandler("add_cat", add_cat))
    application.add_handler(CommandHandler("add_dog", add_dog))
    application.add_handler(CommandHandler("add_other", add_other))

    # собственно добавление фото
    photo_handler = MessageHandler(filters.PHOTO, add_photo)
    application.add_handler(photo_handler)
