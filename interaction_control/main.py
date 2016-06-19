#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from interaction import *
from tablet import *
from robot import *
from child import *
from internal_clock import *
from hourglass import *
from the_game import *


class InteractionApp(App):
    def __init__(self, **kwargs):
        super(InteractionApp, self).__init__(**kwargs)
        self.interaction = Interaction()

    def build(self):
        layout = BoxLayout()
        layout.add_widget(Button(text='run', on_press=self.on_run))

        panel = BoxLayout()
        panel.add_widget(Button(text='start', on_press=self.on_start_button))
        panel.add_widget(Button(text='yes', on_press=self.on_yes_button))
        panel.add_widget(Button(text='no', on_press=self.on_no_button))

        layout.add_widget(panel)
        return layout

    def on_run(self, *args):
        print('run')
        self.interaction.components['tablet'] = TabletComponent(self.interaction, 'tablet')
        self.interaction.components['robot'] = RobotComponent(self.interaction, 'robot')
        self.interaction.components['child'] = ChildComponent(self.interaction, 'child')
        self.interaction.components['internal_clock'] = ClockComponent(self.interaction, 'internal_clock')
        self.interaction.components['hourglass'] = HourglassComponent(self.interaction, 'hourglass')
        self.interaction.components['game'] = GameComponent(self.interaction, 'game')
        self.interaction.load()
        self.interaction.show()
        self.interaction.run()

    def on_start_button(self, *args):
        self.interaction.components['child'].on_action('press_start_button')

    def on_yes_button(self, *args):
        self.interaction.components['child'].on_action('press_yes_button')

    def on_no_button(self, *args):
        self.interaction.components['child'].on_action('no')

    def on_pause(self):
        return True

if __name__ == '__main__':
    InteractionApp().run()