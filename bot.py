import os
import telebot
import random
from flask import Flask, request
import consts
from db import DB

bot = telebot.TeleBot(consts.BOT_TOKEN)
app = Flask(__name__)
db = DB()


# --------------------COMANDI--------------------

@bot.message_handler(commands=['start'])
def start(message):
    db.setChatStatus(message.chat.id, True)
    bot.reply_to(message, 'On')


@bot.message_handler(commands=['status'])
def status(message):
    enabled = 'on' if db.getChatStatus(message.chat.id) else 'off'
    prob = db.getRate(message.chat.id) * 100.0
    bot.reply_to(message, '*Stato*: {}\n*Probabilità risposta*: {}%'.format(enabled, prob), parse_mode="MARKDOWN")


@bot.message_handler(commands=['stop'])
def stop(message):
    db.setChatStatus(message.chat.id, False)
    bot.reply_to(message, 'Off')


@bot.message_handler(commands=['id'])
def user_id(message):
    if message.reply_to_message.from_user.id is not None:
        bot.reply_to(message, message.reply_to_message.from_user.id)
    else:
        bot.reply_to(message, "Devi citare un messaggio")


@bot.message_handler(commands=['whoami'])
def whoami(message):
    bot.reply_to(message, message.chat.id)


@bot.message_handler(commands=['info'])
def info(message):
    bot.reply_to(message, 'By @davide99 & @AndreaFelipe')


@bot.message_handler(commands=['wasabi'])
def wasabi(message):
    bot.send_photo(message.chat.id, 'AgADBAADvLUxG8D9OwJmOy4zQ-z9LnxCKRkABM79MKc4wySEgz4CAAEC',
                   reply_to_message_id=message.message_id)


@bot.message_handler(commands=['ban'])
def ban(message):
    if message.reply_to_message.from_user.id is not None:
        bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    else:
        bot.reply_to(message, "Devi citare un messaggio dell'utente da bannare")


@bot.message_handler(commands=['rate'])
def rate(message):
    try:
        val = float(message.text.split()[1].replace(',', '.'))

        if val > 1:
            val /= 100.0

        if val <= 1:
            db.setRate(message.chat.id, val)
            bot.reply_to(message, 'Probabilità di risposta settata su {}%'.format(val * 100))
        else:
            raise ValueError
    except (IndexError, ValueError):
        bot.reply_to(message, "Errore, valore non valido")


# -----------MESSAGGI SENZA RATE------------

@bot.message_handler(func=lambda message: message.text.lower().startswith('pippi dice'), content_types=['text'])
def pippi_dice(message):
    bot.send_message(message.chat.id, message.text[11:])


# -----------MESSAGGI CON RATE--------------


