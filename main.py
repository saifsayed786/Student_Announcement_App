from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
import os
from gtts import *
from kivy.core.audio import SoundLoader


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "sinfo"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"


class StudentInfo(Screen):
	candidateName=ObjectProperty(None)
	calledBy=ObjectProperty(None)
	destination=ObjectProperty(None)
	sound=None


	def textTOspeech(self):
		self.a=self.candidateName.text+" You have been called by "+self.calledBy.text+" in "+self.destination.text
		print(self.a)
		self.text1=self.a
		self.language="en"
		self.filename="my.mp3"
		audio=gTTS(text=self.text1,lang=self.language,slow=False)
		audio.save(self.filename)
		

	def play_text(self):
		self.get_sound()

		if not self.sound:
			pass
		else:
			self.sound.play()



	def get_sound(self, fl = 'my.mp3'):		
		self.sound = SoundLoader.load(fl)

		
	def reset(self):
		self.candidateName.text=""
		self.calledBy.text=""
		self.destination.text=""
	


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main"),StudentInfo(name="sinfo")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"



class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
