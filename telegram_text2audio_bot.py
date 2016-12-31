#!/usr/bin/python

# Install FFMpeg:  apt-get install ffmpeg
# Install Telebot: git clone https://github.com/eternnoir/pyTelegramBotAPI.git
# Install Espeak apt-get install espeak
# Sustituir BASE_PATH por la ruta dodne se van a guardar los textos y los audio
# Crear una carpeta llamada "text" y otra "audio" en BASE_PATH para guardar los textos enviados y los audios generados

import telebot
import subprocess
import os
from datetime import datetime
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

TOKEN = open(os.path.realpath('..') + "/tokens_telegram_bots/token_text2audio_bot.txt", 'rb').read().rstrip('\n')

BASE_PATH = "/media/HDD2/telegram_bot"

def send_message(cid, text):
    bot.send_message(cid, text)

def send_audio(cid, audio):
    bot.send_audio(cid, audio)

def reply_to(message, text):
    bot.reply_to(message, text)

def touch(fname):
    if os.path.exists(fname):
        os.utime(fname, None)

def current_time():
    date = datetime.now()
    final_date = date.strftime('%Y-%m-%d_%H:%M:%S')
    return str(final_date)

def textToFile(text):
    path_file = BASE_PATH + "/text/speech" + time + ".txt"
    touch(path_file)
    file = open(path_file, "w")
    file.write(str(text) + '\n')
    file.close()
    return path_file

def convertAudio(input_file, output_file, lang):
    language = "english-us"
    if (str(lang) == "es"):
        language = "spanish"
    bashCommand = "/usr/bin/espeak -f " + input_file + " -v " + language + " --stdout | ffmpeg -i - -ar 44100 -ac 2 -ab 192k -f mp3 " + output_file
    os.system(bashCommand)

def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    out = p.stdout.read()
    out = out.replace("\n", "")
    return out

time = current_time()
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    reply_to(message, "This is the text to audio bot. Enter your message and I will send an audio with your message")
    reply_to(message, "Use: /convert YOUR TEXT")
    reply_to(message, "Spanish language Use: /convert YOUR TEXT es")

@bot.message_handler(commands=['convert']) 
def command_convert(message):
    cid = message.chat.id
    try:
       check_string = message.text.replace("/convert", "")
       if str(check_string) == '':
          send_message(cid, "Please type a text to convert to audio")
       else:
          language = check_string[-2:].lower()
          final_text = check_string
          if (language == "es" or language == "en"):
              final_text = check_string[:-2]
          file_path = textToFile(final_text)    
          random_string = system_call("/usr/bin/head /dev/urandom | tr -dc A-Za-z0-9 | /usr/bin/head -c 5 | xargs echo").lower()
          path_file = BASE_PATH + "/audio/audio_" + time + "_" + random_string + ".mp3"
          bot.send_message(cid, "Converting file, please wait...")
          convertAudio(file_path, path_file, language)
          audio = open(path_file, 'rb')
          send_message(cid, "Sending file...")
          send_audio(cid, audio)
          send_message(cid, "File sended !! Thank you !!")
    except ValueError:
       send_message(cid, "Bot error, sorry...try again")

bot.polling(none_stop=True, interval=0)
