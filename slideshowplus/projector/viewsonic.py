# from slideshowplus.projector import projector
import projector
import socket
import logging
import threading
import time

log = logging.getLogger(__file__)


class ViewSonic(projector.Projector):
    def __init__(self, name=None, ip=None, port=None):
        super().__init__(name=name)
        self.name = name or "ViewSonic"
        # on the projector, you need DHCP off, configure ip address
        self.ip = ip or "192.168.1.143"
        # control ports: TCP 23, TCP 9715 ...
        # some other specs say port 4661
        # !! self.port is overwritten in send_command and send_command1
        self.port = port or 23
        self.buffer_size = 1024

    # For the LAN control, the code format is similar except that
    # to replace the “0x” to “\”, via a LAN Port 4661.
    def on(self):
        self.state = "on"
        log.info("power on")
        # NOT SURE ABOUT COMMANDS
        # CHECK https://www.manualslib.com/manual/897314/Viewsonic-Pj1158-1.html?page=65#manual
        on_command1 = b'\x06\x14\x00\x04\x00\x34\x11\x00\x00\x5D'
        # on_command1 = b'\06\14\00\04\00\34\11\00\00\5D'
        self.thread_send_command(on_command1)

    def off(self):
        self.state = "off"
        log.info("power off")
        off_command1 = b'\x06\x14\x00\x04\x00\x34\x11\x01\x00\x5E'
        self.thread_send_command(off_command1)

    def sleep(self):
        return

    # not sure how the projector protocol works,
    # trying 2 different send commands
    def send_command(self, cmd_string):
        try:
            try_port = 23
            log.info("Trying port {}.".format(try_port))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(0)
            s.settimeout(2)
            s.connect((self.ip, try_port))
            s.send(cmd_string)
            response = s.recv(self.buffer_size)
            s.close()
            log.info(response)
        except Exception as e:
            log.warning(e)

    def send_command1(self, cmd_string):
        try:
            try_port = 6641
            log.info("Trying port {}.".format(try_port))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(0)
            s.settimeout(2)
            s.connect((self.ip, try_port))
            s.send(cmd_string)
            response = s.recv(self.buffer_size)
            s.close()
            log.info(response)
        except Exception as e:
            log.warning(e)

    def thread_send_command(self, cmd_string):
        thread = threading.Thread(
            target=self.send_command,
            args=(cmd_string,)
        )
        thread.start()

        time.sleep(2)

        thread1 = threading.Thread(
            target=self.send_command1,
            args=(cmd_string,)
        )
        thread1.start()


if __name__ == "__main__":
    print("Testing ViewSonic.")
    vs = ViewSonic(
        name="Test_ViewSonic",
        ip="localhost",
    )
    vs .on()
    # eps.off()
    # eps.sleep()  # Not implemented.
