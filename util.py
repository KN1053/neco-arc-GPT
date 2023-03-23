import openai
import os
import pyttsx3
import random
import threading
from dotenv import load_dotenv


def normalize(list):
    mag = sum(list)
    return [v / mag for v in list]


def make_cum(list):
    acc = 0
    for i in range(len(list)):
        temp = list[i]
        list[i] = acc
        acc += temp
    return list


class WeightedRandomMap:
    def __init__(self, list):
        self.names = [obj["name"] for obj in list]
        self.P = make_cum(normalize([obj["probability"] for obj in list]))
        assert len(self.names) == len(self.P)

    def get_rand(self):
        val = random.random()
        for i, p in enumerate(self.P):
            if p > val:
                return self.names[i - 1]
        return self.names[-1]


def openai_query(message):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        response = openai.Completion.create(model="text-davinci-003", prompt=message, temperature=.95, max_tokens=2500)
        return response["choices"][0]["text"]
    except Exception:
        message = "Nyaa! I'm Neco-Arc, an advanced programmable AI from the café Ahnenerbe. Unfortunately, it looks like ChatGPT is not reachable at the moment. You may need to set your API key to an environment variable in order for it to work nyaa."
        return message


def speak(message, callback):
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    engine.say(message)

    def f():
        engine.runAndWait()
        callback()
    threading.Thread(target=f).start()
