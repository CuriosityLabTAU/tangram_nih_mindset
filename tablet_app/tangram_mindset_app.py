from zero_screen_room import *
from first_screen_room import *
from selection_screen_room import *
from solve_tangram_room import *
from game_facilitator import *

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


class MyScreenManager (ScreenManager):

    def enter_first_screen_room(self):
        print("enter_first_screen_room")
        self.current = "FirstScreenRoom"

    def enter_selection_tangram_room(self):
        print("enter_selection_screen_room")
        self.current = "SelectionScreenRoom"

    def enter_solve_tangram_room(self):
        print("enter_solve_tangram_room")
        self.current = "SolveTangramRoom"


root_widget = Builder.load_string('''
MyScreenManager:
    ZeroScreenRoom:
    FirstScreenRoom:
    SelectionScreenRoom:
    SolveTangramRoom:

<ZeroScreenRoom>:
    name: 'zero_screen_room'
    Widget:
        Button:
            id: start_button
            background_color: 1,0,1,1
            background_normal: ''
            text: 'Start'
            font_size: 36
            size: root.width * 0.3, root.height * 0.2
            pos: root.width * 0.5 - self.width * 0.5, root.height * 0.7 - self.height * 0.5
            on_press: app.action('press_start_button')

<FirstScreenRoom>:
    name: 'first_screen_room'
    Widget:
        FirstScreenBackground:
            size: root.size
            pos: root.pos
        Button:
            id: yes_button
            borders: 2, 'solid', (1,1,0,1)
            background_normal: 'images/BalloonBtn.gif'
            background_down: 'images/BalloonBtn_on.gif'
            size: root.width * 0.2, root.height * 0.5
            pos: root.width * 0.5 - self.width * 0.5, root.height * 0.7 - self.height * 0.5
            on_press: app.action('press_yes_button')
            opacity: 0

<FirstScreenBackground>:
    Image:
        size: root.size
        pos: root.pos
        source: 'images/TangramGame_Open.jpg'
        allow_stretch: True
        keep_ratio: False


<SelectionScreenRoom>:
    name: 'selection_screen_room'
    Widget:
        Image:
            size: root.size
            pos: root.pos
            source: 'images/TangramGame_Selection.jpg'
            allow_stretch: True
            keep_ratio: False

<SolveTangramRoom>:
    name: 'solve_tangram_room'
    Widget:
        Background:
            size: root.size
            pos: root.pos
        TreasureBox:
            size: root.size
            pos: root.pos
        HourGlassWidget:
            id: hourglass
        GridLayout:
            columns: 3
            rows: 4
            Button:
                text: 'run'
                on_press: app.press_run_button()
            Button:
                text: 'start'
                on_press: app.action('press_start_button')
            Button:
                text: 'yes'
                on_press: app.action('press_yes_button')
            Button:
                text: 'treasure1'
                on_press: app.press_treasure(0)
            Button:
                text: 'treasure2'
                on_press: app.press_treasure(1)
            Button:
                text: 'treasure3'
                on_press: app.press_treasure(2)
            Button:
                text: 'move'
                on_press: app.tangram_move()
            Button:
                text: 'rotate'
                on_press: app.turn_button()

<Background>:
    Image:
        size: root.size
        pos: root.pos
        source: 'images/tangram_background.jpg'
        allow_stretch: True
        keep_ratio: False

<TreasureBox>:
    Image:
        id: box
        size: root.width * 0.6, root.height * 0.6
        pos: root.width * 0.2, root.height * 0.2
        source: 'images/TreasureBoxLayers.gif'
        allow_stretch: True
        keep_ratio: False

    Image:
        id: rotate
        size: root.width * 0.08, root.height * 0.1
        pos: root.width * 0.65, root.height * 0.48
        source: 'images/Tangram_rotate_btn.gif'
        allow_stretch: True
        keep_ratio: False
        on_touch_down: root.rotate_shape()

<HourGlassWidget>:
    Image:
        id:topSand
        source: 'images/sand.jpg'
        allow_stretch: True
        keep_ratio: False
    Image:
        id:middleSand
        source: 'images/sand.jpg'
        allow_stretch: True
        keep_ratio: False
    Image:
        id:bottomSand
        source: 'images/sand.jpg'
        allow_stretch: True
        keep_ratio: False
    Image:
        id: hourglass
        source: 'images/hour_glass.gif'
        allow_stretch: True
        keep_ratio: False
        pos: self.pos
        size: self.size
''')

# functions connecting to button pressed

class TangramMindsetApp(App):
    interaction = None
    sounds = None
    current_sound = None
    screen_manager = None

    def build(self):
        self.interaction = Interaction(
            [('tablet', 'TabletComponent'),
             ('robot', 'RobotComponent'),
             ('child', 'ChildComponent'),
             ('internal_clock', 'ClockComponent'),
             ('hourglass', 'HourglassComponent'),
             ('game', 'GameComponent')]
        )
        self.interaction.components['hourglass'].max_counter = 120
        self.interaction.load()
        self.interaction.components['game'].game_facilitator = GameFacilitator()

        s = SolveTangramRoom()
        self.interaction.components['hourglass'].widget = s.ids['hourglass']
        self.interaction.components['tablet'].app = self
        self.interaction.components['robot'].app = self
        self.interaction.run()

        self.load_sounds()
        self.init_communication()

        self.screen_manager = MyScreenManager()
        self.screen_manager.add_widget(ZeroScreenRoom())
        self.screen_manager.add_widget(FirstScreenRoom())
        self.screen_manager.add_widget(SelectionScreenRoom())
        self.screen_manager.add_widget(SolveTangramRoom())
        return self.screen_manager

    def init_communication(self):
        KL.start([DataMode.file, DataMode.communication, DataMode.ros], self.user_data_dir)
        KC.start(the_parents=[self, self.interaction.components['robot']], the_ip='127.0.0.1')

    def load_sounds(self):
        # load all the wav files into a dictionary whose keys are the expressions from the transition.json
        sound_list = ['introduction', 'click_balloon']
        self.sounds = {}
        for s in sound_list:
            self.sounds[s] = SoundLoader.load("sounds/" + s + ".m4a")
        self.current_sound = None

    def action(self, action):
        self.interaction.components['child'].on_action([action])

    def first_screen(self):
        self.screen_manager.current = 'first_screen_room'

    def selection_screen(self, x):
        # Rinat: x is a list of tangrams from maor
        # you need to present all options with the tangram pieces
        print(x)
        self.screen_manager.current = 'selection_screen_room'

    def tangram_screen(self, x):
        # Rinat: x is a single tangram from maor
        # you need to present it and allow game
        print(x)
        self.screen_manager.current = 'solve_tangram_room'

    def robot_express(self, action):
        print ('robot_express ',action)
        self.current_sound = action[0]
        try:
            sound = self.sounds[self.current_sound]
            print(sound)
            sound.bind(on_stop=self.finish_robot_express)
            sound.play()
        except:
            print('no sound file: ', action[0])
            self.finish_robot_express(0)

    def finish_robot_express (self, dt):
        print ('finish_robot_express', self, self.current_sound)
        self.interaction.components['robot'].finished_expression(self.current_sound)

    def yes(self):
        print ('yes in app')
        self.screen_manager.current_screen.ids['yes_button'].opacity = 1


if __name__ == "__main__":
    TangramMindsetApp().run()