import telebot
import config
import webbrowser
from telebot import types

bot = telebot.TeleBot(config.token)

#Клавиши на уровне модуля
item1 = types.KeyboardButton('análogos')
item2 = types.KeyboardButton('conjugación')
item3 = types.KeyboardButton('declinación')
item4 = types.KeyboardButton('pronunciación')

def analizar_palabra(palabra): #словарь аналогов
    analogías = {
        'а': ('a', 'Argentina'),
        'б': ('b', 'Barbara'),
        'в': ('v', 'Valencia'),
        'г': ('g', 'gota'),
        'д': ('d', 'dormir'),
        'е': ('e', 'leche'),
        'ё': ('llo', 'llorar'),
        'ж': ('zh', 'zh'),
        'з': ('z', 'zona (con más fuerte)'),
        'и': ('i', 'Sonrisa'),
        'й': ('ll', 'brillar'),
        'к': ('c/k', 'cola'),
        'л': ('l', 'Lola'),
        'м': ('m', 'madre'),
        'н': ('n', 'nosotros'),
        'о': ('o', 'Lola'),
        'п': ('p', 'padre'),
        'р': ('r', 'Rosa'),
        'с': ('c', 'Sevilla'),
        'т': ('t', 'tortilla'),
        'у': ('u', 'Usted'),
        'ф': ('f', 'Favorito'),
        'х': ('j', 'José (con menos fuerte)'),
        'ц': ('ts', 'Cesar (con más aspiración)'),
        'ч': ('che', 'Che'),
        'ш': ('sh', 'Sasha'),
        'щ': ('sch', 'sch'),
        'ь': ('suavidad del sonido', 'pronuncie el sonido consonante anterior lo más suavemente posible'),
        'ъ': ('un sonido fuerte', 'agregue el separador [ll] como en lleno después de la próxima consonante'),
        'ы': ('[yi]', 'no hay análogos, diga u como en usted y relaje los labios'),
        'э': ('e', 'Europa'),
        'ю': ('llu', 'lluvia'),
        'я': ('lla', 'llamada')
    }

    url = f'https://context.reverso.net/%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4/%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9-%D0%B8%D1%81%D0%BF%D0%B0%D0%BD%D1%81%D0%BA%D0%B8%D0%B9/{palabra}'
    webbrowser.open(url)
#Строка webbrowser.open(url) принимает URL (веб-адрес) в качестве входных данных и запускает этот URL в браузере пользователя. Это позволяет боту взаимодействовать с внешними веб-сайтами
    resultado = "Los sonidos y sus análogos en Español:\n\n"
    resultado += f"{'La letra rusa':<15} {'La letra parecida en Español':<15} {'Un ejemplo en Español':<30}\n"
    resultado += "-" * 60 + "\n"

    for letra in palabra.lower():
        if letra in analogías:
            español_análogo, ejemplo = analogías[letra]
            resultado += f"{letra:<15} {español_análogo:<15} {ejemplo:<30}\n"

    resultado += "\nОбратите внимание, что произношение может варьироваться в зависимости от контекста. 😊"
    return resultado

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(item1, item2, item3, item4) 

    bot.send_message(message.chat.id, "Bienvenidos! Elija lo que necesita entre los botones:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'análogos')
def request_word(message):
    bot.send_message(message.chat.id, "Introduzca la palabra rusa для анализа:")
    bot.register_next_step_handler(message, process_word)

def process_word(message):
    palabra = message.text
    resultado_analisis = analizar_palabra(palabra)
    bot.send_message(message.chat.id, resultado_analisis)

@bot.message_handler(func=lambda message: message.text == 'conjugación')
def request_conjugation_word(message):
    bot.send_message(message.chat.id, "Introduzca el verbo ruso para conjugar:")
    bot.register_next_step_handler(message, open_conjugation_site)

def open_conjugation_site(message):
    verbo = message.text
    url = f"https://www.babla.ru/%D1%81%D0%BF%D1%80%D1%8F%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F/%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9/{verbo}?ysclid=mbtltv91v9278454031"
    webbrowser.open(url)
    bot.send_message(message.chat.id, f"Открываю сайт для спряжения глагола: {verbo}. ✍️")

@bot.message_handler(func=lambda message: message.text == 'declinación')
def request_declension_word(message):
    bot.send_message(message.chat.id, "Escriba un sustantivo o adjetivo para declinar:")
    bot.register_next_step_handler(message, open_declension_site)

def open_declension_site(message):
    sustantivo_o_adjetivo = message.text
    url = f"https://morpher.ru/Demo.aspx?ysclid=mburtf3v6q709603480&word={sustantivo_o_adjetivo}" 
    webbrowser.open(url)
    bot.send_message(message.chat.id, f"Открываю сайт для склонения слова: {sustantivo_o_adjetivo}. ✍️")

@bot.message_handler(func=lambda message: message.text == 'pronunciación')
def request_pronunciation_word(message):
    bot.send_message(message.chat.id, "Escriba la palabra для получения произношения:")
    bot.register_next_step_handler(message, open_pronunciation_site)

def open_pronunciation_site(message):
    palabra = message.text
    url = f"https://www.cambridge.org/ru/dictionary/english-russian/{palabra}"
    webbrowser.open(url)
    bot.send_message(message.chat.id, f"Vale, empezamos: {palabra}. 🔊")

@bot.message_handler(content_types=['text'])
def handle_unrecognized(message):
    bot.send_message(message.chat.id, "Vale, ¿qué hago con esa palabra? Elija lo que necesita между los кнопками.")

bot.polling(none_stop=True)
