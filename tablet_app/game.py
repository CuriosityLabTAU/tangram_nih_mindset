from interaction_control.component import *
from game_facilitator import *


class GameComponent(Component):
    game_facilitator = None

    def generate_selection(self):
        print(self.name, 'generate selection')
        T = []
        if self.game_facilitator:
            T = self.game_facilitator.generate_tangram_options()
        self.current_param = T
        self.current_state = 'generate_selection'

    def tangram_selected(self, action):
        print(self.name, 'tangram selected', action)
        selected_tangram = None
        while not selected_tangram and action:
            if isinstance(action, int):
                selected_tangram = action
                self.game_facilitator.tangram_selected(action)
            elif isinstance(action, list):
                action = action[0]
        if selected_tangram:
            self.current_param = self.current_param[selected_tangram-1]
        self.current_state = 'tangram_selected'


    def tangram_moved(self, action):
        print(self.name, 'game.py: tangram moved', action)

    def tangram_turned(self, action):
        print(self.name, 'game.py: tangram turned')
        self.win()

    def win(self):
        print(self.name, 'game.py: win')
        self.current_state = 'win'
