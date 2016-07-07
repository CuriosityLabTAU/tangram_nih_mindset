import json
from random import choice
import time
try:
    from plyer import tts
    tts.speak('hello')
    the_tts = 'plyer'
except:
    import pyttsx
    the_tts = 'pyttsx'


class TextHandler:

    def __init__(self, condition='growth'):
        self.data = None
        self.condition = condition
        self.what = None
        if the_tts is 'pyttsx':
            self.engine = pyttsx.init()
            self.engine.setProperty('voice', 'HKEY_LOCAL_MACHINE/SOFTWARE/Microsoft/Speech/Voices/Tokens/TTS_MS_EN-US_ZIRA_11.0')
            self.engine.connect(topic='finished-utterance', cb=self.finished)

    def load_text(self, filename='./tablet_app/robot_text.json'):
        with open(filename) as data_file:
            self.data = json.load(data_file)

    def finished(self):
        print('finished', self.what)
        return True

    def say(self, what):
        self.what = what
        if what in self.data:
            the_options = self.data[what]
            the_text = []
            if isinstance(the_options, list):
                the_text.append(choice(the_options))
            elif isinstance(the_options, dict):
                if 'all' in the_options:
                    the_text.append(choice(the_options['all']))
                if self.condition in the_options:
                    the_text.append(choice(the_options[self.condition]))

            print('speak: ', the_text)
            for txt in the_text:
                if the_tts is 'pyttsx':
                    self.engine.say(txt)
                else:
                    tts.speak(txt)
                    time.sleep(float(len(txt)) * 0.05)
            if the_tts is 'pyttsx':
                self.engine.runAndWait()
                time.sleep(1)
            return self.finished()
        else:
            return False