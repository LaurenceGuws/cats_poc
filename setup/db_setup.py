import os
import sqlite3
import click
from flask import current_app


def init_db():
    instance_path = current_app.config['INSTANCE_FOLDER']

    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    db_path = os.path.join(instance_path, 'cats.sqlite')
    if not os.path.exists(db_path):
        execute_sql_from_file(db_path, 'setup/schema.sql')


def execute_sql_from_file(db_path, sql_file):
    absolute_path = os.path.abspath(sql_file)
    print(f"Absolute path to SQL file: {absolute_path}")

    if os.path.exists(absolute_path):
        print("SQL file exists.")
        conn = sqlite3.connect(db_path)
        with current_app.open_resource(absolute_path, mode='r') as f:
            conn.cursor().executescript(f.read())
        conn.commit()
        conn.close()
        click.echo('Database updated successfully.')
    else:
        print("SQL file does not exist.")


def execute_query(db_path, query, params=()):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        conn.rollback()
    finally:
        conn.close()


def get_all_cats():
    db_path = os.path.join(current_app.config['INSTANCE_FOLDER'], 'cats.sqlite')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cats")
    cats = cursor.fetchall()
    conn.close()
    return cats


def add_cat(cat_data):
    db_path = os.path.join(current_app.config['INSTANCE_FOLDER'], 'cats.sqlite')
    query = """
    INSERT INTO Cats (Name, Pic, Sex, Colour, Condition, Weight, Age, FirstVax, SecondVax, SteriDue, AdoptedDate, AdoptedBy, AdopterContact, Message, ReceivedDate)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    execute_query(db_path, query, tuple(cat_data.values()))


def update_cat_by_name(cat_name, updated_data):
    try:
        conn = sqlite3.connect('instance/cats.sqlite')
        cursor = conn.cursor()
        
        update_statements = []
        values = []
        
        for key, value in updated_data.items():
            db_key = key
            update_statements.append(f"{db_key} = ?")
            values.append(value)
        
        update_str = ", ".join(update_statements)
        values.append(cat_name)
        
        sql_query = f"UPDATE Cats SET {update_str} WHERE Name = ?"
        print(f"SQL Query: {sql_query}")  # Debugging
        print(f"Values: {values}")  # Debugging
        
        cursor.execute(sql_query, values)
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
        
    return True



def mock_data():
    # Connect to the database
    instance_path = current_app.config['INSTANCE_FOLDER']
    db_path = os.path.join(instance_path, 'cats.sqlite')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Insert mock data for Cats table
    c.executemany(
        '''INSERT INTO Cats (Name, Pic, Sex, Colour, Condition, Weight, Age, FirstVax, SecondVax, SteriDue, AdoptedDate, AdoptedBy, AdopterContact, Message, ReceivedDate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        [
            ('cat1', 'pic1.jpg', 'Male', 'Black', 'Healthy', 4.2, 2, '2022-01-01', '2022-02-01', '2023-01-01', '2022-03-01', 'John Doe', 'john@example.com', 'Happy Cat', '2022-01-01'),
            ('cat2', 'pic2.jpg', 'Female', 'White', 'Healthy', 3.5, 1, '2022-02-01', '2022-03-01', '2023-02-01', '2022-04-01', 'Jane Doe', 'jane@example.com', 'Cute Cat', '2022-02-01'),
            ('cat3', 'pic3.jpg', 'Male', 'Brown', 'Sick', 2.8, 3, '2022-05-01', '2022-06-01', '2023-05-01', '2022-07-01', 'Sam Smith', 'sam@example.com', 'Get well soon', '2022-05-01')
        ]
    )

    # Insert mock data for Moms table
    c.executemany(
        '''INSERT INTO Moms (Username, Password, Location)
        VALUES (?, ?, ?)''',
        [
            ('mom1', 'password1', 'Location1'),
            ('mom2', 'password2', 'Location2'),
            ('mom3', 'password3', 'Location3')
        ]
    )

    # Insert mock data for Deaths table
    c.executemany(
        '''INSERT INTO Deaths (CatID, CauseOfDeath, VetName, Date, Location)
        VALUES (?, ?, ?, ?, ?)''',
        [
            (1, 'Old Age', 'Vet1', '2022-04-01', 'Location1'),
            (2, 'Accident', 'Vet2', '2022-05-01', 'Location2'),
            (3, 'Disease', 'Vet3', '2022-06-01', 'Location3')
        ]
    )

    # Insert mock data for VetVisits table
    c.executemany(
        '''INSERT INTO VetVisits (CatID, Diagnosis, MedsPrescribed, Date)
        VALUES (?, ?, ?, ?)''',
        [
            (1, 'Diagnosis1', 'Meds1', '2022-05-01'),
            (2, 'Diagnosis2', 'Meds2', '2022-06-01'),
            (3, 'Diagnosis3', 'Meds3', '2022-07-01')
        ]
    )

    # Insert mock data for VetChecks table
    c.executemany(
        '''INSERT INTO VetChecks (CatID, Deworm, Date)
        VALUES (?, ?, ?)''',
        [
            (1, 'Deworm1', '2022-06-01'),
            (2, 'Deworm2', '2022-07-01'),
            (3, 'Deworm3', '2022-08-01')
        ]
    )

    # Insert mock data for LocationMoves table
    c.executemany(
        '''INSERT INTO LocationMoves (CatID, FromLocation, ToLocation, Date)
        VALUES (?, ?, ?, ?)''',
        [
            (1, 'From1', 'To1', '2022-07-01'),
            (2, 'From2', 'To2', '2022-08-01'),
            (3, 'From3', 'To3', '2022-09-01')
        ]
    )

    # Insert mock data for Docs table
    c.executemany(
        '''INSERT INTO Docs (Type, File)
        VALUES (?, ?)''',
        [
            ('Type1', b'File1'),
            ('Type2', b'File2'),
            ('Type3', b'File3')
        ]
    )


    # Commit changes and close the connection
    conn.commit()
    conn.close()

    return "Mock data has been added."
