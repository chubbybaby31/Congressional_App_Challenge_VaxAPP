import kivy
from kivy.core import text
import qrcode
kivy.require('1.0.6') # replace with your current kivy version !
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.image import Image





class MyApp(App):

    def build(self):
        img = qrcode.make('hello')
        type(img)  
        img.save("some_file.png")
      
        return Image(source='some_file.png')


if __name__ == '__main__':
    MyApp().run()