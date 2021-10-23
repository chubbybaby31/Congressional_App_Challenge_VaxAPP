import socket
from _thread import start_new_thread, exit_thread

class Host():
    def __init__(self, profile):
        self.profile = profile
        self.profile_str = self.profile.transmit_string()
        self.ip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
        self.port = 65432
        self.hosting = True

    def start_hosting(self):
        print("starting to host profile")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip, self.port))
            start_new_thread(self.listen, (s,))
            while self.hosting:
                if not self.hosting:
                    exit_thread()
                    exit()

    def listen(self, s):
        while self.hosting:
            try:
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    conn.sendall(self.profile_str.encode())
            except ConnectionAbortedError:
                break