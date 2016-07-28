
from kivy.app import App
from kivy_communication import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader

class ZeroScreenRoom(Screen):
    the_app = None
    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()

    def on_enter(self, *args):
        KL.restart()
    #print "Zero"
    #self.sm.current = "SolveTangramRoom"
    #def __init__(self, **kwargs):
    #    print("init zero")
    #    super(Screen, self).__init__(**kwargs)

    #def press_start_button(self):
        #print("press_yes_button")
        #app.sm.enter_solve_tangram_room()
        #App.action('press_yes_button')

    def spinner_selected(self):
        print("spinner_selected")
        condition = self.ids['condition_spinner'].text
        self.the_app.CONDITION = condition
        print(condition)
