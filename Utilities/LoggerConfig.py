from inspect import currentframe
from datetime import datetime
import logging
import sys

class EnhancedPrint:
    def __init__(self, file_name=__file__):
        self.file_name = file_name

    def error(self, msg):
        print(f"ERROR: {self._format_msg(msg)}")

    def info(self, msg):
        print(f"INFO: {self._format_msg(msg)}")

    def debug(self, msg):
        print(f"DEBUG: {self._format_msg(msg)}")

    def _format_msg(self, msg):
        formatted_message = f" FILE:{self.file_name}: TIME: {datetime.utcnow()} LINE:{currentframe().f_back.f_back.f_lineno} {msg}"
        return formatted_message


def setup_python_logging(log_name: str):
    """
    Does all the setup for python logging so that it does not have to be done in each file
    :return:
    """
    # Create a logger and set the logging level
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)

    # Create a formatter for the output. The formatter is not added to the logger directly, but the "handler" that the logger will use
    o_formatter = logging.Formatter('%(asctime)s :%(filename)s :%(lineno)d :%(levelname)s:-----%(message)s')

    # handler - stream
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(o_formatter)
    logger.addHandler(stream_handler)

    # Handler - File
    # file_handler = logging.FileHandler("TestFile_ThreadingDemo.log")
    # file_handler.setFormatter(o_formatter)
    # logger.addHandler(file_handler)

    return logger