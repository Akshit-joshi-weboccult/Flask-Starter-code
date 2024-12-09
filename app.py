from flask import Flask, jsonify, request, render_template
import requests
from logger import Logger
import os
from dotenv import load_dotenv
import traceback

# Load environment variables from .env file
load_dotenv()

# Get log directory from environment variable
log_dir = os.getenv('LOG_DIR')

# Initialize Flask app
app = Flask(__name__)

# Set up logger using the Logger class from logger.py
logger = Logger(app.name).get_logger()

# ping API
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'success', 'message': 'Active'}), 200


# index API
@app.route('/')
def index():
    # This log will be captured in the Flask app log file
    app.logger.info("This is an app log.")
    app.logger.warning("This is a warning message.(for testing)")
    return render_template('index.html')


# to see logs of werkzeug (Flask)
@app.route('/logs/werkzeug/', defaults={'line_count': None})
@app.route('/logs/werkzeug/<int:line_count>')
def show_werkzeug_logs(line_count):
    
    # log_files =  [f for f in sorted(os.listdir(log_dir), reverse=True) if f.startswith('werkzeug.log.')] + ['werkzeug.log']

    try:
        log_files =  [f for f in sorted(os.listdir(log_dir), reverse=True) if f.startswith('werkzeug.log.')] + ['werkzeug.log']
        logs = []
        # Read all log files in order (current log + rotated backups)
        for log_file in log_files:
            with open(os.path.join(log_dir, log_file), 'r') as log_file_handle:
                logs.extend(log_file_handle.readlines())

        if line_count is not None:
            logs = logs[-line_count:]
        logs_str = ''.join(logs)
        return f"<pre>{logs_str}</pre>"
    except Exception as e:
        app.logger.error(f"An error occurred: \n{traceback.format_exc()}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


# to see logs of app
@app.route('/logs/', defaults={'line_count': None})
@app.route('/logs/<int:line_count>')
def show_app_logs(line_count):
    log_files =  [f for f in sorted(os.listdir(log_dir), reverse=True) if f.startswith('app.log.')] + ['app.log']
    try:
        logs = []
        # Read all log files in order (current log + rotated backups)
        for log_file in log_files:
            with open(os.path.join(log_dir, log_file), 'r') as log_file_handle:
                logs.extend(log_file_handle.readlines())
        if line_count is not None:
            logs = logs[-line_count:]
        logs_str = ''.join(logs)
        return f"<pre>{logs_str}</pre>"
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 50


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
