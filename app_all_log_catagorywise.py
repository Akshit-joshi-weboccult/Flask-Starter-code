import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
import requests
app = Flask(__name__)

# Set up log file for capturing only Werkzeug logs
werkzeug_log_file = 'werkzeug.log'
werkzeug_handler = RotatingFileHandler(werkzeug_log_file, maxBytes=10*1024*1024, backupCount=5)
werkzeug_handler.setLevel(logging.DEBUG)

# Set up log file for capturing only Flask app logs
app_log_file = 'app.log'
app_handler = RotatingFileHandler(app_log_file, maxBytes=10*1024*1024, backupCount=5)
app_handler.setLevel(logging.DEBUG)

# Add the handler to the 'werkzeug' logger, not the Flask app logger
logging.getLogger('werkzeug').addHandler(werkzeug_handler)

# Add the handler to Flask's app logger
app.logger.addHandler(app_handler)
app.logger.setLevel(logging.DEBUG)



# Home API
@app.route('/')
def index():
    # This log will be captured in the Flask app log file
    app.logger.info("This is an app log.")
    app.logger.warning("This is a warning message.")
    return "Welcome to the Home Page!"



# to see logs of werkzeug (Flask) and app logs
@app.route('/logs/werkzeug', defaults={'line_count': None})
@app.route('/logs/werkzeug/<int:line_count>')
def show_werkzeug_logs(line_count):
    try:
        with open(werkzeug_log_file, 'r') as log_file_handle:
            logs = log_file_handle.readlines()
            if line_count is not None:
                logs = logs[-line_count:]
            logs_str = ''.join(logs)
        return f"<pre>{logs_str}</pre>"
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/logs/', defaults={'line_count': None})
@app.route('/logs/<int:line_count>')
def show_app_logs(line_count):
    try:
        with open(app_log_file, 'r') as log_file_handle:
            logs = log_file_handle.readlines()
            if line_count is not None:
                logs = logs[-line_count:]
            logs_str = ''.join(logs)
        return f"<pre>{logs_str}</pre>"
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    




#this is for test api to check working of logs API
@app.route('/target-api', methods=['GET'])
def target_api():
    app.logger.info("Target API accessed")
    data = {'message': 'Hello from target API!'}
    return jsonify(data)


# This is the second API (caller API)
@app.route('/caller-api', methods=['GET'])
def caller_api():
    # URL of the target API
    target_url = 'http://localhost:5000/target-api'
    
    try:
        # Make a GET request to the target API
        for _ in range(1000):
            response = requests.get(target_url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the data from the target API
            return jsonify({'status': 'success', 'data_from_target': response.json()})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to call target API'}), 500
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    


if __name__ == '__main__':
    app.run(debug=True)
