import logging
from .colors import *


# class Formatter(logging.Formatter):
#
#     def __init__(self, mode):
#
#         if mode == "dev":
#             self.FORMATS = {
#                 logging.DEBUG: WHITE + "\n\t[%(name)s]  " + BASE_C + "%(message)s" + GREY + "  %(asctime)s",
#                 logging.INFO: GREEN + "\n\t[%(name)s]  " + BASE_C + "%(message)s" + GREY + "  %(asctime)s",
#                 logging.WARNING: ORANGE + "\n\t[%(name)s]  " + BASE_C + "%(message)s" + GREY + "  %(filename)s:%(lineno)d",
#                 logging.ERROR: RED + "\n\t[%(name)s]  " + BASE_C + "%(message)s" + GREY + "  %(filename)s:%(lineno)d",
#                 logging.CRITICAL: PURPLE + "\n\t[%(name)s]  " + BASE_C + "%(message)s" + GREY + "  %(filename)s:%(lineno)d",
#             }
#         elif mode == "prod":
#             self.FORMATS = {
#                 logging.DEBUG: WHITE + "\n\t[%(levelname)s]  " + BASE_C + "%(message)s",
#                 logging.INFO: GREEN + "\n\t[%(levelname)s]  " + BASE_C + "%(message)s",
#                 logging.WARNING: ORANGE + "\n\t[%(levelname)s]  " + BASE_C + "%(message)s",
#                 logging.ERROR: RED + "\n\t[%(levelname)s]  " + BASE_C + "%(message)s",
#                 logging.CRITICAL: PURPLE + "\n\t[%(levelname)s]  " + BASE_C + "%(message)s",
#             }
#
#     def format(self, record):
#         datefmt = '%H:%M:%S'
#         log_fmt = self.FORMATS.get(record.levelno)
#         formatter = logging.Formatter(log_fmt, datefmt)
#         return formatter.format(record)
#
#
# def gen(name="FLAUNCHER", level=logging.DEBUG, mode="prod"):
#     logger = logging.getLogger(name)
#     logger.setLevel(level)
#
#     h = logging.StreamHandler()
#     h.setLevel(logging.DEBUG)
#     h.setFormatter(Formatter(mode))
#
#     logger.addHandler(h)
#
#     return logger


class Formatter(logging.Formatter):

    def __init__(self):

        self.FORMATS = {
            logging.DEBUG: WHITE + "\n\t[%(name)s]  " + BASE_C + "%(message)s" + GREY + "  %(asctime)s" + WHITE,
            logging.INFO: GREEN + "\n\t[%(name)s]  " + BASE_C + "%(message)s" + GREY + "  %(asctime)s" + WHITE,
            logging.WARNING: ORANGE + "\n\t[%(name)s]  " + BASE_C + "%(message)s" + GREY + "  %(filename)s:%(lineno)d" + WHITE,
            logging.ERROR: RED + "\n\t[%(name)s]  " + BASE_C + "%(message)s" + GREY + "  %(filename)s:%(lineno)d" + WHITE,
            logging.CRITICAL: PURPLE + "\n\t[%(name)s]  " + BASE_C + "%(message)s" + GREY + "  %(filename)s:%(lineno)d" + WHITE,
        }

    def format(self, record):
        datefmt = '%H:%M:%S'
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt)
        return formatter.format(record)


def gen(name="FLAUNCHER", level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    h = logging.StreamHandler()
    h.setLevel(logging.DEBUG)
    h.setFormatter(Formatter())

    logger.addHandler(h)

    return logger
