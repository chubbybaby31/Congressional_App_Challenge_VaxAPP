import qrcode
# from host import Host
# import kivy
# from kivy.app import App
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button
# from kivy.uix.image import Image
# import os
# from _thread import start_new_thread

class Profile():
    def __init__(self, name, vaccinated, company, img=None):
        self.name = name
        self.vaccinated = vaccinated
        self.company = company
        self.img = img

    def transmit_string(self):
        return "Name: " + str(self.name) + "; Vaccinated: " + str(self.vaccinated) + "; Vaccination Company: " + str(self.company)

    def displayProfile(self):
        print("Name: " + self.name + "\nVaccinated: " + str(self.vaccinated) + "\nVaccination Company: " + self.company)
        img = qrcode.make("Name " + self.name + "\n Vaccinated " + str(self.vaccinated) + "\nVaccination Company " + self.company)
        img.save("some_file.jpg")
        return "some_file.jpg"

    def file_string(self):
        return str(self.name) + ";*|" + str(self.vaccinated) + ";*|" + str(self.company)

# class childApp(GridLayout):
#     def __init__(self, **kwargs):
#         super(childApp, self).__init__()
#         self.cols = 2
#         self.addWidgets()
#
#     def addWidgets(self):
#         self.add_widget(Label(text='Name', size_hint = (0.5, 0.25)))
#         self.name = TextInput(size_hint = (2, 0.25))
#         self.add_widget(self.name)
#
#         self.add_widget(Label(text='company', size_hint = (0.5, 0.25)))
#         self.company = TextInput(size_hint = (2, 0.25))
#         self.add_widget(self.company)
#
#         self.press = Button(text = 'Done', size_hint = (0.25, 0.25))
#         self.press.bind(on_press = self.submit)
#         self.add_widget(self.press)
#
#     def submit(self, instance):
#         self.clear_widgets()
#         p = Profile(self.name.text, True, self.company.text)
#         # self.addWidgets()
#         # self.add_widget(Image(source=p.displayProfile()))
#         h = Host(p)
#         start_new_thread(h.start_hosting, ())
#
# class parentApp(App):
#     def build(self):
#         return childApp()
#
# if __name__ == "__main__":
#     parentApp().run()
        