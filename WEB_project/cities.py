# импорт библиотек
import json
import logging
from random import choice
from table_of_results import add_information

# импорт для яндекс карт
from geocoder import get_ll_span

# телеграм бот
from telegram.ext import CommandHandler, MessageHandler, filters

# логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


# приветсвие и старт игры
async def cities(update, context):
    await update.message.reply_text("Поиграем в города! Я начну")
    context.user_data['list_of_cities'] = ["Москва"]
    # показать Москву
    ll, spn = await get_ll_span("Москва")
    if ll and spn:
        point = "{ll},pm2vvl".format(ll=ll)
        static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map&pt={point}"
        await context.bot.sendPhoto(update.message.chat.id, static_api_request,
                                    caption="Москва")
    await update.message.reply_text("Напишите 'заново', чтобы начать игру сначала.")
    await update.message.reply_text("Напишите 'помощь', чтобы я сделал ещё один ход.")


# ход игры
async def geocoder(update, context):
    try:
        # выгружаем словарь городов
        with open('list_of_cities.json') as file:
            dictionary_of_cities = json.load(file)
        # сообщение пользователя
        mes = update.message
        new_city = mes.text.capitalize()
        # проверка на начало заново
        if "заново" in new_city.lower():
            context.user_data['list_of_cities'] = ["Москва"]
        # помощь бота
        elif "помощь" in new_city.lower():

            # поиск последней подходящей буквы
            last_possible_letter = -1
            while context.user_data['list_of_cities'][-1][last_possible_letter:][0] in 'ъьыё':
                last_possible_letter -= 1
            last_possible_letter = context.user_data['list_of_cities'][-1][last_possible_letter:][0].upper()

            # список возможных новых городов
            set_of_possible_cities = set(dictionary_of_cities[last_possible_letter]) - set(
                context.user_data['list_of_cities'])

            # окончание игры
            if len(set_of_possible_cities) == 0:
                await update.message.reply_text("Не могу придумать город, начните игру заново.")

            else:
                # выбор города
                new_city = choice(list(set_of_possible_cities))
                help_list = context.user_data.get('list_of_cities', [])
                # добавление города в список, чтобы избежать повторений
                help_list.append(new_city)
                context.user_data['list_of_cities'] = help_list

                # показ карты города
                ll, spn = await get_ll_span(new_city)
                if ll and spn:
                    point = "{ll},pm2vvl".format(ll=ll)
                    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map&pt={point}"
                    await context.bot.sendPhoto(update.message.chat.id, static_api_request,
                                                caption=new_city)
                else:
                    # без карты
                    await update.message.reply_text(f"Увы, но в этот раз без карты. Город:{new_city}")
        elif new_city not in dictionary_of_cities[new_city[0].upper()]:
            # ложный город (введён бред)
            await update.message.reply_text("Такого города не существует.")
        else:

            # проверка последней буквы
            last_city = context.user_data['list_of_cities'][-1]
            letter_for_user = -1
            while last_city[letter_for_user:][0] in 'ъьыё':
                letter_for_user -= 1
            letter_for_user = last_city[letter_for_user:][0].upper()
            if letter_for_user != new_city[0]:
                await update.message.reply_text("Не та первая буква.")
                await update.message.reply_text(f"Вам нужна: {letter_for_user.capitalize()}.")

            else:
                help_list = context.user_data.get('list_of_cities', [])
                # проверка повтора города
                if new_city in help_list:
                    await update.message.reply_text("Такой город уже был.")
                else:
                    # добавление города
                    help_list.append(new_city)
                    context.user_data['list_of_cities'] = help_list
                    add_information(mes.from_user.username, add_city=True)

                    # карта города
                    ll, spn = await get_ll_span(new_city)
                    if ll and spn:
                        point = "{ll},pm2vvl".format(ll=ll)
                        static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map&pt={point}"
                        await context.bot.sendPhoto(update.message.chat.id, static_api_request,
                                                    caption=update.message.text.capitalize())
                    else:
                        await update.message.reply_text(
                            f"Увы, но в этот раз без карты. Город:{update.message.text.capitalize()}")

                    # ответ бота
                    # последняя возможная буква
                    last_possible_letter = -1
                    while new_city[last_possible_letter:][0] in 'ъьыё':
                        last_possible_letter -= 1
                    last_possible_letter = new_city[last_possible_letter:][0].upper()
                    set_of_possible_cities = set(dictionary_of_cities[last_possible_letter]) - set(
                        context.user_data['list_of_cities'])

                    # начать заново
                    if len(set_of_possible_cities) == 0:
                        await update.message.reply_text("Не могу придумать город, начните игру заново.")
                    else:

                        # добавление города
                        new_city = choice(list(set_of_possible_cities))
                        help_list = context.user_data.get('list_of_cities', [])
                        help_list.append(new_city)
                        context.user_data['list_of_cities'] = help_list

                        #показ карты
                        ll, spn = await get_ll_span(new_city)
                        if ll and spn:
                            point = "{ll},pm2vvl".format(ll=ll)
                            static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map&pt={point}"
                            await context.bot.sendPhoto(update.message.chat.id, static_api_request,
                                                        caption=new_city)
                        else:
                            await update.message.reply_text(
                                f"Увы, но в этот раз без карты. Город:{new_city}")
    except RuntimeError as ex:
        await update.message.reply_text(str(ex))


# подключение городов
def main_cities(application):
    application.add_handler(CommandHandler("cities", cities))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, geocoder))
