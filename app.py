from flask import Flask, request, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)

# Conexión con la base de datos
def get_db_connection():
    conn = sqlite3.connect('comments.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear la base de datos y tabla si no existen
def init_db():
    if not os.path.exists('comments.db'):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                rating INTEGER,
                comment TEXT
            )
        ''')
        conn.commit()
        conn.close()

init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    comments = conn.execute('SELECT * FROM comments ORDER BY id DESC LIMIT 5').fetchall()
    conn.close()
    return render_template('index.html', comments=comments)

@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    name = request.form.get('name') or 'Anónimo'
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    conn = get_db_connection()
    conn.execute('INSERT INTO comments (name, rating, comment) VALUES (?, ?, ?)', (name, rating, comment))
    conn.commit()
    conn.close()
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
