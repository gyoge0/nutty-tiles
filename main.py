import time
import mss
import numpy
import pytesseract
import re
import keyboard
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source="english", target="spanish")

words = {}

def get_words():
    global words
    print("paste spanish then english, STOP to exit")
    while (span := input("Spanish: ")).upper() != "STOP":
        words[input("English: ").strip().lower()] = span.strip()
    print(words)


dimensions = {'top': 225, 'left': 700, 'width': 550, 'height': 115}

get_words()

with mss.mss() as sct:
    while True:
        match keyboard.read_key():
            case "f4":
                im = numpy.asarray(sct.grab(dimensions))

                text = pytesseract.image_to_string(im).strip().replace("|", "I").lower() # 'I' is read as '|' (pipe)

                translated = words.get(text, re.sub(r'[^a-zA-Z]', '', translator.translate(text)).strip())
                print(text, "=", translated)
                keyboard.write(translated, delay=0.005)
                keyboard.press_and_release("enter")
                time.sleep(0.15)
            case "f10":
                span = input("Spanish: ")
                words[input("English: ").strip().lower()] = span.strip()
            case "f12":
                get_words()
