# подключение библиотек
import pip

pip.main(['install', 'pytelegrambotapi', "requests", "python-telegram-bot", "flask"])

# импорт других частей кода
from funny_pictures import *
from cities import *
from table_of_results import get_info

# токен бота
from Bot_Token import TOKEN

# логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

# клавиатура начального меню
base_keyboard = [['/cities', '/funny_pictures', '/results']]
base_markup = ReplyKeyboardMarkup(base_keyboard, one_time_keyboard=False)


# старт: описание, что можно делать
async def start(update, context):
    await update.message.reply_text("Привет! Чем бы Вы хотели заняться?")
    # подключение клавиатуры
    await update.message.reply_text(
        "/cities: играть в города, /funny_pictures: смотреть картинки, /results: увидеть самых активных пользователей",
        reply_markup=base_markup)


# показ результатов
async def results(update, context):
    # получение информации
    winner_lists = get_info()

    await update.message.reply_text("Самые активные пользователи:")

    # вывод информации
    output = []
    for user in winner_lists:
        output.append(user[0])

    # печать результатов
    await update.message.reply_text("\n".join(output))


# подключение функций
def main():
    # подключение бота
    application = Application.builder().token(TOKEN).build()

    # старт и результаты
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("results", results))

    # подключение городов
    main_cities(application)

    # подключение картинок
    main_funny_pictures(application)

    application.run_polling()
    bot.polling()


# главная функция
if __name__ == '__main__':
    main()
