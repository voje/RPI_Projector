import logging

logging.basicConfig(filename="./testlog.log")

log = logging.Logger("my_logger")

log.debug("asdf")
log.info("test")
