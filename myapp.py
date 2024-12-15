

from sklearn.feature_extraction.text import CountVectorizer  # pip install scikit-learn
from sklearn.linear_model import LogisticRegression
import sounddevice as sd  # pip install sounddevice
import vosk  # pip install vosk
import chat

import json
import queue

import words
from skills import *

q = queue.Queue()

model = vosk.Model('model_small')


device = sd.default.device

samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])  # получаем частоту микрофона


def callback(indata, frames, time, status):


    q.put(bytes(indata))


def recognize(data, vectorizer, clf):
    if len(data) < 7:
        return
        # если нет фразы обращения к ассистенту, то отправляем запрос gpt
    trg = words.TRIGGERS.intersection(data.split())
    if not trg:
        return

    data = data.split()
    filtered_data = [word for word in data if word not in words.TRIGGERS]
    data = ' '.join(filtered_data)
    print("Я векторизую слово: " + data)


    # получаем вектор полученного текста
    # сравниваем с вариантами, получая наиболее подходящий ответ
    # Преобразование команды пользователя в числовой вектор
    user_command_vector = vectorizer.transform([data])
    print("Получился вектор:")
    print(user_command_vector)



    # Предсказание вероятностей принадлежности к каждому классу
    predicted_probabilities = clf.predict_proba(user_command_vector)

    # Задание порога совпадения
    threshold = 0.1

    # Поиск наибольшей вероятности и выбор ответа, если он превышает порог
    max_probability = max(predicted_probabilities[0])
    print("Максимальная совместимость: " + str(max_probability))

    if max_probability >= threshold:
        answer = clf.classes_[predicted_probabilities[0].argmax()]
    else:
        speak("Команда не распознана")
        return

    func_name = answer.split()[0]

    # озвучка ответа из модели data_set
    speak(answer.replace(func_name, ''))

    # запуск функции из skills
    exec(func_name + '()')


def main():
    speak('Привет, Кеша слушает')

    # Обучение матрицы на data_set модели
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))


    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set

    # постоянная прослушка микрофона
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16',
                           channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                print('[Log] ' + data)
                recognize(data, vectorizer, clf)
            # else:
            #     print(rec.PartialResult())


if __name__ == '__main__':
    main()
