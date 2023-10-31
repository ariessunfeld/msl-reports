import logging

# Set up a specific logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Clear default handlers
logger.handlers = []

# Formatter for the logs
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# File handler to log messages to a file
file_handler = logging.FileHandler('app_log.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Stream handler to log messages to the console (terminal)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

username = None
password = None
session = None
driver = None
