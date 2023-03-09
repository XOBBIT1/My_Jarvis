import datetime
import subprocess
import time
import os
import webbrowser

import requests
import sounddevice as sd
from fuzzywuzzy import fuzz
from num_to_rus import Converter

from settings import config, commands


def speak(what: str):
    audio = config.model.apply_tts(
        text=what,
        speaker=config.speaker,
        sample_rate=config.sample_rate,
        put_accent=True,
        put_yo=True
    )

    sd.play(audio, config.sample_rate * 1.05)
    time.sleep((len(audio) / config.sample_rate) + 0.5)
    sd.stop()


def respond(voice: str):
    print(voice)
    if voice.startswith(commands.TRIGGERS):

        cmd = recognize_cmd(filter_cmd(voice))

        if cmd['cmd'] not in commands.DATA_SET.keys():
            speak("Чтоо случилось?")
        else:
            execute_cmd(cmd['cmd'])


def filter_cmd(raw_voice: str):

    for x in commands.TRIGGERS:
        raw_voice = raw_voice.replace(x, "").strip()

    for x in commands.COMMANDS_FOR_DO:
        raw_voice = raw_voice.replace(x, "").strip()

    return raw_voice


def recognize_cmd(cmd: str):
    recognize_commands = {'cmd': '', 'percent': 0}
    for key, value in commands.DATA_SET.items():

        for words in value:
            vars_recognize = fuzz.ratio(cmd, words)
            if vars_recognize > recognize_commands['percent']:
                recognize_commands['cmd'] = key
                recognize_commands['percent'] = vars_recognize

    return recognize_commands


def execute_cmd(cmd: str):
    if cmd == 'help':
        speak(commands.HELP)

    elif cmd == 'open_browser':
        speak("Какоойй?")
        if cmd == 'yandex':
            yandex_path = os.environ['YANDEX']
            webbrowser.open(yandex_path)
        elif cmd == 'chrom':
            chrom_path = os.environ['CHROM']
            webbrowser.open(chrom_path)
        elif cmd == 'edge':
            edge_path = os.environ['EDGE']
            webbrowser.open(edge_path)
        speak("Удачи в поиске чумба!")

    elif cmd == 'ctime':
        now = datetime.datetime.now()
        speak("Сейчас " + Converter().convert(now.hour) + "часов" + ":" + Converter().convert(now.minute) + "минут")
        print(str(now.hour))

    elif cmd == 'music':
        spotify_path = os.environ['SPOTIFY']
        subprocess.Popen(spotify_path)
        speak("Приятного прослушивания !")

    elif cmd == "weather":
        try:
            params = {'q': 'Minsk', 'units': 'metric', 'lang': 'ru', 'appid': '82b6d937032b30ff2cc9bdcfc6b0771b'}
            response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
            if not response:
                raise
            w = response.json()
            speak(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")

        except:
            speak('Произошла ошибка при попытке запроса к ресурсу API, проверь код')



    elif cmd == 'stop':
        speak("Покааааааааа!!!")
        sd.stop()


