from flask import Flask, jsonify, render_template, request
from flask.cli import with_appcontext
from setup.db_setup import init_db, get_all_cats, mock_data  # Import the function
from collections import OrderedDict
from datetime import datetime
import sqlite3


app = Flask(__name__)
app.config['INSTANCE_FOLDER'] = 'instance'

@app.cli.command('setup')
@with_appcontext
def setup():
    """Set up the application."""
    init_db()  # Call the function

@app.route('/')
def hello_world():
    current_year = datetime.now().year  # Get the current year
    return render_template('index.html', current_year=current_year)


@app.route('/cats')
def cats_page():
    cats = get_all_cats()  # Assume this returns a list of tuples
    # Convert to a list of dictionaries for better compatibility with the template
    cats_dict_list = []
    field_names = ['CatID', 'Name', 'Sex', 'Colour', 'Condition', 'Weight', 'Age', 
                   'FirstVax', 'SecondVax', 'SteriDue', 'AdoptedDate', 'AdoptedBy', 
                   'AdopterContact', 'Message', 'ReceivedDate']
    for cat in cats:
        cat_dict = OrderedDict(zip(field_names, cat))
        cats_dict_list.append(cat_dict)
    return render_template('cats/cats.html', cats=cats_dict_list)


@app.route('/update_cat', methods=['POST'])
def update_cat_route():
    cat_data = request.json
    cat_name = cat_data.get('cat_name')
    updated_data = {k: v for k, v in cat_data.items() if k != 'cat_name'}
    result = update_cat_by_name(cat_name, updated_data)  # You'll have to implement update_cat_by_name()
    if result:
        return jsonify({"message": "Cat updated successfully"})
    else:
        return jsonify({"message": "Failed to update cat"}), 400

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
    mock_data()  # Call the mock_data function here
    return "Mock data has been added."

############################################################
def update_cat_by_name(cat_name, updated_data):
    try:
        conn = sqlite3.connect('instance/cats.sqlite')
        cursor = conn.cursor()
        
        update_statements = []
        values = []
        
        for key, value in updated_data.items():
            db_key = key  # Adjust this line to map JavaScript keys to DB keys, if needed
            update_statements.append(f"{db_key} = ?")
            values.append(value)
        
        update_str = ", ".join(update_statements)
        values.append(cat_name)
        
        sql_query = f"UPDATE Cats SET {update_str} WHERE Name = ?"
        cursor.execute(sql_query, values)
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
        
    return True


if __name__ == '__main__':
    app.run(debug=True)
