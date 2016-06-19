from component import *


class ChildComponent(Component):
    def run_function(self, action):
        if action[0] == 'action':
            self.on_action(action[1:][0])
        else:
            print(self.name, 'wait for ', action[0])
            self.current_state = action[0]
            self.current_param = action[1:]

    def on_action(self, action):
        print(self.name, 'action ', action)
        self.current_state = action[0]
        self.current_param = action[1:]