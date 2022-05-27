from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
import mimetypes
from kivy.core.window import Window
import os
import ffmpeg

mimetypes.init()
def get_extensions_for_type(general_type):
    for ext in mimetypes.types_map:
        if mimetypes.types_map[ext].split('/')[0] == general_type:
            yield ext


global image_formats
images_formats = tuple(get_extensions_for_type('image'))

import ffmpeg
def doCrop(sizex,sizey,ratio,ksize):
    r_folder = os.path.join(os.path.dirname(__file__) , "Resizer-Results")
    print(r_folder)
    if not os.path.exists(r_folder):
        os.mkdir(r_folder)
    for i in items:
        img = ffmpeg.input(i)
        #if ratio:
            #img = ffmpeg.filter(img,"scale",str(sizex)+":"+str(sizey)+":force_original_aspect_ratio=decrease")
        img = ffmpeg.filter(img,"pad",str(sizex)+":"+str(sizey)+":(ow-iw)/2:(oh-ih)/2)")
        img =  ffmpeg.output(img, str(r_folder) + "//"+ str(i))
        ffmpeg.run(img)





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


class ResizeWindow(Screen):
    sizex = ObjectProperty(None)
    sizey = ObjectProperty(None)
    ratio = ObjectProperty(None)
    ksize = ObjectProperty(None)

    def loginBtn(self):
        try:
            doCrop(int(self.sizex.text),int(self.sizey.text),self.ratio.active,self.ksize.active)
        except Exception as e:
            print(e)
        print(items)

        '''
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()
        '''

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    files = ObjectProperty(None)
    selected =  ObjectProperty(None)
    current = ""

    def resize_settings(self):
        sm.current = "resize"


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


kv = Builder.load_file("test.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [ResizeWindow(name="resize"), MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)
sm.current = "main"





class MyMainApp(App):
    global items
    items = []
    def build(self):
        Window.bind(on_dropfile=self._on_file_drop)
        return sm
    def recursive(self, path):
                result = []
                for subdir, dirs, files in os.walk(path):
                        for file in files:
                                result.append(os.path.join(subdir, file))
                return result

    def _on_file_drop(self, window, file_path):
            global items
            files = []
            file_path = bytes.decode(file_path)
            if os.path.isdir(str(file_path)):
                files.extend(self.recursive(file_path))
            items = [file for file in files if file.lower().endswith(images_formats)]
            print(items)
            return



if __name__ == "__main__":
    MyMainApp().run()
