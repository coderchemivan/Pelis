from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen


class LoginPage(Screen):
    username = ObjectProperty()
    password = ObjectProperty()
    login_cb = ObjectProperty()

    def on_pre_enter(self, *args):
        pass