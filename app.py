

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create table if not exists
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            course TEXT
        )
    ''')
    conn.close()

init_db()

# Home - View Records
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    data = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=data)

# Add Record
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        conn = sqlite3.connect('database.db')
        conn.execute('INSERT INTO students (name, age, course) VALUES (?, ?, ?)',
                     (name, age, course))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')

# Edit Record
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('database.db')

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        conn.execute('UPDATE students SET name=?, age=?, course=? WHERE id=?',
                     (name, age, course, id))
        conn.commit()
        conn.close()
        return redirect('/')

    student = conn.execute('SELECT * FROM students WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('edit.html', student=student)

# Delete Record
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    conn.execute('DELETE FROM students WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)