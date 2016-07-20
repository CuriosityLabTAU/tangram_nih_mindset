from component import *
import time
from agent import *
import json
is_logged = True
try:
    from kivy_communication import *
except:
    print('no logging')
    is_logged = False


class RobotComponent(Component):
    whos_playing = None
    app = None
    expression = None
    agent = Agent()
    current_tangram = None

    def run_function(self, action):
        print(self.name, 'run_function', action[0], action[1:])
        if action[0] == action[1:]:
            print('weird')
            return False
        try:
            if action[1]:
                getattr(self, action[0])(action[1])
            else:
                getattr(self, action[0])()
            return True
        except:
            if not isinstance(sys.exc_info()[1], AttributeError):
                print ("unexpected error:",sys.exc_info())
            self.express(action)
        return False

    def express(self, action):
        self.current_state = 'express'
        self.expression = action[0]
        if len(action) > 1:
            self.current_param = action[1:]

        if KC.client.connection:
            data = [self.current_state, self.expression]
            data = {'robot': data}
            KC.client.send_message(str(json.dumps(data)))

        if self.app:
            self.app.robot_express(self.expression)

    def after_called(self):
        if self.current_param:
            if isinstance(self.current_param, list):
                if 'done' in self.current_param:
                    self.current_state = 'idle'

    def set_playing(self, action):
        self.current_param = action[1:]
        self.whos_playing = action[0]
        print(self.whos_playing, self.current_param)

    def select_treasure(self):
        the_selection = self.agent.set_selection()
        print(self.name, 'select_treasure', the_selection, self.current_param)
        self.current_tangram = self.current_param[0][the_selection]
        self.current_state = 'select_treasure'
        self.current_param = the_selection
        self.agent.finish_moves() #  indication to the agent that the last game is finished. agent clears the last solution

    def select_move(self, x):
        print(self.name, 'select_move', x)
        self.current_state = 'select_move'
        self.current_param = self.current_tangram[0]
        move = self.agent.play_move(x)
        self.current_param = move

    # def set_selection(self, action):
    #     print('robot set selection', action)
    #     # self.current_param = action[1:]
    #     # set the possible treasures to select from
    #     # select 1 for demo, 2 for robot
    #     # waiting for Maor's algorithm
    #     if self.whos_playing == 'demo':se
    #         self.current_param = 1
    #         self.current_state = 'idle'
    #     if self.whos_playing == 'robot':
    #         self.current_state = 'select_treasure'
    #         self.current_param = 2

    def win(self):  # called only in tutorial
        print(self.name, self.whos_playing, 'wins!')
        if self.whos_playing == 'child':
            self.run_function(['child_win', None])
        else:
            self.run_function(['robot_win', None])

    def child_win(self):
        print(self.name, self.whos_playing, 'child_win')
        self.agent.record_child_result('S')
        self.current_state = 'child_win'

    def child_lose(self):
        print(self.name, self.whos_playing, 'child_lose')
        self.agent.record_child_result('F')
        self.current_state = 'child_lose'

    def play_game(self, action):
        print(self.whos_playing, 'playing the game', action)
        self.current_state = 'play_game'
        self.agent = Agent()
        seq = self.agent.solve_task(action[1][0]) #  solve the selected task and return a seq of moves in json string
        #self.current_param = action[1]
        self.current_param = seq

    # def comment_selection(self, action):
    #     if self.whos_playing == "child":
    #         print(self.name, 'commenting on selection ', action)

    # def comment_move(self, action):
    #     if self.whos_playing == "child":
    #         print(self.name, 'commenting on move ', action)

    # def comment_turn(self, action):
    #     if self.whos_playing == "child":
    #         print(self.name, 'commenting on turn ', action)

    def finished_expression(self, action):
        # self.current_param = None
        self.current_state = action
        print('finished expression:', self.name, action, self.current_state)

    def data_received(self, data):
        # if data signals end of speech
        # call: self.finished_expression(action)
        print(self.name, data)
        self.finished_expression(data)

    def child_selection(self, x):
        print(self.name, 'child selected', x)
        self.agent.record_child_selection(x)
