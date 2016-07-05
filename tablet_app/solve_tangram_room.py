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
from tangram_game import *


class SolveTangramRoom(Screen):
    task_json = None
    the_app = None

    def __init__(self, **kwargs):
        print("solveTangramRoom")
        super(Screen, self).__init__(**kwargs)

    def on_enter(self, *args):
        print("on_enter solve_tangram_room")
        # self.load_sounds()
        # self.play_sound("TangramOpen_myFriend")

    def init_task(self,x,the_app):
        self.task_json = x[0]
        self.the_app = the_app
        print("Solve Tangram Room init_task ", self.task_json)
        game_task_layout = GameTaskLayout()
        game_task_layout.reset(str(0))
        game_task_layout.import_json_task(self.task_json)
        print ("after import json")
        game_task_layout.update_selection_task_shade()
        print ("after update selection task shade")
        game_task_layout.update_task()
        print ("after update task")

        # #game_task_layout.update_task_pieces()
        #self.game_tasks_layout.append(game_task_layout)

        self.ids['tangram_game_widget'].add_widget(game_task_layout)

        #self.add_widget(game_task_layout)

class GameTaskLayout(Button, TaskLayout):
    # inherits from TaskLayout which is in tangram_game.py

    def __init__(self):
        super(GameTaskLayout, self).__init__()
        self.canvas.clear()
        print("Window.width", Window.width)
        self.size_hint = [0.28,0.28]
        self.update_position()
        with self.canvas.before:
             print ("self.canvas.before")
             Color(1,0,0,1)
             self.rect = Rectangle()
             self.bind(size=self._update_rect, pos=self._update_rect)
             self.bind(size=self.update_position, pos=self.update_position)

    def update_position(self, *args):
        print('update_position')
        self.pos = [Window.width * 0.3, Window.height * 0.3]
        #self.update_selection_task_pos()

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        print('self.size ',self.size, 'instance.size ', instance.size)
        self.rect.size = self.size

    def on_press(self, *args):
        super(Button, self).on_press()
        # self.incorrect_pos()
        # self.the_app.selected_task(self.original_task)
        print("Selection Task Layout: on_press" , self.name)
        #self.parent.the_app.press_treasure(self.index)

    def update_selection_task_shade(self):
        print ('update_selection_task_shade ')
        print('TangramGame.SCALE ', TangramGame.SCALE)
        print('update_selection_task_pos ', self.pos, self.size)
        for p in self.pieces:
            # p['pos'][0] += 13 * TangramGame.SCALE
            # p['pos'][1] += 20 * TangramGame.SCALE
            print("p[pos] ", p['pos'], p['name'])

            #p['pos'][0] += 100 + index * TangramGame.SCALE * 15
            #p['pos'][1] += round(TangramGame.window_size[1] / 2.7)

            p['pos'][0] += self.x + 3.5 * TangramGame.SCALE
            p['pos'][1] += self.y + 3.5 * TangramGame.SCALE



    def update_task_pieces(self):
        # in the selection room we are adding the game pieces
        print ('update_task_pieces TaskLayout')
        # for g in self.groups:
        #    self.canvas.remove(g)
        # self.groups = []
        i = 0
        for p in self.pieces:
            print(p['pos'])
            p['pos'] = [self.x + 40 * i, Window.height * 0.14]
            #p['rot'] = 0
            self.groups.append(TangramPiece.get_shape(p, self.get_color(i)))
            self.canvas.add(self.groups[-1])
            i += 1

    def get_color(self, index):
        modulo = index % 3
        if (modulo == 0):
            my_color = Color(1,0,0,1)
        elif (modulo == 1):
            my_color = Color(0,1,0,1)
        elif (modulo == 2):
            my_color = Color(0,0,1,1)
        return my_color


class Background(Widget):
    pass

class TreasureBox(Widget):
    def rotate_shape(self, *kwargs):
        print("rotate shape")


class TangramGameWidget(Widget):
    def __init__(self, **kwargs):
        super(TangramGameWidget, self).__init__(**kwargs)
        self.canvas.clear()


class HourGlassWidget (Widget):
    def __init__(self, **kwargs):
        super(HourGlassWidget, self).__init__(**kwargs)
        self.delta=0
        #self.animate_sand()
        Clock.schedule_interval(self.after_init,0.01)  #only after init is done ids can be accessed

    def after_init(self, *args):
        print ('HourGlassWidget: after init')
        self.hourglass = self.ids['hourglass']
        self.topSand = self.ids['topSand']
        self.middleSand = self.ids['middleSand']
        self.bottomSand = self.ids['bottomSand']
        self.init = False
        self.do_layout()
        # self.start_hourglass(120)
        return False

    def do_layout(self, *args):
        print ("do_layout")
        print (self)
        if (not self.init):
            self.size = Window.width * 0.08, Window.height * 0.2
            self.pos = Window.width * 0.85, Window.height * 0.25
            sandWidth = self.width
            sandHeight = self.height * 0.25
            self.sandHeight = sandHeight
            self.hourglass.size = self.width, self.height
            self.hourglass.pos = self.x, self.y
            self.topSand.size = sandWidth, sandHeight
            self.topSand.pos = self.x, self.y+self.height * 0.5
            self.middleSand.size = sandWidth * 0.05, sandHeight * 2
            self.middleSand.pos = self.x + sandWidth/2.0 - sandWidth*0.02, self.y+0
            self.bottomSand.size = sandWidth, 0
            self.bottomSand.pos = self.x, self.y+0 + self.height * 0.041
            self.init = True

    def start_hourglass(self):
        print('start hourglass')
        pass

    def stop_hourglass(self, *args):
        self.middleSand.height = 0
        print("time is up")

    def update_hourglass (self, percent):
        # Rinat: change to percentage
        current_time = float(percent[0][0])
        total_time = float(percent[0][1])
        current_percent = current_time / total_time
        self.topSand.height =  self.sandHeight * current_percent
        self.bottomSand.height = self.sandHeight* (1 - current_percent)
        if (current_percent < 0.02):
            self.middleSand.height = 0




    # def animate_sand (self,*args):
    #     animTop = Animation(height=0,
    #                      duration=60,
    #                      transition='in_quad')
    #     #animTop.start(self.topSand)
    #     animBottom = Animation(height=100,
    #                      duration=4,
    #                      transition='in_quad')
    #     animBottom.start(self.bottomSand)

# runTouchApp(SolveTangramRoom())


