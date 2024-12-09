# logger.py

import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Logger:
    def __init__(self, app_name):
        # Ensure the logs directory exists
        log_dir = os.getenv('LOG_DIR')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        # Set up log file for capturing only Werkzeug logs
        self.werkzeug_log_file = os.path.join(log_dir, 'werkzeug.log')
        self.werkzeug_handler = RotatingFileHandler(self.werkzeug_log_file, maxBytes=10*1024, backupCount=5)
        self.werkzeug_handler.setLevel(logging.DEBUG)

        # Set up log file for capturing only Flask app logs
        self.app_log_file = os.path.join(log_dir, 'app.log')
        self.app_handler = RotatingFileHandler(self.app_log_file, maxBytes=10*1024, backupCount=5)
        self.app_handler.setLevel(logging.DEBUG)
        app_formatter = logging.Formatter(log_format)
        self.app_handler.setFormatter(app_formatter)

        
        # Create and configure logger for the Flask app
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(logging.DEBUG)

        # Add the handler to the 'werkzeug' logger
        logging.getLogger('werkzeug').addHandler(self.werkzeug_handler)

        # Add the handler to Flask's app logger
        self.logger.addHandler(self.app_handler)

    def get_logger(self):
        return self.logger
