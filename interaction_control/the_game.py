from component import *


class GameComponent(Component):
    current_player = 'robot'

    def generate_selection(self):
        print(self.name, 'generate selection')
        self.current_param = 'T1, T2, T3'
        self.current_state = 'generate_selection'

    def tangram_selected(self, action):
        print(self.name, 'tangram selected', action)

    def tangram_moved(self, action):
        print(self.name, 'tangram moved', action)

    def tangram_turned(self):
        print(self.name, 'tangram turned')
        self.win()

    def win(self):
        if self.current_player == 'robot':
            self.current_state = 'robot_win'
        else:
            self.current_state = 'child_win'