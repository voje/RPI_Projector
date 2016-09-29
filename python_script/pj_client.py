from pjlink import *
import socket
import sys


class PjClient:

    def __init__(self):
        self.ip = "192.168.1.143"
        #self.ip = "127.0.0.1" #for testing
        self.port = 4352
        self.mute = False
        #if the projector is running and muted and we restart raspberry
        try:
            self.init_unmute()
        except:
            pass

    def init_unmute(self):
        sock = socket.socket()
        sock.connect((self.ip, self.port))
        f = sock.makefile()
        proj = projector.Projector(f)
        proj.set_mute(MUTE_VIDEO, '0')
        f.close()
        sock.close()

    def send_command(self, command):
        sock = socket.socket()
        sock.connect((self.ip, self.port))
        f = sock.makefile()

        #--- use pjlink here

        proj = projector.Projector(f)

        if command == "on":
            proj.set_power("on")
        elif command == "off":
            proj.set_power("off")
        elif command == "mute":
            if not self.mute:
                self.mute = True
                proj.set_mute(MUTE_VIDEO, '1')
            else:
                self.mute = False
                proj.set_mute(MUTE_VIDEO, '0')

        #---

        f.close()
        sock.close()

if __name__ == "__main__":
    pjCli = PjClient()
    #pjCli.send_command("on")
    #pjCli.send_command("off")
    pjCli.send_command("mute")
