from slideshowplus.projector import projector
import socket
import logging
import threading

log = logging.getLogger(__file__)


class Pjlink(projector.Projector):
    def __init__(self, name=None, ip=None, port=None):
        super().__init__(name=name)
        self.name = name or "pjlink"
        self.ip = ip or "192.168.1.143"
        self.port = port or 4352
        self.commands = {
            "on": b'%1POWR 1\r',
            "off": b'%1POWR 0\r',
            "query": b'%1POWR ?\r'
        }
        self.buffer_size = 1024

    def on(self):
        self.state = "on"
        log.info("on")
        self.thread_send_command("on")

    def off(self):
        self.state = "off"
        log.info("off")
        self.thread_send_command("off")

    def sleep(self):
        return

    def send_command(self, command):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(0)
            s.settimeout(2)
            s.connect((self.ip, self.port))
            s.send(self.commands[command])
            response = s.recv(self.buffer_size)
            s.close()
            log.info(response)
        except Exception as e:
            log.warning(e)

    def thread_send_command(self, command):
        thread = threading.Thread(
            target=self.send_command,
            args=(command,)
        )
        thread.start()


if __name__ == "__main__":
    pj = Pjlink(
        name="pjlink",
        ip="localhost",
        port=4352
    )
    pj.on()
    pj.off()
    pj.sleep()  # Not implemented.
