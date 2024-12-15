import os, webbrowser, sys, requests, subprocess, pyttsx3, datetime
import pyautogui
engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    engine.say(text)
    engine.runAndWait()
    print(text)

def collapse_window():
    pyautogui.hotkey('win', 'd')

def pause():
    pyautogui.hotkey('space')

def music():
    os.startfile("C:\\Users\\pavel\\AppData\\Local\\Programs\\YandexMusic\\Яндекс Музыка.exe")
    speak("Включаю")

def close_window():
    pyautogui.hotkey('alt', 'f4')

def ctime():
    h = ""
    m = ""
    now = datetime.datetime.now()
    if now.hour == 1 or now.hour == 21:
        h = ""
    elif now.hour in [2, 3, 4, 22, 23, 24]:
        h = "а"
    else:
        h = "ов"
    if now.minute >= 11 and now.minute <= 19:
        m = ""
    else:
        i = now.minute % 10
        if i == 1:
            m = "а"
        elif i in [2, 3, 4]:
            m = "ы"
        else:
            m = ""
    speak(f"Сейчас {now.hour} час{h} {now.minute} минут{m}")

def browser():
    os.startfile('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')

def game():
    os.startfile("C:\\Program Files (x86)\\Steam\\steam.exe")

def offpc():
    #os.system('shutdown /s')
    speak("пк выключен")


def weather():
    try:
        params = {'q': 'Шилка', 'units': 'metric',
                  'lang': 'ru', 'appid': '459dae14a5a24997247998c061c61ee5'}
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather', params=params)
        if not response:
            raise
        w = response.json()
        speak(
            f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")

    except:
        speak(
            'Произошла ошибка при попытке запроса к ресурсу, проверь код')


def youtube():
    webbrowser.open('https://youtube.com/', new=2)

def offBot():
    sys.exit()

def passive():
    pass