
import json
import thread
from component import *


class Interaction:

    def __init__(self):
        self.components = {}

    def run(self):
        try:
            for c in self.components.values():
                thread.start_new_thread(c.run)
        except:
            print "Error: unable to start thread"

    def show(self):
        for c in self.components.values():
            c.show()

    def load(self):
        with open('transitions.json') as data_file:
            data = json.load(data_file)
        for t in data['transitions']:
            source, state, target, fun, value = t.split(':')
            if source not in self.components.keys():
                self.components[source] = Component(source)
            if target not in self.components.keys():
                self.components[target] = Component(target)
            self.components[source].add_transition(state, target, fun, value)
