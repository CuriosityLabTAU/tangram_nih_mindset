from component import *


class HourglassComponent(Component):
    update_interval = 1

    def start(self):
        print(self.name, 'start')
        self.current_state = 'update'
        self.current_param = 120
        Clock.schedule_interval(self.update, self.update_interval)

    def stop(self):
        print(self.name, 'stopped')
        self.current_state = 'idle'
        Clock.unschedule(self.update)

    def update(self, *args):
        # print('houglass update. remaining: ', self.current_param, ' seconds...')
        self.current_param -= self.update_interval
        if self.current_param <= 0:
            self.current_state = 'finish'
            self.current_param = 0

    def after_called(self):
        if self.current_state is not 'update':
            self.current_state = 'idle'
