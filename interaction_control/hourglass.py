from interaction_control.component import *


class HourglassComponent(Component):
    update_interval = 0.25
    max_counter = 120
    the_clock = None

    def end_run(self):
        Clock.unschedule(self.event)
        Clock.unschedule(self.the_clock)

    def start(self):
        print(self.name, 'start')
        self.current_state = 'update'
        self.current_param = [self.max_counter, self.max_counter]
        self.the_clock = Clock.schedule_interval(self.update, self.update_interval)

    def stop(self):
        print(self.name, 'stopped')
        self.current_state = 'idle'
        Clock.unschedule(self.the_clock)

    def update(self, *args):
        self.current_param[0] -= self.update_interval

        if self.current_param[0] <= 0:
            self.current_state = 'finish'
            self.current_param[0] = 0
            return False

    def after_called(self):
        if self.current_state is not 'update':
            self.current_state = 'idle'