@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_with_rate(message):
    if random.uniform(0, 1) > db.getRate(message.chat.id) or not db.getChatStatus(message.chat.id):
        return

    msg = message.text.lower()

    if 'chi' in msg and 'sei' in msg:
        bot.reply_to(message, 'Io sono Pippi u elettrotecnicu 👋')
    elif 'man' in msg and 'ag' in msg and 'gia' in msg:
        bot.reply_to(message, 'Mannaggia a te')
    elif 'rotto' in msg and ('cazzo' in msg or 'palle' in msg or 'coglioni' in msg):
        bot.reply_to(message, 'Nemmeno Skyler rompeva così')
    elif 'cazz' in msg:
        bot.reply_to(message, 'Hai tittu cazzu?')
    elif 'non hai visto niente' in msg or ('sh' in msg and 'ss' in msg):
        bot.send_document(message.chat.id, 'BQADBAADNAMAAoYeZAd25LnwZcUYdQI', reply_to_message_id=message.message_id)
    elif 'anime' in msg:
        bot.reply_to(message, 'Si chiamano cartoni animati giapponesi')
    elif 'scaric' in msg and ('tel' in msg or 'cel' in msg):
        bot.reply_to(message, 'Ovvio che è scarico, è un iPhone')
    elif 'non so' in msg or 'non lo so' in msg or 'che ne so' in msg:
        bot.reply_to(message, 'Chiedi a Steve Jobs 😷')
    elif 'walt' in msg or 'heisenberg' in msg:
        bot.reply_to(message, 'Tanto non è morto❗')
    elif 'uomo' in msg:
        bot.reply_to(message, 'Siniora c\'è un womo pellei')
    elif 'zitto' in msg:
        bot.reply_to(message, 'Si siniora')
    elif 'wow' in msg and 'renna' in msg:
        bot.reply_to(message, 'Wow quella renna parla! 😱')
    elif 'buongiorno' in msg:
        bot.reply_to(message, 'Era 😡')
    elif 'apple' in msg:
        bot.reply_to(message, 'Mele di merda!')
    elif 'spacobot' in msg:
        bot.reply_to(message, 'Spacobot di merda!')
    elif 'euh' in msg:
        bot.reply_to(message, 'Euh 😰')
    elif 'fox' in msg:
        bot.reply_to(message, 'Ring ding ding ding dingeringeding 🐺')
    elif 'ah' in msg and 'ha' in msg:
        bot.reply_to(message, 'Cazzo ti ridi? 😒')
    elif 'video' in msg:
        bot.reply_to(message, 'Bravoh')
    elif 'pippi' in msg:
        bot.reply_to(message, 'Giovane... vai fuori!')
    elif 'ricchion' in msg or 'gay' in msg:
        bot.reply_to(message, 'Mi avete chiamato?')
    elif 'ciao' in msg:
        bot.reply_to(message, 'Buongina')
    elif 'colion' in msg or 'giuliv' in msg:
        bot.reply_to(message, 'Ma tu mi sembri un po\' colione')
    elif 'aah' in msg:
        if len(msg.replace('a', '').replace('h', '')) == 0:
            bot.reply_to(message, 'Cazzo ti esclami? 😒')
    elif 'funziona' in msg:
        bot.reply_to(message, 'E cettu che funziona')
    elif 'good' in msg:
        bot.reply_to(message, 'Maleducato che sei')
    elif 'cittu' in msg:
        opts = ["merda", "minchia", "incintu", "lezzu", "ttau", "pippi", "cittu", "shrek", "fessa"]
        bot.reply_to(message, 'Cittu ' + random.choice(opts))
    elif 'bacino' in msg:
        bot.reply_to(message, 'In privato')
    elif 'genius' in msg:
        bot.reply_to(message, 'I\'m a fucking genius bitch! 😎')
    elif 'eh' in msg and 'he' in msg:
        if len(msg.replace('e', '').replace('h', '')) == 0:
            bot.reply_to(message, 'Figlio di babbano 😏')
    elif 'say my name' in msg:
        bot.reply_to(message, 'I\'m Heisenberg 🔫')
    elif 'pene' in msg:
        bot.reply_to(message, 'Cacacacacacacacaca')
    elif 'who' in msg and 'are' in msg and 'you' in msg:
        bot.reply_to(message, 'I\'m the one who knocks 🚪')
    elif 'bast' in msg:
        bot.reply_to(message, 'st\nst\nst\nst\nst\nst')
    elif 'lezz' in msg:
        bot.reply_to(message, 'You are lezzo')
    elif 'san' in msg:
        bot.reply_to(message, 'San ' + message.from_user.first_name)
    elif 'futtitene' in msg:
        bot.reply_to(message, 'Tie te n\'hai FUTTIRE')
    elif 'matematica' in msg:
        bot.reply_to(message, 'A matematica quiddha ete')
    elif 'simo' in msg:
        bot.reply_to(message, 'Va fanne sicchi')
    elif 'non è' in msg or 'non é' in msg:
        bot.reply_to(message, 'Quello che non è')
    elif 'sono tutti' in msg:
        bot.reply_to(message, 'Ma di diverse categorie')
    elif 'spieg' in msg:
        bot.reply_to(message, 'Non fare mansplanning!')
    elif 'non ci sono' in msg:
        bot.reply_to(message, 'Succube.')


@app.route('/' + consts.BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=consts.APP_URL + consts.BOT_TOKEN)
    return "!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
