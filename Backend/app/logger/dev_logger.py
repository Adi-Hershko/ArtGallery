import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:     %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)