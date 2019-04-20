import logging

FORMAT = '\n[%(levelname)s]:%(name)s: %(message)s\n'
logging.basicConfig(format=FORMAT)


def build_logger(name, level=logging.DEBUG):
    new_logger = logging.getLogger(name)
    new_logger.setLevel(level)
    return new_logger
