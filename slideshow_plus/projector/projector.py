import logging

log = logging.getLogger(__name__)


class Projector:
    def __init__(self, name=None):
        self.name = name or "skeleton for a projector class"
        self.state = "off"   # For debugging. TODO change to undefined

    def on(self):
        self.state = "on"
        log.info("on")

    def off(self):
        self.state = "off"
        log.info("off")

    def sleep(self):
        self.state = "sleep"
        log.info("sleep")
