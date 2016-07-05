from interaction_control.component import *


class TabletComponent(Component):
    hourglass_widget = None
    app = None

    def first_screen(self):
        print(self.name, 'first_screen')
        self.current_state = 'first_screen'
        self.app.first_screen()

    def yes(self):
        print(self.name, 'yes in tablet')
        self.current_state = 'yes'
        self.current_state = "selection_screen_room"
        self.app.yes()

    def wait(self):
        #print(self.name, 'wait')
        self.current_state = 'wait'

    def selection_screen(self, x):
        print(self.name, 'selection_screen', x)
        self.current_state = 'selection_screen'
        self.app.selection_screen(x)

    def tangram_screen(self, x):
        print(self.name, 'tangram_screen', x)
        self.app.tangram_screen(x)
        self.current_state = 'tangram_screen'

    def hourglass_update(self, x):
        # print(self.name, 'hourglass update', x)
        # print ("self.hourglass_widget", self.hourglass_widget)
        if self.hourglass_widget:
            self.hourglass_widget.update_hourglass(x)
