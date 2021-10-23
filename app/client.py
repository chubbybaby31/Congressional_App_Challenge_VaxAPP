import nmap
import socket
import time
from _thread import start_new_thread, exit_thread
import netifaces


class Client():

    def __init__(self):
        self.nm = nmap.PortScanner()
        self.gateway = self.find_gateway() + '/24'
        self.targets = self.nm.listscan(hosts='{}'.format(self.gateway))
        self.PORT = 65432
        self.profiles_found = []
        self.done = False

    def find_gateway(self):
        Interfaces = netifaces.interfaces()
        for inter in Interfaces:
            gws = netifaces.gateways()
            temp_list = list(gws['default'][netifaces.AF_INET])
            count = 0
            for item in temp_list:
                count += 1
                if count >= 1:
                    return item

    def find(self):
        self.done = False
        for target in self.targets:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    start_new_thread(self.connect, (s, target))
                    time.sleep(0.1)
            except:
                pass
        self.done = True
        print("done")

    def connect(self, s, target):
        try:
            s.connect((target, self.PORT))
            data = s.recv(1024).decode()
            print('Received', repr(data))
            self.profiles_found.append(data)
            exit_thread()
        except:
            exit_thread()