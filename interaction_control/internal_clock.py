from component import *
from kivy.clock import Clock


class ClockComponent(Component):
    def run_function(self, action):
        if action[0] == 'stop':
            self.stop()
        else:
            how_long = float(action[1])
            print(self.name, 'wait for ', how_long, ' seconds')
            self.current_state = action[0]
            self.current_param = how_long
            Clock.schedule_once(self.prompt, how_long)

    def prompt(self, *args):
        print(self.name, 'prompt', self.current_state)
        self.current_state = 'prompt_' + self.current_state
        self.current_param = None

    def stop(self):
        print(self.name, 'stop')
        self.current_state = 'idle'
