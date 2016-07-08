import json
from component import *


class Interaction:
    data = None
    components = {}
    current_interaction = None

    def __init__(self):
        pass

    def __init__(self, component_list=None):
        # list of tuples (name, class_name)
        if component_list:
            for c in component_list:
                name = c[0]
                class_name = c[1]
                try:
                    module = __import__(name)
                except:
                    module = __import__('interaction_control.' + name)
                class_ = getattr(module, class_name)
                self.components[name] = class_(self, name)

    def run(self, start):
        for c in self.components.values():
            c.run()
        self.components[start[0]].current_state = start[1]

    def show(self):
        for c in self.components.values():
            c.show()

    def load(self, filename='transitions.json'):
        with open(filename) as data_file:
            self.data = json.load(data_file)
        self.current_interaction = 0

    def next_interaction(self):
        the_interaction = self.data['sequence'][self.current_interaction]
        the_data = self.data[the_interaction]

        # first nonify all general param
        for c_key, c_val in self.components.items():
            if c_key in the_data.keys():
                c_val.general_param = {}
                for i in the_data[c_key]:
                    i_str = i.split(':')
                    c_val.general_param[i_str[0]] = i_str[1]
            else:
                c_val.general_param = None


        for t in the_data['transitions']:
            info = str(t).split(':')
            source, state, target, fun, value = info[0:5]
            param = None
            if len(info) == 6:
                param = info[5]
            elif len(info) > 6:
                param = info[5:]
            if source not in self.components.keys():
                self.components[source] = Component(self, source)
            if target not in self.components.keys():
                self.components[target] = Component(self, target)
            self.components[source].add_transition(state, target, fun, value, param)
        start = the_data['start'].split(':')
        start = [str(x) for x in start]
        print("starting", the_interaction)
        self.run(start)
