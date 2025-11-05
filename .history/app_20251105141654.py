import os
from flask import Flask, render_template, request, redirect, url_for, g
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Get database URL from environment variable
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/govfunds')

# Helper to get DB connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return db

# Close DB on app teardown
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Initialize DB by executing the SQL file
def init_db():
    try:
        with app.app_context():
            db = get_db()
            with open('create_database.sql', 'r') as f:
                sql_script = f.read()
            cursor = db.cursor()
            cursor.execute(sql_script)
            db.commit()
            cursor.close()
    except Exception as e:
        print(f"Database initialization error (this is normal if already initialized): {e}")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/budget')
def budget():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM budget')
    budgets = cursor.fetchall()
    cursor.close()
    return render_template('budget.html', budgets=budgets)

@app.route('/spending')
def spending():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM budget')
    budgets = cursor.fetchall()
    cursor.close()
    return render_template('spending.html', budgets=budgets)

@app.route('/projects')
def projects():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM projects')
    projects_data = cursor.fetchall()
    cursor.close()
    return render_template('projects.html', projects_data=projects_data)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        comment = request.form.get('comment')
        if name and comment:
            db = get_db()
            db.execute('INSERT INTO feedback (name, comment) VALUES (?, ?)', (name, comment))
            db.commit()
        return redirect(url_for('feedback'))
    db = get_db()
    feedback_data = db.execute('SELECT * FROM feedback').fetchall()
    return render_template('feedback.html', feedback_data=feedback_data)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        dept = request.form.get('department')
        allocated = float(request.form.get('allocated', 0))
        spent = float(request.form.get('spent', 0))
        db = get_db()
        db.execute('UPDATE budget SET allocated = ?, spent = ? WHERE department = ?', (allocated, spent, dept))
        db.commit()
        
        proj_name = request.form.get('project_name')
        proj_status = request.form.get('project_status')
        proj_budget = float(request.form.get('project_budget', 0))
        if proj_name:
            db.execute('INSERT INTO projects (name, status, budget) VALUES (?, ?, ?)', (proj_name, proj_status, proj_budget))
            db.commit()
        return redirect(url_for('home'))
    return render_template('upload.html')

if __name__ == '__main__':
    init_db()  # Load and execute the SQL file
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)