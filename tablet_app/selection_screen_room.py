from interaction_control import *
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import Layout
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window

from kivy.app import App
from kivy_communication import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader

import json

class SelectionScreenRoom(Screen):
    selection_json = None
    selection_tasks = {}

    def __init__(self, **kwargs):
        print("init first")
        super(Screen, self).__init__(**kwargs)

    def init_selection_options(self,x):
        #this function is called from tangram_mindset_app
        print ('init_selection_options', x)
        self.selection_json = x

    def on_enter(self, *args):
        print("on_enter selection_screen_room")
        self.convert_json2tasks()

    def convert_json2tasks(self):
        i=0
        for task in self.selection_json[0]:
            print(json.loads(task))
            self.selection_tasks[i] = json.loads(task)
            #print (self.selection_tasks[i])
            i=i+1
        print (self.selection_tasks[1]['pieces'])

    def display_task(self,task):
        print('display_task')