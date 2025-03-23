from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
DATABASE = "plates.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Gets the rows as dictionaries
    return conn


def insert_plate(plate):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO plates (plate) VALUES (?)", (plate,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # It already exists
    finally:
        conn.close()


def is_valid(s):
    if not (2 <= len(s) <= 6): # cant be too big
        return False
    if not s[:2].isalpha(): # It needs to begin with a letter
        return False
    if not s.isalnum(): # No special characters
        return False
    
    found_number = False
    for i, char in enumerate(s):
        if char.isdigit():
            if char == '0' and i == 2: # First number cannot be 0
                return False
            found_number = True
        elif found_number: # If the letter after a number is bad
            return False
    
    return True


def get_all_plates():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT plate FROM plates ORDER BY id DESC") # Gets the newest one first
    plates = [row["plate"] for row in cursor.fetchall()]
    conn.close()
    return plates


@app.route('/', methods=["GET", "POST"])
def home():
    message = None
    if request.method == "POST":
        plate = request.form["plate"].upper()

        if not is_valid(plate):
            message = "❌ Invalid plate"
        elif insert_plate(plate):
            message = f"✅ Plate '{plate}' added perfectly"
        else:
            message = "⚠️ This plate already exists"

    plates = get_all_plates()
    return render_template('index.html', message=message, plates=plates)


if __name__ == '__main__':
    #create_db()
    app.run(debug=True)