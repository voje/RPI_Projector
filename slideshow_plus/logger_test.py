import logging

logging.basicConfig(filename="logtest.log", filemode="a", level=logging.INFO)
# logging levels: NONE, DEBUG, INFO, WARNING, ERROR, CRITICAL

log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)

log.warning("Warning level.")  # will print a message to the console
log.info("Info level.")  # will not print anything
log.debug("Debug level.")
