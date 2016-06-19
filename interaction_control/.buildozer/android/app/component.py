from kivy.clock import Clock
import numpy as np


class Component:
    def __init__(self, name_in):
        self.actors = {}
        self.name = name_in
        self.current_state = 'idle'

    def add_transition(self, state, target, fun, value):
        if state not in self.actors:
            self.actors[state] = {}
        if target not in self.actors[state]:
            self.actors[state][target] = {}
        self.actors[state][target][fun] = value

    def show(self):
        print(self.name, self.actors)

    def run(self):
        print(self.name, 'running ...')
        Clock.schedule_interval(self.resolve, 0.5)
        print(self.name, 'finished!')

    def resolve(self, *args):
        print(self.name, 'resolving ', args)
        if self.current_state in self.actors:
            for target,funs in self.actors[self.current_state].items():
                Q = np.zeros([len(funs)])
                for k in range(0, len(funs.keys())):
                    Q[k] = funs[funs.keys()[k]]
                print(target, Q)


