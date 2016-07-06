from tangram_selection_not_using import *
from tangram_game import *

from zero_screen_room import *
from first_screen_room import *
from selection_screen_room import *
from solve_tangram_room import *
from game_facilitator import *

from interaction_control import *
from game import *
from tablet import *

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


GAME_WITH_ROBOT = False

class MyScreenManager (ScreenManager):
    pass

# MyScreenManager:
#    ZeroScreenRoom:
#    FirstScreenRoom:
#    SelectionScreenRoom:
#    SolveTangramRoom:

root_widget = Builder.load_string('''

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
            on_press: app.press_start_button()

<FirstScreenRoom>:
    name: 'first_screen_room'
    Widget:
        FirstScreenBackground:
            size: root.size
            pos: root.pos
        Button:
            id: yes_button
            borders: 2, 'solid', (1,1,0,1)
            background_normal: './tablet_app/images/BalloonBtn.gif'
            background_down: './tablet_app/images/BalloonBtn_on.gif'
            size: root.width * 0.2, root.height * 0.5
            pos: root.width * 0.5 - self.width * 0.5, root.height * 0.7 - self.height * 0.5
            on_press: app.press_yes_button()
            opacity: 0

<FirstScreenBackground>:
    Image:
        size: root.size
        pos: root.pos
        source: './tablet_app/images/TangramGame_Open.jpg'
        allow_stretch: True
        keep_ratio: False


<SelectionScreenRoom>:
    name: 'selection_screen_room'
    Widget:
        Image:
            size: root.size
            pos: root.pos
            source: './tablet_app/images/TangramGame_Selection.jpg'
            allow_stretch: True
            keep_ratio: False
        SelectWidget:
            id: selection_widget

<SelectWidget>
    name: "select_widget"

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
            id: hourglass_widget
        TangramGameWidget:
            id: tangram_game_widget


<Background>:
    Image:
        size: root.size
        pos: root.pos
        source: './tablet_app/images/tangram_background.jpg'
        allow_stretch: True
        keep_ratio: False

<TreasureBox>:
    Image:
        name: 'treasure_box'
        id: box
        size: root.width * 0.6, root.height * 0.6
        pos: root.width * 0.2, root.height * 0.2
        source: './tablet_app/images/TreasureBoxLayers.gif'
        allow_stretch: True
        keep_ratio: False

<HourGlassWidget>:
    name: 'hour_glass_widget'
    Image:
        id:topSand
        source: './tablet_app/images/sand.jpg'
        allow_stretch: True
        keep_ratio: False
    Image:
        id:middleSand
        source: './tablet_app/images/sand.jpg'
        allow_stretch: True
        keep_ratio: False
    Image:
        id:bottomSand
        source: './tablet_app/images/sand.jpg'
        allow_stretch: True
        keep_ratio: False
    Image:
        id: hourglass
        source: './tablet_app/images/hour_glass.gif'
        allow_stretch: True
        keep_ratio: False
        pos: self.pos
        size: self.size

<TangramGameWidget>:
    name: 'tangram_game_widget'


''')

# functions connecting to button pressed


class TangramMindsetApp(App):
    interaction = None
    sounds = None
    current_sound = None
    screen_manager = None
    current = None

    game = None
    selection = None

    def build(self):
        self.interaction = Interaction(
            [('robot', 'RobotComponent'),
             ('child', 'ChildComponent'),
             ('internal_clock', 'ClockComponent'),
             ('hourglass', 'HourglassComponent')
             ]
        )
        self.interaction.components['tablet'] = TabletComponent(self.interaction, 'tablet')
        self.interaction.components['game'] = GameComponent(self.interaction, 'game')
        
        self.interaction.components['hourglass'].max_counter = 120
        self.interaction.load(filename='./tablet_app/transitions.json')
        self.interaction.components['game'].game_facilitator = GameFacilitator()

        s = SolveTangramRoom()

        self.interaction.components['tablet'].hourglass_widget = s.ids['hourglass_widget']
        #self.interaction.components['hourglass'].widget = s.ids['hourglass_widget']
        self.interaction.components['tablet'].app = self
        if not GAME_WITH_ROBOT:
            self.interaction.components['robot'].app = self
        self.interaction.run()

        self.load_sounds()
        self.init_communication()

        self.screen_manager = MyScreenManager()
        self.screen_manager.add_widget(ZeroScreenRoom())
        self.screen_manager.add_widget(FirstScreenRoom())
        self.screen_manager.add_widget(SelectionScreenRoom())
        self.screen_manager.add_widget(s)

        #self.game = TangramGame(self)
        #self.selection = TangramSelection(self)

        #self.selection = TangramSelection(self)
        #self.agent = Agent(parent_app=self)
        #screen = Screen(name='selection')
        #self.screen_manager.get_screen('selection_screen_room').add_widget(self.selection.the_widget)


        return self.screen_manager

    def on_start(self):
        print ('app: on_start')
        TangramGame.SCALE = round(self.root_window.size[0] / 60)
        TangramGame.window_size = self.root_window.size

    def init_communication(self):
        KL.start([DataMode.file, DataMode.communication, DataMode.ros], self.user_data_dir)
        KC.start(the_parents=[self, self.interaction.components['robot']], the_ip='192.168.0.101') # 127.0.0.1

    def load_sounds(self):
        # load all the wav files into a dictionary whose keys are the expressions from the transition.json
        sound_list = ['introduction', 'click_balloon']
        self.sounds = {}
        for s in sound_list:
            self.sounds[s] = SoundLoader.load("./tablet_app/sounds/" + s + ".m4a")
        self.current_sound = None

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Messages from tablet to interaction
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def press_start_button (self):
        #child pressed the start button
        self.interaction.components['child'].on_action(["press_start_button"])

    def press_yes_button(self):
        # child pressed the yes button
        self.interaction.components['child'].on_action(["press_yes_button"])

    def press_treasure(self, treasure):
        # child selected treasure (1/2/3)
        print("press_treasure", treasure)
        self.interaction.components['child'].on_action(['press_treasure', treasure])

    def tangram_move(self, action):
        # child moved a tangram piece (json of all the pieces)
        print(self.name, 'tangram_mindset_app: tangram_move', action)
        self.interaction.components['child'].on_action(['tangram_move',action])

    def tangram_turn (self, action):
        # child turned a tangram piece (json of all the pieces)
        print(self.name, 'tangram_mindset_app: tangram_turn', action)
        self.interaction.components['child'].on_action(['tangram_turn', action])

    def check_solution(self, solution_json):
        # this function should not really be here
        print("tangram_mindset_app: check_solution", solution_json)
        return self.interaction.components['game'].game_facilitator.check_solution(solution_json)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Messages from interaction to tablet
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def first_screen(self):
        self.screen_manager.current = 'first_screen_room'

    def selection_screen(self, x):
        # Rinat: x is a list of tangrams from maor
        # you need to present all options with the tangram pieces
        print('x=',x)
        TangramGame.SCALE = round(Window.size[0] / 50)
        self.screen_manager.get_screen('selection_screen_room').init_selection_options(x=x,the_app=self)
        self.screen_manager.current = 'selection_screen_room'

    def tangram_screen(self, x):
        # Rinat: x is a single tangram from maor
        # you need to present it and allow game
        print("tangram_screen",x)
        TangramGame.SCALE = round(Window.size[0] / 40)
        self.screen_manager.get_screen('solve_tangram_room').init_task(x, the_app=self)
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