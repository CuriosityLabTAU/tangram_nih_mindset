#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from interaction import *


class InteractionApp(App):
    def __init__(self, **kwargs):
        super(InteractionApp, self).__init__(**kwargs)
        self.interaction = Interaction()

    def build(self):
        layout = BoxLayout()
        layout.add_widget(Button(text='run', on_press=self.on_run))
        return layout

    def on_run(self, *args):
        print('run')
        self.interaction.load()
        self.interaction.show()
        self.interaction.run()

    def on_pause(self):
        return True

if __name__ == '__main__':
    InteractionApp().run()