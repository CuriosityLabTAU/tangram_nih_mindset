from interaction_control.component import *
from game_facilitator import *


class GameComponent(Component):
    game_facilitator = None

    def generate_selection(self, *args):
        print(self.name, 'generate selection', args)
        T = []
        if self.game_facilitator:
            T = self.game_facilitator.generate_tangram_options()
        self.current_param = T
        self.current_state = 'generate_selection'

    def tangram_selected(self, action):
        print(self.name, 'tangram selected', action)
        selected_tangram = action
        self.game_facilitator.tangram_selected(selected_tangram)
        self.current_param = self.current_param[selected_tangram]
        self.current_state = 'tangram_selected'

    def tangram_changed(self, x):
        print(self.name, 'tangram_changed', x)
        if self.game_facilitator.check_solution(x):
            self.win()

    def tangram_moved(self, action):
        print(self.name, 'game.py: tangram moved', action)
        if self.game_facilitator.check_solution(action):
            self.win()


    def tangram_turned(self, action):
        print(self.name, 'game.py: tangram turned', action)
        if self.game_facilitator.check_solution(action):
            self.win()

    def win(self):
        print(self.name, 'game.py: win')
        self.game_facilitator.update_game_result('S')
        self.current_state = 'win'

    def finished(self, action):
        print(self.name, 'game.py: finished')
        self.game_facilitator.update_game_result('F')
