# Flask Starter Code

This is a Flask application that captures logs from both Werkzeug and the Flask app. It has a simple home page that displays a welcome message.

It is just a starter code for flask app which comes with already managed logger class and log APIs, It is recommended to go through code once before starting actual code.

## Log Files

The application captures logs from both Werkzeug and the Flask app. The logs are stored in separate files:

- `werkzeug.log`: Captures logs from Werkzeug (Flask)
- `app.log`: Captures logs from the Flask app

## Home Page

The home page is a simple HTML template that displays a welcome message. It can be accessed at the root URL (`/`).


## Running the Application

To run the application, follow these steps:

1. Make sure you have Python and Flask installed.
2. Clone the repository or download the code.
3. Create a virtual environment and activate it.
4. Install the required dependencies by running `pip install -r requirements.txt`.
5. Set up the environment variables by creating a `.env` file in the root directory and adding the following line: `LOG_DIR=logs`
6. Run the application by executing `python app.py`.
7. URL for this app will be (http://localhost:5000/) you can change accordingly.

## Additional Information

- The application uses the `logger.py` module to set up the log files and handlers.
- The log files are stored in the `logs` directory.
- Logs won't be visible in the console; they are available in the logs folder, or you can check them through http://localhost:5000/logs/. There are other APIs available to check the logs, such as http://localhost:5000/logs/werkzeug/. You can append an integer to the URL to view only the last that many logs. For more check code. 
- The home page template is located in the `templates` directory.
- The CSS styles for the home page are located in the [static/css] directory.
