from component import *
import time


class RobotComponent(Component):
    def run_function(self, action):
        self.express(action)

    def express(self, action):
        print(self.name, action[0], action[1:])
        self.current_state = action[0]
        self.current_param = action[1:]
        time.sleep(1)

    def after_called(self):
        if 'done' in self.current_param:
            self.current_state = 'idle'
            self.current_param = None