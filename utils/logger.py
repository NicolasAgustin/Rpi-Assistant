import logging
import sys

class Logger:

    def __init__(self, module_name: str):

        self.a_logger = logging.getLogger()
        self.a_logger.setLevel(logging.DEBUG)

        output_file_handler = logging.FileHandler("logs/app.log")
        stdout_handler = logging.StreamHandler(sys.stdout)

        self.a_logger.addHandler(output_file_handler)
        self.a_logger.addHandler(stdout_handler)

        # logging.basicConfig(filename='logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
        # logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    def info(self, des: str):
        self.a_logger.info(des)

    def error(self, error: str):
        self.a_logger.error(error)
