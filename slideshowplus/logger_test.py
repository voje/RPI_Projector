import logging

logging.basicConfig(
    filename="log/logtest.log",
    filemode="a", level=logging.INFO
)
# logging levels: NONE, DEBUG, INFO, WARNING, ERROR, CRITICAL

log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)

i = 0
while True:
    log.warning(i)  # will print a message to the console
    log.info(i)  # will not print anything
    log.debug(i)
    i += 1
