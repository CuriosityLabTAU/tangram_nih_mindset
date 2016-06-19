from component import *


class GameComponent(Component):
    def generate_selection(self):
        print(self.name, 'generate selection')
        self.current_param = ['T1', 'T2', 'T3']
        self.current_state = 'generate_selection'

    def tangram_selected(self, action):
        print(self.name, 'tangram selected', action)
        selected_tangram = None
        while not selected_tangram and action:
            if isinstance(action, int):
                selected_tangram = action
            elif isinstance(action, list):
                action = action[0]
        if selected_tangram:
            self.current_param = self.current_param[selected_tangram]
        self.current_state = 'tangram_selected'

    def tangram_moved(self, action):
        print(self.name, 'tangram moved', action)

    def tangram_turned(self):
        print(self.name, 'tangram turned')
        self.win()

    def win(self):
        print(self.name, 'win')
        self.current_state = 'win'
