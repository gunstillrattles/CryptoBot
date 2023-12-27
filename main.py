import telebot
from telebot import types
import functions
from data import descriptions, descriptions_exchanges
import time

bot = telebot.TeleBot('6805721763:AAEbH1hqqQOdimh9pyw79zZHVzo5nFpEXP4')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     f"""🚀 Добро пожаловать {message.from_user.username}  в CryptoBot! 🚀

📊 Мои услуги включают:
- Технический анализ криптовалют, бирж, рынка.
- Уведомления о важных событиях и трендах.
- Разные дополнительные функции

📈 Готовы начать? Просто выберите нужную опцию из меню, и мы начнем!

🌐 Для получения дополнительной информации по командам введите /help.

Удачных инвестиций! 💹""")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Список доступных команд💪:\n"
                                      "/coins -   Выводит всю информацию об интересующей вас криптовалюте\n"
                                      "/changes - Узнайте на сколько поменялась ваша криптовалюта за выбранное вами время\n"
                                      "/history - Узнайте сколько стоило криптовалюта в любой день\n"
                                      "/trending - Самые частые криптовалюты которые пользователи искали сегодня\n"
                                      "/exchanges - Топ самых лучших и распространенных бирж на данный момент\n"
                                      "/categories - Самые распространенные категории и какие криптовалюты к ним относятся\n"
                     )


def send_time_keyboard(message, coin_id):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('1 hour ⌚', callback_data=f'1h {coin_id}')
    btn2 = types.InlineKeyboardButton('1 day ⌚', callback_data=f'24h {coin_id}')
    markup.row(btn1, btn2)
    btn3 = types.InlineKeyboardButton('1 week ⌚', callback_data=f'7d {coin_id}')
    btn4 = types.InlineKeyboardButton('1 month ⌚', callback_data=f'1m {coin_id}')
    markup.row(btn3, btn4)
    btn5 = types.InlineKeyboardButton('1 year ⌚', callback_data=f'1y {coin_id}')
    markup.row(btn5)
    bot.reply_to(message, "Выберите интересующий вас период времени⏰:", reply_markup=markup)


