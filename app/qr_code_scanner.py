from __future__ import print_function
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy_garden.xcamera.xcamera import XCamera
from kivy.uix.button import Button
import os

class QrCodeScanner():
    def __init__(self, im):
        import cv2
        if im == None:
            self.im_name, self.im = self.find_image()
        else:
            self.im = cv2.imread(im)
            self.im_name = im
        self.data = self.decode()
        self.delete_image()

    def find_image(self):
        import cv2
        dirs = os.listdir()
        for dir in dirs:
            if '.jpg' in str(dir):
                return str(dir), cv2.imread(str(dir))

    def delete_image(self):
        os.remove(self.im_name)

    def decode(self):
        import pyzbar.pyzbar as pyzbar
        decodedObjects = pyzbar.decode(self.im)
        for obj in decodedObjects:
            print('Data : ', obj.data,'\n')
            return obj.data

class Photo(FloatLayout):
    def __init__(self):
        self.add_widgets()

    def add_widgets(self):
        self.camera = XCamera(on_picture_taken = self.picture_taken)
        self.add_widget(self.camera)

        self.change_cam_button = Button(text = "change cam", size_hint = (0.2, 0.1), pos_hint = {"center_x": 0.5}, on_release = self.change_cam)
        self.add_widget(self.change_cam_button)

    def picture_taken(self, instance, image_name):
        self.image_name = image_name
        QrCodeScanner(image_name)

    def change_cam(self, instance):
        print("done")
        if self.camera.index == 0:
            self.camera.index = int(self.camera.index) + 1
        elif self.camera.index == 1:
            self.camera.index = int(self.camera.index) - 1
        else:
            self.camera.index = self.camera.index