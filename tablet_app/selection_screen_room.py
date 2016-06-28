from interaction_control import *
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import Layout
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.app import App
from kivy.animation import Animation
from kivy.core.window import Window

from kivy.app import App
from kivy_communication import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader

class SelectionScreenRoom(Screen):

    def __init__(self, **kwargs):
        print("init first")
        super(Screen, self).__init__(**kwargs)

    def on_enter(self, *args):
        print("on_enter selection_screen_room")
        #self.load_sounds()
        #self.play_sound("TangramOpen_myFriend")

    def load_sounds(self):
        self.sounds = {}
        self.sounds[0] = SoundLoader.load("sounds/TangramOpen_myFriend.m4a")
        self.sounds[1] = SoundLoader.load("sounds/TangramOpen_click.m4a")

    def callback(self):
        print('rinat')

    def play_sound(self, soundName):
        if soundName == "TangramOpen_myFriend":
            sound = self.sounds.get(0)
            sound.bind(on_stop=self.finish_tangram_intro)
            # Clock.schedule_once(self.callback(), 0)
        elif soundName == "TangramOpen_click":
            sound = self.sounds.get(1)
        if sound is not None:
            sound.volume = 0.5
            sound.play()

    def finish_tangram_intro(self, dt):
        #now present the yes button
        self.ids['yes_button'].opacity = 1
        print("finish_tangram_intro")

    #def press_yes_button(self):
        #print("press_yes_button")
        #app.sm.enter_solve_tangram_room()
        #App.action('press_yes_button')

class FirstScreenBackground(Widget):
    pass


