import kivy
kivy.require('1.8.0')  # replace with your current kivy_tests version !
from kivy.graphics import *

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
from kivy.graphics.vertex_instructions import (Rectangle,
                                               Ellipse,
                                               Line)
from kivy.app import App
from kivy_communication import *
from kivy.core.audio import SoundLoader
from tangrams import *
from tangram_game import *
import json
from kivy_communication import logged_widgets

from tangram_selection_not_using import *
from kivy.uix.screenmanager import ScreenManager, Screen


class SelectionScreenRoom(Screen):
    tasks_json = None
    tasks_layout = []
    the_app = None
    the_tablet = None

    def __init__(self, the_tablet):
        self.the_tablet = the_tablet
        super(Screen, self).__init__()

    def init_selection_options(self,x,the_app):
        # this function is called from tangram_mindset_app
        # print ('init_selection_options', x)
        self.tasks_json = x
        self.the_app=the_app

    def on_enter(self, *args):
        # print("on_enter selection_screen_room")
        self.init_tasks()
        self.the_tablet.change_state('selection_screen')
        if self.the_app.tablet_disabled:
            self.disable_widgets()
        # self.selections_widget = SelectionsWidget()
        # self.display_tasks()

    def init_tasks (self):
        # print("init_tasks",self.the_app)
        self.ids["tangram_selection_widget"].clear_widgets()
        self.ids["tangram_selection_widget"].init_app(self.the_app)
        i = 0
        for task_json in self.tasks_json:
            # print(task_json)
            selection_task_layout = SelectionTaskLayout(index=i)
            selection_task_layout.reset(str(i))
            selection_task_layout.import_json_task(task_json[0])
            selection_task_layout.update_selection_task_pos()
            selection_task_layout.update_task()
            selection_task_layout.update_task_pieces(task_json[0])
            self.tasks_layout.append(selection_task_layout)
            self.ids["tangram_selection_widget"].add_widget(selection_task_layout)
            #self.add_widget(selection_task_layout)
            i += 1

    def show_selection(self, treasure):
        # print("show selection treasure=", treasure)
        selection_task_layout = self.tasks_layout[treasure]
        selection_task_layout.set_border()

    def disable_widgets(self):
        for c in self.ids["tangram_selection_widget"].children:
            c.disabled = True


class SelectionTaskLayout(LoggedButton, TaskLayout):
    # inherits from TaskLayout which is in tangram_game.py

    def __init__(self, index):
        super(SelectionTaskLayout, self).__init__()
        self.index = index
        self.name = str(index)
        self.update_position()
        self.canvas.clear()
        with self.canvas.before:
            print ("self.canvas.before")
            # Color(1,0,0,1)
            # self.rect = Rectangle()
            # self.rect.pos= self.pos
            # self.rect.size = self.size
            # # self.bind(size=self._update_rect, pos=self._update_rect)
            # # self.bind(size=self.update_position, pos=self.update_position)

    def update_position(self, *args):
        # print('update_position')
        box_width_and_gap = Window.width * 0.31
        margin_left = Window.width * 0.073
        self.size = [Window.width * 0.28, Window.height * 0.36]
        self.pos = [margin_left + self.index * box_width_and_gap, Window.height * 0.21]

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        # print('self.size ',self.size, 'instance.size ', instance.size)
        self.rect.size = self.size

    def on_press(self, *args):
        super(Button, self).on_press()
        # print("Selection Task Layout: on_press" , self.index)
        self.set_border()
        self.parent.the_app.press_treasure(self.index)  #I'm sending index+1 because index=0 will cause problems in game.py > tangram_selected

    def set_border (self):
        # print ('set_border')
        g = InstructionGroup()
        g.add(Color(1, 0, 0, 1))
        L = Line(points=[self.x, self.y, self.x+self.width, self.y, self.x+self.width, self.y+self.height, self.x, self.y+self.height],
                 close=True,
                 width=3)
        g.add(L)
        self.canvas.add(g)
        self.canvas.ask_update()

    def update_selection_task_pos(self):
        # print ('update_selection_task_pos ', self.index)
        for p in self.pieces:
            p['pos'][0] += self.x + 4.5 * TangramGame.SCALE
            p['pos'][1] += self.y + 6.5 * TangramGame.SCALE

    def update_task_pieces(self, task_pieces):
        # in the selection room show also the pieces of the tangram (not only the shade)
        # print ('update_task_pieces TaskLayout')
        # for g in self.groups:
        #    self.canvas.remove(g)
        # self.groups = []

        i = 0
        for p in self.pieces:
            name = p['name']
            dx = TangramPiece.piece_size[name][0] * TangramGame.SCALE / 2
            dy = TangramPiece.piece_size[name][1] * TangramGame.SCALE / 2
            dx=0
            dy=0

            p['pos'] = [self.x - dx  + TangramGame.SCALE * 3 * (i+1), -dy + Window.height * 0.14]
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


class TangramSelectionWidget(Widget):
    task_json = None
    the_app = None
    current = None  #current selected piece
    current_game_task_layout = None

    def __init__(self, **kwargs):
        # print("TangramSelectionWidget __init__")
        super(TangramSelectionWidget, self).__init__(**kwargs)
        self.canvas.clear()
        self.clear_widgets()

    def init_app(self,the_app):
        self.the_app =  the_app

class BalloonsWonWidget (Widget):
    pass