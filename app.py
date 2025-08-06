from flask import Flask, request, render_template, jsonify
import mysql.connector
import os

app = Flask(__name__)

# ✅ Define database config properly
db_config = {
    'host': os.environ.get("DB_HOST", "localhost"),
    'port': int(os.environ.get("DB_PORT", 3306)),
    'user': os.environ.get("DB_USER", "root"),
    'password': os.environ.get("DB_PASSWORD", ""),
    'database': os.environ.get("DB_NAME", "school")
}

# ✅ Optional: Initial connection test
try:
    test_conn = mysql.connector.connect(**db_config)
    print("Connected to database:", test_conn.is_connected())
    test_conn.close()
except Exception as e:
    print("Connection failed:", e)

# ✅ DB connection function
def get_db_connection():
    return mysql.connector.connect(**db_config)

# ✅ Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO students (id, name, section, cid) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (data['id'], data['name'], data['section'], data['cid']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Student added"})

@app.route('/add_course', methods=['POST'])
def add_course():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO courses (cid, cname) VALUES (%s, %s)"
    cursor.execute(query, (data['cid'], data['cname']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Course added"})

@app.route('/run_query', methods=['POST'])
def run_query():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(data['query'])
        result = cursor.fetchall()
        conn.commit()
    except Exception as e:
        result = {"error": str(e)}
    cursor.close()
    conn.close()
    return jsonify(result)
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            cid INT PRIMARY KEY,
            cname VARCHAR(100)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            section VARCHAR(10),
            cid INT,
            FOREIGN KEY (cid) REFERENCES courses(cid)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)

