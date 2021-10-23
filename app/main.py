import kivy.utils

from client import Client
from host import Host
from profile import Profile
from qr_code_scanner import QrCodeScanner
import qrcode
import os
from _thread import start_new_thread

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy_garden.xcamera.xcamera import XCamera
from kivy.uix.image import Image
from kivy.core.window import Window

class Menu(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        app = App.get_running_app()
        print("app.directory = ", app.directory)
        print("app.user_data_dir = ", app.user_data_dir)

        global configfilename, user_data_dir_path
        configfilename = os.path.join(app.user_data_dir, 'geo-esp-train.cfg')
        user_data_dir_path = app.user_data_dir  # Used for other data files.
        self.hosting = False
        self.c = Client()
        if self.get_profile_text() == "None":
            self.valid_profile = False
        else:
            self.valid_profile = True
            name, vaccinated, company = self.get_profile_text()
            self.profile = Profile(name, bool(vaccinated), company)

        self.title_font_size = 26
        self.font_size = 18
        self.yellow = kivy.utils.get_color_from_hex('#EDE5A6')
        self.lightgreen = kivy.utils.get_color_from_hex('#B2D3A8')
        self.green = kivy.utils.get_color_from_hex('#52B788')
        self.darkgreen = kivy.utils.get_color_from_hex('#498467')
        self.red = kivy.utils.get_color_from_hex('#592941')
        self.add_widgets_menu()

    def add_widgets_menu(self):
        self.clear_widgets()
        self.add_widget(Label(text="Menu", pos_hint={"center_x": 0.5, "center_y": 0.9}, font_size=self.title_font_size, bold=True, color=self.red))
        if self.valid_profile:
            if self.hosting:
                self.hosting_status = Label(text = "Currently Hosting Profile", size_hint = (0.2, 0.1), pos_hint = {"center_x": 0.5, "center_y": 0.8}, font_size=self.font_size, color=self.red)
            else:
                self.hosting_status = Label(text = "Not Hosting Profile", size_hint = (0.2, 0.1), pos_hint = {"center_x": 0.5, "center_y": 0.8}, font_size=self.font_size, color=self.red)
            self.add_widget(self.hosting_status)
        else:
            profile_status = Label(text = "Profile Not Yet Created", size_hint = (0.2, 0.1), pos_hint = {"center_x": 0.5, "center_y": 0.8}, font_size=self.font_size, color=self.red)
            self.add_widget(profile_status)


        edit_profile_button = Button(text = "View Profile", size_hint = (0.3, 0.15), pos_hint = {"center_x": 0.5, "center_y": 0.66}, on_release = self.profile_menu, background_color=self.green)
        self.add_widget(edit_profile_button)

        host_profile_button = Button(text = "Host Profile", size_hint = (0.3, 0.15), pos_hint = {"center_x": 0.5, "center_y": 0.49}, on_release = self.host_profile_menu, background_color=self.darkgreen)
        self.add_widget(host_profile_button)

        scan_profile_button = Button(text="Scan for Profiles", size_hint = (0.3, 0.15), pos_hint={"center_x": 0.5, "center_y": 0.32}, on_release=self.scan_profiles_menu, background_color=self.green)
        self.add_widget(scan_profile_button)

        scan_qr_code_button = Button(text = "Scan QR-Code", size_hint = (0.3, 0.15), pos_hint={"center_x": 0.5, "center_y": 0.15}, on_release=self.scan_qr_code_menu, background_color=self.darkgreen)
        self.add_widget(scan_qr_code_button)

    def back_to_menu(self, instance):
        self.clear_widgets()
        self.add_widgets_menu()

    def add_widgets_profile(self):
        self.clear_widgets()
        title = Label(text="Profile", pos_hint={"center_x": 0.5, "center_y": 0.9}, font_size=self.title_font_size, bold=True, color=self.red)
        self.add_widget(title)

        name, vaccinated, company = self.get_profile_text()
        profile_label = Label(text="Name: {}\nVaccinated: {}\nVaccination Company: {}".format(name, vaccinated, company), pos_hint={"center_x":0.5, "center_y":0.75}, font_size=self.font_size, color=self.red)
        self.add_widget(profile_label)

        im_exists = False

        dirs = os.listdir()
        for dir in dirs:
            if "profile_qrcode.png" in str(dir):
                im_exists = True

        if not im_exists:
            im = qrcode.make(self.profile.transmit_string())
            im.save('profile_qrcode.png')

        self.qr_code_profile = Image(source = 'profile_qrcode.png', size_hint=(0.4,0.4), pos_hint={"center_x":0.5, "center_y":0.45})
        self.add_widget(self.qr_code_profile)

        edit_profile_button = Button(text="Edit Profile", size_hint=(0.3, 0.15), pos_hint={"center_x": 0.33, "center_y": 0.1}, on_release=self.edit_profile, background_color=self.green)
        self.add_widget(edit_profile_button)

        back_button = Button(text="Back", size_hint=(0.3, 0.15), pos_hint={"center_x": 0.67, "center_y": 0.1}, on_release=self.back_to_menu, background_color=self.darkgreen)
        self.add_widget(back_button)

    def get_profile_text(self):
        try:
            with open("Profile.txt", "r") as f:
                content = f.read()
                profile = content.split(";*|")
                name = profile[0]
                vaccinated = profile[1]
                company = profile[2]
                return name, vaccinated, company
        except:
            return "None"


    def add_widgets_edit_profile(self):
        self.clear_widgets()
        self.add_widget(Label(text="Edit Profile", pos_hint={"center_x":0.5, "center_y":0.85}, font_size=self.title_font_size, bold=True, color=self.red))

        self.add_widget(Label(text='Name', size_hint=(0.2, 0.1), pos_hint={"center_x": 0.33, "center_y": 0.6}, font_size=self.font_size, color=self.red))
        self.name = TextInput(size_hint = (0.3, 0.15), pos_hint={"center_x": 0.67, "center_y": 0.6})
        self.add_widget(self.name)

        self.add_widget(Label(text='Vaccination Company', size_hint = (0.2, 0.1), pos_hint={"center_x": 0.33, "center_y": 0.4}, font_size=self.font_size, color=self.red))
        self.company = TextInput(size_hint = (0.3, 0.15), pos_hint={"center_x": 0.67, "center_y": 0.4})
        self.add_widget(self.company)

        done_button = Button(text='Done', size_hint = (0.3, 0.15), pos_hint={"center_x": 0.5, "center_y": 0.1}, on_release=self.update_profile, background_color=self.green)
        self.add_widget(done_button)

    def update_profile(self, instance):
        self.profile = Profile(self.name.text, True, self.company.text)
        with open("Profile.txt", "w") as f:
            f.truncate(0)
            f.write(self.profile.file_string())
            f.close()
        self.add_widgets_profile()

    def profile_menu(self, instance):
        self.clear_widgets()
        try:
            with open("Profile.txt", "r") as f:
                content = f.read()
                if content:
                    self.add_widgets_profile()
                else:
                    self.add_widgets_edit_profile()
                f.close()
        except:
            self.add_widgets_edit_profile()

    def edit_profile(self, instance):
        self.clear_widgets()
        self.add_widgets_edit_profile()

    def host_profile_menu(self, instance):
        self.clear_widgets()
        self.add_host_widgets()

    def add_host_widgets(self):
        self.clear_widgets()
        self.add_widget(Label(text="Host Profile", pos_hint={"center_x": 0.5, "center_y": 0.85}, font_size=self.title_font_size, bold=True,color=self.red))

        if self.valid_profile:
            if self.hosting:
                self.hosting_status = Label(text = "Status: Currently Hosting Profile", size_hint = (0.2, 0.1), pos_hint = {"center_x": 0.5, "center_y": 0.5}, font_size=self.font_size, color=self.red)
                stop_hosting_button = Button(text = "Stop Hosting", size_hint = (0.3, 0.15), pos_hint = {"center_x": 0.33, "center_y": 0.1}, on_release = self.stop_hosting, background_color=self.green)
                self.add_widget(stop_hosting_button)
            else:
                self.hosting_status = Label(text = "Status: Not Hosting Profile", size_hint = (0.2, 0.1), pos_hint = {"center_x": 0.5, "center_y": 0.5}, font_size=self.font_size, color=self.red)
                start_hosting_button = Button(text = "Start Hosting", size_hint = (0.3, 0.15), pos_hint = {"center_x": 0.33, "center_y": 0.1}, on_release = self.start_hosting, background_color=self.green)
                self.add_widget(start_hosting_button)
            self.add_widget(self.hosting_status)
        else:
            status = Label(text = "Please create a profile before coming here", size_hint = (0.2, 0.1), pos_hint = {"center_x": 0.5, "center_y": 0.4}, font_size=self.title_font_size, color=self.red)
            self.add_widget(status)

        back_button = Button(text="Back", size_hint=(0.3, 0.15), pos_hint={"center_x": 0.67, "center_y": 0.1}, on_release=self.back_to_menu, background_color=self.darkgreen)
        self.add_widget(back_button)


    def start_hosting(self, instance):
        self.host = Host(self.profile)
        self.thread = start_new_thread(self.host.start_hosting, ())
        self.hosting = True
        self.add_host_widgets()

    def stop_hosting(self, instance):
        self.host.hosting = False
        self.hosting = False

        print("Terminated Hosting session")
        self.add_host_widgets()

    def scan_profiles_menu(self, instance):
        self.clear_widgets()
        self.add_scan_profiles_widgets()

    def add_scan_profiles_widgets(self):
        self.clear_widgets()
        self.add_widget(Label(text="Scan for Profiles", pos_hint={"center_x": 0.5, "center_y": 0.85}, font_size=self.title_font_size, bold=True, color=self.red))
        scan_button = Button(text = "Scan", size_hint = (0.3, 0.15), pos_hint = {"center_x": 0.33, "center_y": 0.65}, on_release = self.start_scan_profile, background_color=self.green)
        self.add_widget(scan_button)

        back_button = Button(text = "Back", size_hint = (0.3, 0.15), pos_hint = {"center_x": 0.67, "center_y": 0.65}, on_release = self.back_to_menu, background_color=self.darkgreen)
        self.add_widget(back_button)
        try:
            profiles_found = ""
            with open("scan_list.txt", "r") as f:
                content = f.read().split("; ")
                profiles_found += content[0] + '\n' + content[1] + '\n' + content[2] + '\n'
                if content:
                    profile_label = Label(text = profiles_found, pos_hint={"center_x": 0.5, "center_y": 0.4}, font_size=self.font_size, color=self.red)
                    self.add_widget(profile_label)
        except:
            pass


    def start_scan_profile(self, instance):
        self.clear_widgets()
        self.add_widget(Label(text="Scan for Profiles", pos_hint={"center_x": 0.5, "center_y": 0.9}, font_size=self.title_font_size, bold=True, color=self.red))
        back_button = Button(text = "Back", size_hint = (0.3, 0.15), pos_hint = {"center_x": 0.5, "center_y": 0.7}, on_release = self.back_to_menu, background_color=self.green)
        self.add_widget(back_button)
        self.c.profiles_found = []
        start_new_thread(self.c.find, ())
        start_new_thread(self.update_profile_list, ())


    def update_profile_list(self):
        temp_label = Label(text="Scanning for profiles around you...", pos_hint={"center_x": 0.5, "center_y": 0.45}, font_size=self.font_size, color=self.red)
        self.add_widget(temp_label)
        while not self.c.done:
            pass
        profile_string = ""
        self.remove_widget(temp_label)
        with open("scan_list.txt", "w") as f:
            f.truncate(0)
            for p in self.c.profiles_found:
                f.write(str(p) + '\n')
                sections = str(p).split("; ")
                profile_string += sections[0] + '\n' + sections[1] + '\n' + sections[2] + '\n'
            f.close
        self.add_widget(Label(text=str(len(self.c.profiles_found)) + " profile(s) found", pos_hint={"center_x": 0.5, "center_y": 0.5}, font_size=self.font_size, color=self.red))
        profile_scan_label = Label(text = profile_string, pos_hint={"center_x": 0.5, "center_y": 0.35}, font_size=self.font_size, color=self.red)
        self.add_widget(profile_scan_label)

    def scan_qr_code_menu(self, instance):
        self.clear_widgets()
        self.add_qr_code_scanner()

    def add_qr_code_scanner(self):
        self.camera = XCamera(on_picture_taken=self.picture_taken)
        self.add_widget(self.camera)

        self.change_cam_button = Button(text="change cam", size_hint=(0.2, 0.1), pos_hint={"center_x": 0.66, "center_y": 0.1}, on_release=self.change_cam, background_color=self.darkgreen)
        self.add_widget(self.change_cam_button)

        self.back_button = Button(text= "Back", size_hint=(0.2, 0.1), pos_hint={"center_x": 0.33, "center_y": 0.1}, on_release=self.back_to_menu, background_color=self.green)
        self.add_widget(self.back_button)

    def picture_taken(self, instance, image_name):
        self.image_name = image_name
        scanner = QrCodeScanner(image_name)
        self.clear_widgets()
        self.add_widget(Label(text="Scan Results", pos_hint={"center_x": 0.5, "center_y": 0.85}, font_size=self.title_font_size, color=self.red))
        self.add_widget(Label(text=str(scanner.data), pos_hint={"center_x": 0.5, "center_y": 0.65}, font_size=self.font_size, color=self.red))
        self.add_widget(Button(text="Back", pos_hint={"center_x": 0.5, "center_y": 0.2}, size_hint=(0.3, 0.15), background_color=self.green, on_release=self.back_to_menu))

    def change_cam(self, instance):
        print("done")
        if self.camera.index == 0:
            self.camera.index = int(self.camera.index) + 1
        elif self.camera.index == 1:
            self.camera.index = int(self.camera.index) - 1
        else:
            self.camera.index = self.camera.index

class runMenu(App):
    def build(self):
        Window.clearcolor = kivy.utils.get_color_from_hex('#EDE5A6')
        return Menu()

runMenu().run()




