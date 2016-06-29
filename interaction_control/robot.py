from component import *
import time
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

    def run_function(self, action):
        print(self.name, action[0], action[1:])
        try:
            if action[1]:
                getattr(self, action[0])(action[1])
            else:
                getattr(self, action[0])()
            return True
        except:
            self.express(action)
        return False

    def express(self, action):
        self.current_state = 'express'
        if action[1]:
            self.current_param = action[1:]

        if KC.client.connection:
            data = [self.current_state, self.current_param]
            data = {'robot': data}
            KC.client.send_message(str(json.dumps(data)))

        if self.app:
            self.app.robot_express(action)

    def after_called(self):
        if self.current_param:
            if isinstance(self.current_param, list):
                if 'done' in self.current_param:
                    self.current_state = 'idle'
                    self.current_param = None

    def set_playing(self, action):
        self.current_param = action[1:]
        self.whos_playing = action[0]
        print(self.whos_playing, self.current_param)

    def set_selection(self, action):
        # set the possible treasures to select from
        if self.whos_playing == 'demo':
            self.current_param = 1
        if self.whos_playing == 'robot':
            self.current_state = 'select_treasure'
            self.current_param = 2

    def win(self):
        print(self.name, self.whos_playing, 'wins!')
        if self.whos_playing == 'child':
            self.run_function(['child_win_happy', None])
        else:
            self.run_function(['robot_win_happy', None])

    def play_game(self, action):
        print(self.whos_playing, 'playing the game')

    def comment_selection(self, action):
        if self.whos_playing == "child":
            print(self.name, 'commenting on selection ', action)

    def comment_move(self, action):
        if self.whos_playing == "child":
            print(self.name, 'commenting on move ', action)

    def comment_turn(self, action):
        if self.whos_playing == "child":
            print(self.name, 'commenting on turn ', action)

    def finished_expression(self, action):
        self.current_param = None
        self.current_state = action
        print(self.name, action, self.current_state)

    def data_received(self, data):
        # if data signals end of speech
        # call: self.finished_expression(action)
        print(self.name, data)
