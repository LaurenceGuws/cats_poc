import logging
from flask import Flask, jsonify, render_template, request
from flask.cli import with_appcontext
from setup.db_setup import init_db, get_all_cats, mock_data, update_cat_by_name
from collections import OrderedDict
from datetime import datetime
import sqlite3

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize the Flask application
app = Flask(__name__)
app.config['INSTANCE_FOLDER'] = 'instance'

@app.cli.command('setup')
@with_appcontext
def setup():
    """Set up the application."""
    logging.debug("Setting up the application...")
    init_db()

@app.route('/')
def hello_world():
    current_year = datetime.now().year
    logging.debug(f"Rendering index.html with current_year={current_year}")
    return render_template('index.html', current_year=current_year)

@app.route('/cats')
def cats_page():
    logging.debug("Fetching all cats from the database...")
    cats, field_names = get_all_cats()
    cats_dict_list = [OrderedDict(zip(field_names, cat)) for cat in cats]
    return render_template('cats/cats.html', cats=cats_dict_list)

@app.route('/update_cat', methods=['POST'])
def update_cat_route():
    logging.debug("Received POST request to update a cat.")
    cat_data = request.json
    logging.debug(f"Received data: {cat_data}")  # Debugging line
    cat_name = cat_data.get('cat_name')
    updated_data = {k: v for k, v in cat_data.items() if k != 'cat_name'}
    print(f"cat_name: {cat_name}")
    print(f"updated_data: {updated_data}")
    result = update_cat_by_name(cat_name, updated_data)  # Using the imported function
    return (jsonify({"message": "Cat updated successfully"}), 200) if result else (jsonify({"message": "Failed to update cat"}), 400)

# Additional routes for other functionalities
# These could be generalized further
@app.route('/moms')
def moms_page():
    return render_template('moms/moms.html')

@app.route('/deaths')
def deaths_page():
    return render_template('deaths/deaths.html')

@app.route('/vet_visits')
def vet_visits_page():
    return render_template('vet_visits/vet_visits.html')

@app.route('/vet_checks')
def vet_checks_page():
    return render_template('vet_checks/vet_checks.html')

@app.route('/location_moves')
def location_moves_page():
    return render_template('location_moves/location_moves.html')

@app.route('/docs')
def docs_page():
    return "This is the Docs page."

@app.route('/mock')
def mock_data_route():
    mock_data()  # Populate the database with mock data
    return "Mock data has been added."


if __name__ == '__main__':
    app.run(debug=True)
