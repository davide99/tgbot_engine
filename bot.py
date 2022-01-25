import os
import random

import telebot
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
    bot.reply_to(message, 'Bot di @steghold\nPowered by pippibot engine')


def is_admin(chat_id: int, user_id_: int) -> bool:
    return bot.get_chat_member(chat_id, user_id_).status in ['administrator', 'creator']


@bot.message_handler(commands=['ban'])
def ban(message):
    print("Is admin: {}".format(is_admin(message.chat.id, message.from_user.id)))
    if not is_admin(message.chat.id, message.from_user.id):
        print(2)
        bot.reply_to(message, "Devi essere amministratore")
        print(3)
        return
    else:
        print(4)
        bot.reply_to(message, "Sei amministratore")
        print(5)

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

@bot.message_handler(func=lambda message: message.text.lower().startswith('stego dice'), content_types=['text'])
def stego_dice(message):
    bot.send_message(message.chat.id, message.text[11:])


# -----------MESSAGGI CON RATE--------------


@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_with_rate(message):
    if not db.getChatStatus(message.chat.id):
        # Esco se non abilitato
        return

    if random.uniform(0, 1) < 0.2:
        bot.send_chat_action(message.chat.id, "typing")

    if random.uniform(0, 1) > db.getRate(message.chat.id):
        return

    msg = message.text.lower()

    if 'chi' in msg and 'sei' in msg:
        bot.reply_to(message, 'Io sono Stego, e tu? 👋')
    elif 'man' in msg and 'ag' in msg and 'gia' in msg:
        bot.reply_to(message, 'Mannaggia a te')
    elif 'cazz' in msg:
        bot.reply_to(message, 'Non dire cazzo')
    elif 'non hai visto niente' in msg or ('sh' in msg and 'ss' in msg):
        bot.send_document(message.chat.id, 'BQADBAADNAMAAoYeZAd25LnwZcUYdQI', reply_to_message_id=message.message_id)
    elif 'scaric' in msg and ('tel' in msg or 'cel' in msg):
        bot.reply_to(message, 'Usa la mia energia per caricarlo')
    elif 'non so' in msg or 'non lo so' in msg or 'che ne so' in msg:
        if random.uniform(0, 1) > 0.5:
            bot.reply_to(message, 'Chiedi a Satoshi Nakamoto')
        else:
            bot.reply_to(message, 'Chiedi a me')
    elif 'meteorit' in msg:
        bot.reply_to(message, 'Non mi piaccioni i meteoriti')
    elif 'asteroid' in msg:
        bot.reply_to(message, 'Non mi piaccioni gli asteroidi')
    elif 'buongiorno' in msg:
        bot.reply_to(message, 'Buongiorno a te')
    elif 'buonasera' in msg:
        bot.reply_to(message, 'Buonasera a te')
    elif 'bot' in msg:
        bot.reply_to(message, 'Non sono un robot!')
    elif 'ah' in msg and 'ha' in msg:
        bot.reply_to(message, 'Ride bene chi ride ultimo')
    elif 'video' in msg:
        bot.reply_to(message, 'Forse c\'è un nuovo video sul nostro canale youtube')
    elif 'stego' in msg:
        bot.reply_to(message, 'Mi avete chiamato?')
    elif 'ciao' in msg:
        bot.reply_to(message, 'Buongiorno')
    elif 'aah' in msg:
        if len(msg.replace('a', '').replace('h', '')) == 0:
            bot.reply_to(message, 'Aaaaaaaaaah')
    elif 'funziona' in msg:
        bot.reply_to(message, 'E certo che funziona')
    elif 'good' in msg:
        bot.reply_to(message, 'Not bad')
    elif 'NFT' in msg:
        bot.reply_to(message, 'Quanti NFT hai?')
    elif 'eh' in msg and 'he' in msg:
        if len(msg.replace('e', '').replace('h', '')) == 0:
            bot.reply_to(message, 'Eheheh, bella questa')
    elif 'who' in msg and 'are' in msg and 'you' in msg:
        bot.reply_to(message, 'I\'m Stego')
    elif 'crypto' in msg:
        if random.uniform(0, 1) > 0.5:
            bot.reply_to(message, 'Io sto holdando Algo')
        else:
            bot.reply_to(message, 'Mai sentito parlare di Algo')
    elif 'san' in msg:
        bot.reply_to(message, 'San Stego')
    elif 'fregare' in msg:
        bot.reply_to(message, 'Te ne devi fregare')
    elif 'matematica' in msg:
        bot.reply_to(message, 'La matematica purtroppo è quella')
    elif 'adri' in msg:
        bot.reply_to(message, 'ADRIANAAA')
    elif 'non è' in msg or 'non é' in msg:
        bot.reply_to(message, 'Quello che non è')
    elif 'sono tutti' in msg:
        bot.reply_to(message, 'Ma di diverse categorie')
    elif 'spieg' in msg:
        bot.reply_to(message, 'Te lo spiego io')
    elif 'godo' in msg:
        bot.reply_to(message, 'Penso che stiamo tutti godendo')
    else:
        if random.uniform(0, 1) < 0.01:
            bot.send_message(message.chat.id, 'Non mi assumo responsabilità')


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
