from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import IRightBodyTouch, ILeftBody
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.clock import Clock




sm = ScreenManager()
class LoginPage(Screen):
    username = ObjectProperty()
    password = ObjectProperty()
    login_cb = ObjectProperty()

    def on_pre_enter(self, *args):
        Clock.schedule_once(self.verificar_status_checkbox)
        

    def verificar_status_checkbox(self,*args):  #Si esta activo el cb se pone en automático en el MDTextField la contraseña y ususario
        archivo = r'assests\BD\usuarioData.csv'
        remember = 1   ##obtener_materias(archivo).remember_status(modo=2)  ##listo
        user = '421157110'
        pass_ = '16091997'
        if remember == 1:
            self.login_cb.active = True
            self.username.text = user
            self.password.text = pass_
        else:
            self.login_cb.active = False
            self.username.text = ""
            self.password.text = ""

    def remember_me(self): #mantener activo el checkbox
        pass
 
    def login(self):
        archivo = r'assests\BD\usuarioData.csv'
        if self.username.text == '421157110' and self.password.text == '16091997':
            sm.current = "firstwindow"
            self.username.text = ""
            self.password.text = ""
        else:
            print("Not here!")

class RightCheckbox(IRightBodyTouch, MDCheckbox): #Pertenece a la pantalla donde se muestran las actividades por materia es el checkbox que se muestra para las actividades por entregar o atrasadas
    '''Custom right container.'''
    screen_login = LoginPage()