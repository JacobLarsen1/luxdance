from flask import Flask, request, render_template_string
import threading
import sqlite3
import os

app = Flask(__name__)

DB_FILE = 'data.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    number INTEGER
                )''')
    conn.commit()
    conn.close()

def load_data():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT name, age, number FROM entries')
    rows = c.fetchall()
    conn.close()
    return [{'name': row[0], 'age': row[1], 'number': row[2]} for row in rows]

def save_entry(name, age, number):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO entries (name, age, number) VALUES (?, ?, ?)', (name, age, number))
    conn.commit()
    conn.close()

init_db()
entries = load_data()
names = {}
counter = 1
for entry in entries:
    if entry['name'] not in names:
        names[entry['name']] = counter
        counter += 1
lock = threading.Lock()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>LuxxOs - Name and Age Assignment</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 0; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: #333; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            min-height: 100vh; 
        }
        .container { 
            background: white; 
            padding: 40px; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2); 
            max-width: 500px; 
            width: 100%; 
            text-align: center; 
        }
        h1 { 
            color: #764ba2; 
            margin-bottom: 30px; 
            font-size: 2.5em; 
            font-weight: bold; 
        }
        .logo { 
            text-align: center; 
            margin-bottom: 20px; 
        }
        .logo img { 
            max-width: 200px; 
            height: auto; 
        }
        form { 
            margin-bottom: 20px; 
        }
        label { 
            display: block; 
            margin-bottom: 10px; 
            font-weight: bold; 
            text-align: left; 
        }
        input[type="text"], input[type="number"] { 
            width: 100%; 
            padding: 15px; 
            margin-bottom: 20px; 
            border: 2px solid #ddd; 
            border-radius: 8px; 
            font-size: 1.1em; 
            box-sizing: border-box; 
        }
        input[type="text"]:focus, input[type="number"]:focus { 
            border-color: #667eea; 
            outline: none; 
        }
        input[type="submit"] { 
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
            color: white; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 1.2em; 
            font-weight: bold; 
            width: 100%; 
            transition: transform 0.2s; 
        }
        input[type="submit"]:hover { 
            transform: scale(1.05); 
        }
        .result { 
            margin-top: 20px; 
            font-size: 1.5em; 
            color: #28a745; 
            font-weight: bold; 
        }
        .view-btn { 
            display: inline-block; 
            margin-top: 20px; 
            padding: 15px 30px; 
            background: linear-gradient(135deg, #007bff 0%, #6610f2 100%); 
            color: white; 
            text-decoration: none; 
            border-radius: 8px; 
            font-size: 1.1em; 
            font-weight: bold; 
            transition: transform 0.2s; 
        }
        .view-btn:hover { 
            transform: scale(1.05); 
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="/static/logo.png" alt="Luxx Dance Logo">
        </div>
        <h1>LuxxOs</h1>
        <form action="/submit" method="post">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
            <label for="age">Age:</label>
            <input type="number" id="age" name="age" required>
            <input type="submit" value="Submit">
        </form>
        {% if number %}
        <div class="result">Your assigned number is: {{ number }}</div>
        {% endif %}
        <a href="/view" class="view-btn">View All Entries</a>
    </div>
</body>
</html>
"""

VIEW_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>LuxxOs - All Entries</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: #333; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
        }
        .container { 
            background: white; 
            padding: 40px; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2); 
            max-width: 800px; 
            width: 100%; 
        }
        h1 { 
            color: #764ba2; 
            text-align: center; 
            font-size: 2.5em; 
            margin-bottom: 30px; 
        }
        .logo { 
            text-align: center; 
            margin-bottom: 20px; 
        }
        .logo img { 
            max-width: 200px; 
            height: auto; 
        }
        .entry { 
            background: #f8f9fa; 
            padding: 20px; 
            margin: 15px 0; 
            border-radius: 10px; 
            box-shadow: 0 5px 15px rgba(0,0,0,0.1); 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
        }
        .entry h3 { 
            margin: 0; 
            color: #007bff; 
            font-size: 1.3em; 
        }
        .entry p { 
            margin: 5px 0; 
            font-size: 1.1em; 
        }
        .back-btn { 
            display: block; 
            margin: 30px auto 0; 
            padding: 15px 30px; 
            background: linear-gradient(135deg, #6c757d 0%, #495057 100%); 
            color: white; 
            text-decoration: none; 
            border-radius: 8px; 
            font-size: 1.1em; 
            font-weight: bold; 
            text-align: center; 
            transition: transform 0.2s; 
        }
        .back-btn:hover { 
            transform: scale(1.05); 
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="/static/logo.png" alt="Luxx Dance Logo">
        </div>
        <h1>LuxxOs</h1>
        <h2>All Entries (Sorted by Age: Youngest to Oldest)</h2>
        {% for entry in sorted_entries %}
        <div class="entry">
            <div>
                <h3>{{ entry.name }}</h3>
                <p>Age: {{ entry.age }}</p>
            </div>
            <div>
                <p>Number: {{ entry.number }}</p>
            </div>
        </div>
        {% endfor %}
        <a href="/" class="back-btn">Back to Form</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, number=None)

@app.route('/submit', methods=['POST'])
def submit():
    global counter
    name = request.form['name']
    age = int(request.form['age'])
    with lock:
        if name not in names:
            names[name] = counter
            counter += 1
        number = names[name]
    entry = {'name': name, 'age': age, 'number': number}
    entries.append(entry)
    save_entry(name, age, number)
    return render_template_string(HTML_TEMPLATE, number=number)

@app.route('/view')
def view():
    sorted_entries = sorted(entries, key=lambda x: x['age'])
    return render_template_string(VIEW_TEMPLATE, sorted_entries=sorted_entries)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)