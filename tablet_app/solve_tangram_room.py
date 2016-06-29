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
from kivy_communication import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader


class SolveTangramRoom(Screen):
    def __init__(self, **kwargs):
        print("solveTangramRoom")
        super(Screen, self).__init__(**kwargs)

    def on_enter(self, *args):
        print("on_enter first_screen_room")
        App.
        # self.load_sounds()
        # self.play_sound("TangramOpen_myFriend")


class Background(Widget):
    pass

class TreasureBox(Widget):
    def rotate_shape(self, *kwargs):
        print("rotate shape")

class HourGlassWidget (Widget):
    def __init__(self, **kwargs):
        super(HourGlassWidget, self).__init__(**kwargs)
        self.delta=0
        #self.animate_sand()
        Clock.schedule_interval(self.after_init,0.01)  #only after init is done ids can be accessed

    def after_init(self, *args):
        self.hourglass = self.ids['hourglass']
        self.topSand = self.ids['topSand']
        self.middleSand = self.ids['middleSand']
        self.bottomSand = self.ids['bottomSand']
        self.init = False
        self.do_layout()
        # self.start_hourglass(120)
        return False


    def do_layout(self, *args):
        if (not self.init):
            self.size = Window.width * 0.08, Window.height * 0.2
            self.pos = Window.width * 0.85, Window.height * 0.25
            self.delta = (self.height * 0.2) / 60.0
            sandWidth = self.width
            sandHeight = self.height * 0.25
            self.sandHeight = sandHeight
            self.delta = sandHeight / 480.0   #120*4
            self.hourglass.size = self.width, self.height
            self.hourglass.pos = self.x, self.y
            self.topSand.size = sandWidth, sandHeight
            self.topSand.pos = self.x, self.y+self.height * 0.5
            self.middleSand.size = sandWidth * 0.05, sandHeight * 2
            self.middleSand.pos = self.x + sandWidth/2.0 - sandWidth*0.02, self.y+0
            self.bottomSand.size = sandWidth, 0
            self.bottomSand.pos = self.x, self.y+0 + self.height * 0.039
            self.init = True

    def start_hourglass(self):
        pass

    def stop_hourglass(self, *args):
        self.middleSand.height = 0
        print("time is up")

    def update_hourglass (self, percent):
        # Rinat: change to percentage
        print ('percent: ',percent)
        self.topSand.height = self.topSand.height - self.delta #self.sandHeight*percent
        self.bottomSand.height = self.bottomSand.height + self.delta #self.sandHeight*(1-percent)

    def animate_sand (self,*args):
        animTop = Animation(height=0,
                         duration=60,
                         transition='in_quad')
        #animTop.start(self.topSand)
        animBottom = Animation(height=100,
                         duration=4,
                         transition='in_quad')
        animBottom.start(self.bottomSand)

# runTouchApp(SolveTangramRoom())