@bot.message_handler(commands=['changes'])
def changes(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Bitcoin 💸', callback_data='bitcoin_changes')
    btn2 = types.InlineKeyboardButton('Ethereum 💸', callback_data='ethereum_changes')
    markup.row(btn1, btn2)
    btn3 = types.InlineKeyboardButton('Binance Coin 💸', callback_data='binance_changes')
    btn4 = types.InlineKeyboardButton('Solana 💸', callback_data='solana_changes')
    markup.row(btn3, btn4)
    btn5 = types.InlineKeyboardButton('Cardano 💸', callback_data='cardano_changes')
    btn6 = types.InlineKeyboardButton('Ripple 💸', callback_data='ripple_changes')
    markup.row(btn5, btn6)
    bot.reply_to(message, "Выберите интересующую вас криптовалюту💰:", reply_markup=markup)


@bot.message_handler(commands=['coins'])
def coins(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Bitcoin 💸', callback_data='bitcoin')
    btn2 = types.InlineKeyboardButton('Ethereum 💸', callback_data='ethereum')
    markup.row(btn1, btn2)
    btn3 = types.InlineKeyboardButton('Binance Coin 💸', callback_data='binance')
    btn4 = types.InlineKeyboardButton('Solana 💸', callback_data='solana')
    markup.row(btn3, btn4)
    btn5 = types.InlineKeyboardButton('Cardano 💸', callback_data='cardano')
    btn6 = types.InlineKeyboardButton('Ripple 💸', callback_data='ripple')
    markup.row(btn5, btn6)
    bot.reply_to(message, "Выберите интересующую вас криптовалюту💰:", reply_markup=markup)


@bot.message_handler(commands=['history'])
def history(message):
    message_parts = message.text.split()
    if len(message_parts) < 3:
        bot.reply_to(message,
                     "Пожалуйста, укажите название криптовалюты💰 и дату в формате дд-мм-гггг📅, например:\n"
                     "Bitcoin: /history bitcoin ДД-ММ-ГГГГ\n"
                     "Ethereum: /history ethereum ДД-ММ-ГГГГ\n"
                     "Binance Coin: /history binance coin ДД-ММ-ГГГГ\n"
                     "Solana: /history solana ДД-ММ-ГГГГ\n"
                     "Cardano: /history cardano ДД-ММ-ГГГГ\n"
                     "Ripple: /history ripple ДД-ММ-ГГГГ")
        return
    coin_id = message_parts[1]
    date = message_parts[2]
    data = functions.get_cryptocurrency_history(coin_id, date)

    historical_price = data.get('market_data', {}).get('current_price', {}).get('usd')

    if historical_price:
        rounded_price = round(float(historical_price), 2)
        bot.reply_to(message, f"Историческая цена для {coin_id} на {date}: {rounded_price}$ долларов США🤑")
    else:
        bot.reply_to(message, f"Цены на {date} не существует🥲")


@bot.message_handler(commands=['trending'])
def trending(message):
    data = functions.get_trending_coins()
    bot.send_message(message.chat.id, "Это топ криптовалют которые пользователи чаще всего искали за 24 часа‼️: ")
    for i in data:
        description = i['content']['description'] if i['content'] is not None else ""
        bot.send_message(message.chat.id,
                         f"Название💹: {i['name']}\n"
                         f"Иконка: {i['large']}\n"
                         f"Цена💸: {i['price']}\n"
                         f"Изменение цены (за 24 часа)⏳: {round(float(i['price_change_percentage_24h']), 2)}% \n"
                         f"График изменения цены📈: {i['sparkline']}\n"
                         f"{description}", parse_mode='html')
        time.sleep(5)


@bot.message_handler(commands=['categories'])
def categories(message):
    data = functions.get_top_categories()
    bot.send_message(message.chat.id, "Это топ самых распространенных категорий✅: ")
    for i in data:
        bot.send_message(message.chat.id,
                         f"Название: {i['name']}\n"
                         f"Рыночная капитализация💵: {i['market_cap']}$ \n"
                         f"Топ криптовалют которые относятся к этой категории {', '.join(i['top_3_coins'])}",
                         parse_mode='html')
        time.sleep(5)


@bot.message_handler(commands=['exchanges'])
def exchanges(message):
    data = functions.get_top_exchanges()
    bot.send_message(message.chat.id, "Вот топ самых популярных и доверенных бирж✅: ")
    length = 0
    for i in data:
        info = f"Название: {i['name']}\n"
        if i['year_established']:
            info += f"Год основания📆: {i['year_established']}\n"
        if i['country']:
            info += f"Страна🌍: {i['country']}\n"
        info += f"Ссылка: {i['url']}\n"
        info += f"Уровень доверия👍: {i['trust_score']}\n"
        info += f"Рейтинг уровня доверия📒: {i['trust_score_rank']}\n"
        info += f"Торговый объем за 24 часа (в BTC)⏰: {i['trade_volume_24h_btc']}\n\n"
        info += f"{descriptions_exchanges[length]}"
        length += 1

        bot.send_message(message.chat.id, info, parse_mode='html')
        time.sleep(5)


@bot.message_handler()
def base(message):
    bot.reply_to(message, """Извините, но я не понимаю, что вы пишите.😔
Введите, пожалуйста, команду из списка доступных команд. /help """)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'bitcoin':
        data = functions.get_coin_info_func("bitcoin")
        bot.send_message(callback.message.chat.id, f""" 
{data["name"]} , сокращенно {data["symbol"]} {f'использует алгоритм хэширования {data["hashing_algorithm"]}' if data["hashing_algorithm"] != None else ''}

И относится к следующим категориям {', '.join(data["categories"])}

Официальный сайт криптовалюты {data["linksh"]}

Blochain сайты {data["links1"]}, {data["links2"]}, {data["links3"]}. 
{f'Дата основания {data["genesis_date"]}' if data["genesis_date"] != None else ''} и текущая цена на рынке {data["current_price"]}$
Текущий обьем рынка {data["market_cap"]}$  

Описание:
{descriptions["bitcoin"]}""", parse_mode="html")

    elif callback.data == 'ethereum':
        data = functions.get_coin_info_func("ethereum")
        bot.send_message(callback.message.chat.id, f""" 
{data["name"]} , сокращенно {data["symbol"]} {f'использует алгоритм хэширования {data["hashing_algorithm"]}' if data["hashing_algorithm"] != None else ''}

И относится к следующим категориям {', '.join(data["categories"])}

Официальный сайт криптовалюты {data["linksh"]}

Blochain сайты {data["links1"]}, {data["links2"]}, {data["links3"]}. 
{f'Дата основания {data["genesis_date"]}' if data["genesis_date"] != None else ''} и текущая цена на рынке {data["current_price"]}$
Текущий обьем рынка {data["market_cap"]}$

Описание:
{descriptions["ethereum"]}   
""", parse_mode="html")

    elif callback.data == 'binance':
        data = functions.get_coin_info_func("binancecoin")
        bot.send_message(callback.message.chat.id, f""" 
{data["name"]} , сокращенно {data["symbol"]} {f'использует алгоритм хэширования {data["hashing_algorithm"]}' if data["hashing_algorithm"] != None else ''}

И относится к следующим категориям {', '.join(data["categories"])}

Официальный сайт криптовалюты {data["linksh"]}

Blochain сайты {data["links1"]}, {data["links2"]}, {data["links3"]}. 
{f'Дата основания {data["genesis_date"]}' if data["genesis_date"] != None else ''} и текущая цена на рынке {data["current_price"]}$
Текущий обьем рынка {data["market_cap"]}$    

Описание:
{descriptions["binance"]} """, parse_mode="html")

    elif callback.data == 'solana':
        data = functions.get_coin_info_func("solana")
        bot.send_message(callback.message.chat.id, f""" 
{data["name"]} , сокращенно {data["symbol"]} {f'использует алгоритм хэширования {data["hashing_algorithm"]}' if data["hashing_algorithm"] != None else ''}

И относится к следующим категориям {', '.join(data["categories"])}

Официальный сайт криптовалюты {data["linksh"]}

Blochain сайты {data["links1"]}, {data["links2"]}, {data["links3"]}. 
{f'Дата основания {data["genesis_date"]}' if data["genesis_date"] != None else ''} и текущая цена на рынке {data["current_price"]}$
Текущий обьем рынка {data["market_cap"]}$

Описание:
{descriptions["solana"]}       
""", parse_mode="html")

    elif callback.data == 'cardano':
        data = functions.get_coin_info_func("cardano")
        bot.send_message(callback.message.chat.id, f""" 
{data["name"]} , сокращенно {data["symbol"]} {f'использует алгоритм хэширования {data["hashing_algorithm"]}' if data["hashing_algorithm"] != None else ''}

И относится к следующим категориям {', '.join(data["categories"])}

Официальный сайт криптовалюты {data["linksh"]}

Blochain сайты {data["links1"]}, {data["links2"]}, {data["links3"]}. 
{f'Дата основания {data["genesis_date"]}' if data["genesis_date"] != None else ''} и текущая цена на рынке {data["current_price"]}$
Текущий обьем рынка {data["market_cap"]}$   

Описание:
{descriptions["cardano"]}     
""", parse_mode="html")

    elif callback.data == 'ripple':
        data = functions.get_coin_info_func("ripple")
        bot.send_message(callback.message.chat.id, f""" 
{data["name"]} , сокращенно {data["symbol"]} {f'использует алгоритм хэширования {data["hashing_algorithm"]}' if data["hashing_algorithm"] != None else ''}

И относится к следующим категориям {', '.join(data["categories"])}

Официальный сайт криптовалюты {data["linksh"]}

Blochain сайты {data["links1"]}, {data["links2"]}, {data["links3"]}. 
{f'Дата основания {data["genesis_date"]}' if data["genesis_date"] != None else ''} и текущая цена на рынке {data["current_price"]}$
Текущий обьем рынка {data["market_cap"]}$

Описание:
{descriptions["ripple"]}       
""", parse_mode="html")
    elif callback.data == "bitcoin_changes":
        send_time_keyboard(callback.message, "bitcoin")
    elif callback.data == "ethereum_changes":
        send_time_keyboard(callback.message, "ethereum")
    elif callback.data == "binance_changes":
        send_time_keyboard(callback.message, "binancecoin")
    elif callback.data == "solana_changes":
        send_time_keyboard(callback.message, "solana")
    elif callback.data == "cardano_changes":
        send_time_keyboard(callback.message, "cardano")
    elif callback.data == "ripple_changes":
        send_time_keyboard(callback.message, "ripple")
    else:
        array = callback.data.split()
        time = array[0]
        coin_id = array[1]
        if time == "1h":
            price = functions.get_current_price("1h", coin_id)
            bot.send_message(callback.message.chat.id, f"{coin_id} за 1 час изменился на {price[0]}% 📈")
        elif time == "24h":
            price = functions.get_current_price("24h", coin_id)
            bot.send_message(callback.message.chat.id,
                             f"{coin_id} за 24 часа изменился на {price[1]}%, это {price[0]}$ 📈")
        elif time == "7d":
            price = functions.get_current_price("7d", coin_id)
            bot.send_message(callback.message.chat.id, f"{coin_id} за 1 неделю изменился на {price[0]}% 📈")
        elif time == "1m":
            price = functions.get_current_price("1m", coin_id)
            bot.send_message(callback.message.chat.id, f"{coin_id} за 1 месяц изменился на {price[0]}% 📈")
        elif time == "1y":
            price = functions.get_current_price("1y", coin_id)
            bot.send_message(callback.message.chat.id, f"{coin_id} за 1 год изменился на {price[0]}% 📈")


bot.polling(none_stop=True)
