import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify

app = Flask(__name__)

# Set up the log file for capturing only Werkzeug logs
log_file = 'werkzeug.log'
handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
handler.setLevel(logging.DEBUG)

# Add the handler to the 'werkzeug' logger, not the Flask app logger
logging.getLogger('werkzeug').addHandler(handler)

@app.route('/')
def index():
    # This log won't be captured by the werkzeug logger
    app.logger.info("This is an app log.")
    return "Welcome to the Home Page!"

@app.route('/logs', defaults={'line_count': None})
@app.route('/logs/<int:line_count>')
def show_logs(line_count):
    try:
        with open(log_file, 'r') as log_file_handle:
            logs = log_file_handle.readlines()
            if line_count is not None:
                logs = logs[-line_count:]
            logs_str = ''.join(logs)
        return f"<pre>{logs_str}</pre>"
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)