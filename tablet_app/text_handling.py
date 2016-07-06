import json
from random import choice
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
            self.engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
            self.engine.connect(topic='finished-utterance', cb=self.finished)

    def load_text(self, filename='robot_text.json'): #'./tablet_app/robot_text.json'
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
                    tts.speak(txt, what)
            if the_tts is 'pyttsx':
                self.engine.runAndWait()
            return self.finished()
        else:
            return False

th = TextHandler()
th.load_text()
print(th.say('test'))


def robot_express(self, action):
    print ('robot_express ',action)
    self.current_sound = action[0]
    # attempt tts
    if self.text_handler.say(self.current_sound):
        self.finish_robot_express(0)
    else:   # attempt recorded speech
        try:
            sound = self.sounds[self.current_sound]
            print(sound)
            sound.bind(on_stop=self.finish_robot_express)
            sound.play()
        except: # there is no sound for
            print('no sound for: ', action[0])
            self.finish_robot_express(0)
