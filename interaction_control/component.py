from kivy.clock import Clock
is_logged = True
try:
    from kivy_communication import *
except:
    print('no logging')
    is_logged = False


class Component:
    def __init__(self, inter, name_in):
        self.interaction = inter
        self.actors = {}
        self.name = name_in
        self.current_state = 'idle'
        self.current_action = {}
        self.current_param = None

    def add_transition(self, state, target, fun, value, param=None):
        if state not in self.actors:
            self.actors[state] = {}
        if target not in self.actors[state]:
            self.actors[state][target] = {}
        self.actors[state][target][fun] = (value, param)

    def show(self):
        print(self.name, self.actors)

    def run(self):
        print(self.name, 'running ...')
        Clock.schedule_interval(self.resolve, 0.5)

    def resolve(self, *args):
        # print('resolve', self.name, self.current_state)
        self.current_action = {}
        if self.current_state != 'idle':
            called = False
            if self.current_state in self.actors:
                for target, funs in self.actors[self.current_state].items():
                    Q = []
                    for value in funs.values():
                        Q.append(float(value[0]))
                    selected_action = self.select_action(Q)
                    selected_function = funs.keys()[selected_action]
                    selected_param = funs.values()[selected_action][1]
                    self.current_action[target] = [selected_function, selected_param]
                for target,action in self.current_action.items():
                    if target != self.name:     # run own functions last
                        if action[1]:
                            if isinstance(action[1], list):
                                for k in range(0, len(action[1])):
                                    if action[1][k] == 'x':
                                        action[1][k] = self.current_param
                            else:
                                if action[1] == 'x':
                                    action[1] = self.current_param
                        self.log_data(target=target, action=action)
                        self.interaction.components[target].run_function(action)
                        called = True
                if self.name in self.current_action.keys():
                    action = self.current_action[self.name]
                    if action[1] and action[1] == 'x':
                        action[1] = self.current_param
                    self.log_data(action=action)
                    self.run_function(action)
                    called = True

                self.current_action = {}
            if called:
                self.after_called()

    def after_called(self):
        self.current_state = 'idle'

    def run_function(self, action):
        print("run_function ", action)
        try:
            if action[1]:
                print("run_function, if ", action)
                getattr(self, action[0])(action[1:])
            else:
                print("run_function, else ", action)
                getattr(self, action[0])()
            return True
        except:
            print('No function: ', self.name, action)
        return False


    def select_action(self, Q):
        # winner takes all
        return Q.index(max(Q))

    def log_data(self, target=None, action=None):
        if is_logged:
            KL.log.insert(action=LogAction.data, obj=self.name, comment=[self.current_state, self.current_param, target, action])
