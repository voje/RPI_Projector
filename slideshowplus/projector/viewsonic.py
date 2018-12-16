# -*- coding: utf-8 -*-
from slideshowplus.projector import projector
import socket
import logging
import threading
import time
import itertools

# for debugging
# import sys
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

log = logging.getLogger(__file__)

class ViewSonic(projector.Projector):
    def __init__(self, name=None, ip=None, port=None):
        super().__init__()
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

        # pj11581.pdf
        try_commands = [
            bytes.fromhex("BEEF030600BAD20100006001000D"), # with carriage return (0D)
            bytes.fromhex("BEEF030600BAD2010000600100"),
        ]
        try_ports = [23, 4661, 9715]
        self.thread_send_multiple(try_commands, try_ports)
        # self.thread_send_command(on_command1)

    def off(self):
        self.state = "off"
        log.info("power off")

        # pj11581.pdf
        try_commands = [
            bytes.fromhex("BEEF0306002AD30100006000000D"), # with carriage return (0D)
            bytes.fromhex("BEEF0306002AD3010000600000"),
        ]
        try_ports = [23, 4661, 9715]
        self.thread_send_multiple(try_commands, try_ports)
        # self.thread_send_command(off_command1)

    def sleep(self):
        return

    # not sure how the projector protocol works,
    # trying 2 different send commands

    def send_command(self, cmd, port):
        try:
            log.info(
                "\n\nSending control command:\n"
                "[*] ip: {}\n"
                "[*] port: {}\n"
                "[*] cmd: {}".format(
                    self.ip, port, cmd)
            )
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(0)
            s.settimeout(2)
            s.connect((self.ip, port))
            s.send(cmd)
            response = s.recv(self.buffer_size)
            s.close()
            log.info(response)
        except Exception as e:
            log.warning(e)

    def thread_send_command(self, cmd, port):
        thread = threading.Thread(
            target=self.send_command,
            args=(cmd, port,)
        )
        thread.start()

    def thread_send_multiple(self, commands, ports):
        for cmd, port in itertools.product(commands, ports):
            # print(cmd, port)
            self.thread_send_command(cmd, port)
            time.sleep(3)


if __name__ == "__main__":
    print("Testing ViewSonic.")
    vs = ViewSonic(
        name="Test_ViewSonic",
        ip="192.168.2.22",
    )
    vs .on()
    # eps.off()
    # eps.sleep()  # Not implemented.
