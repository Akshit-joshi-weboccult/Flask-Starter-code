# Flask Starter Code 
=============================================

This directory contains a Flask starter code for a local environment. The code is organized into several files, each with a specific purpose.

## Default Application (app.py)
---------------------------

The `app.py` file is the default application file, which is similar to `app_all_log_categorywise.py`. It sets up a basic Flask application with logging capabilities. (Recommended)

## Logging Configuration
----------------------

The following files demonstrate different logging configurations for a Flask application:

* `app_all_log_single_file.py`: Logs all application logs to a single file (`app.log`).
* `app_all_log_categorywise.py`: Logs application logs to separate files based on categories (e.g., `app.log` and `werkzeug.log`).
* `app_werkzeug_logs_only.py`: Logs only Werkzeug logs to a file (`werkzeug.log`). 
* you can start with any one file 

## Logging Routes
-----------------

The `app_all_log_categorywise.py` file includes routes for displaying logs:

* `/logs`: Displays all application logs.
* `/logs/werkzeug`: Displays only Werkzeug logs.
* `/logs/<int:line_count>`: Displays a specified number of log lines from last.
* `/logs/werkzeug/<int:line_count>`: Displays a specified number of werkzeug log lines from last.


## API Endpoints for testing purpose
----------------

The `app_all_log_categorywise.py` file includes API endpoints for testing logging:

* `/target-api`: A target API for testing logging.
* `/caller-api`: A caller API that makes requests to the target API.

## Running the Application
-------------------------

To run the application, execute the following command: (change file name as per requirements)
```bash
python app.py
```

## Note
* creating new fresh environment is recommended, environment must have flask