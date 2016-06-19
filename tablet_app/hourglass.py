from interaction_control.component import *


class HourglassComponent(Component):
    update_interval = 0.25
    max_counter = 120
    widget = None

    def start(self):
        print(self.name, 'start')
        self.current_state = 'update'
        self.current_param = self.max_counter

        Clock.schedule_interval(self.update, self.update_interval)
        print(self.widget)
        if self.widget:
            self.widget.start_hourglass()

    def stop(self):
        print(self.name, 'stopped')
        self.current_state = 'idle'
        Clock.unschedule(self.update)
        if self.widget:
            self.widget.stop_hourglass()

    def update(self, *args):
        print('houglass update. remaining: ', self.current_param, ' seconds...')
        self.current_param -= self.update_interval
        if self.widget:
            self.widget.update_hourglass(float(self.current_param) / float(self.max_counter))

        if self.current_param <= 0:
            self.current_state = 'finish'
            self.current_param = 0
            return False

    def after_called(self):
        if self.current_state is not 'update':
            self.current_state = 'idle'
