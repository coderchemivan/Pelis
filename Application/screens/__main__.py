from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from login import LoginPage


class WindowManager(ScreenManager):
    pass


class TestNavigationDrawer(MDApp):
    def build(self):
        Window.size = (1000, 600)
        self.title = "Gestor de tareas"
        Builder.load_file(r'C:\Users\ivan_\OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO\Desktop\repositorios\Pelis\Application\kivy_files/main.kv')
        sm = ScreenManager()
        sm.add_widget(LoginPage(name='login_page'))
        return sm
TestNavigationDrawer().run()






