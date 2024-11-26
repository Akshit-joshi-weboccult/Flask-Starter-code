import logging
import sys
from logging.handlers import RotatingFileHandler
from flask import Flask

app = Flask(__name__)

# Create a log file and use RotatingFileHandler to avoid large log files
log_file = 'app.log'
handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
handler.setLevel(logging.DEBUG)

# Add the handler to Flask's logger
app.logger.addHandler(handler)

# Also add handler to Werkzeug's logger
logging.getLogger('werkzeug').addHandler(handler)

# Redirect print statements (stdout) to logging
class PrintToLog:
    def write(self, message):
        if message != '\n':  # Skip empty lines
            app.logger.info(message)

    def flush(self):
        pass  # No need for flush

# Redirect stdout to capture print statements
sys.stdout = PrintToLog()

@app.route('/')
def index():    
    app.logger.info("Home page accessed")
    app.logger.warning("This is a warning message")
    app.logger.error("This is an error message")
    app.logger.critical("This is a critical message")
    app.logger.debug("This is a debug message")
    return "Welcome to the Home Page!"

@app.route('/logs')
def show_logs():
    with open(log_file, 'r') as log_file_handle:
        logs = log_file_handle.read()
    return f"<pre>{logs}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
