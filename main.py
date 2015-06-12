# -*- coding: utf-8 -*-

import sys
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.image import  Image 
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.screenmanager import NoTransition

from functools import partial 

import pdb
import sys
import random

MODE_HOME = 0
MODE_GAME = 1

NOTIME = 0
EASY = 4
MEDIUM = 2
HARD = 1

colors = ['green', 'red', 'purple']
shapes = ['oval', 'diamond', 'squiggle']
numbers = [1,2,3]
shades = ['filled','shaded', 'empty']

class ImgBtn(ButtonBehavior, Image):
    '''Creates an image with the buttonbehavior of a Kivy button, so you can click on objects and they launch popups, etc'''
   
    def dispPop(self):
        infoPopUp().open()

class infoPopUp(Popup):
    '''Creates an infopopup. In our kivy file, we define an infopopup as a popup 
    with no text input, and that has a button that closes the popup when pressed.
    As you can guess, they're meant to provide information.'''
    pass

class HomeScreen(Screen):
    def change_mode(self,mode):
        print mode

class GameScreen(Screen):
    def __init__(self, name="game"):
        Screen.__init__(self, name="game")

class BackgroundScreenManager(ScreenManager):#creating a new screen manager so we can have lovely background images!
    bk_img = ObjectProperty()
        
class RaApp(App):

    def build(self): #Establishses a screen manager with all of the screens we use for navigation, names all of the screens
        global app
        app = self

        self.home_screen = HomeScreen(name = 'home')
        self.game_screen = GameScreen(name = 'game')

        sm = BackgroundScreenManager()
        sm.transition = NoTransition()
        sm.add_widget(self.home_screen)
        sm.add_widget(self.game_screen)
        sm.current = 'game'
        return sm
   
        
ragame = RaApp()
ragame.build()
#initialize widgets related to conditionals for the door
ragame.run()
