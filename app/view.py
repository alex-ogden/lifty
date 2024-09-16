from flask import render_template, jsonify, request
import sqlite3
from app import app

# Helper function to get database connection
def get_db_connection():
    conn = sqlite3.connect('workouts.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET"])
def index():
    conn = get_db_connection()
    workouts = conn.execute('SELECT * FROM workouts').fetchall()
    conn.close()
    return render_template("index.html", workouts=workouts)

@app.route("/workout/<int:workout_id>", methods=["GET"])
def workout_detail(workout_id):
    conn = get_db_connection()
    workout = conn.execute('SELECT * FROM workouts WHERE id = ?', (workout_id,)).fetchone()
    exercises = conn.execute('SELECT * FROM exercises WHERE workout_id = ?', (workout_id,)).fetchall()
    conn.close()
    return render_template("workout_detail.html", workout=workout, exercises=exercises)

@app.route("/exercise/<int:exercise_id>", methods=["GET"])
def exercise_detail(exercise_id):
    conn = get_db_connection()
    exercise = conn.execute('SELECT * FROM exercises WHERE id = ?', (exercise_id,)).fetchone()
    sets = conn.execute('SELECT * FROM sets WHERE exercise_id = ?', (exercise_id,)).fetchall()
    conn.close()
    return render_template("exercise_detail.html", exercise=exercise, sets=sets)

@app.route("/add_workout", methods=["POST"])
def add_workout():
    name = request.form['name']
    description = request.form.get('description', '')

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO workouts (name, description) VALUES (?, ?)', (name, description))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()

    return jsonify({'success': success})

@app.route("/add_exercise", methods=["POST"])
def add_exercise():
    workout_id = request.form['workout_id']
    name = request.form['name']

    conn = get_db_connection()
    conn.execute('INSERT INTO exercises (workout_id, name) VALUES (?, ?)', (workout_id, name))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

@app.route("/add_set", methods=["POST"])
def add_set():
    exercise_id = request.form['exercise_id']
    reps = request.form['reps']
    weight = request.form['weight']
    notes = request.form.get('notes', '')
    date = request.form['date']

    conn = get_db_connection()
    conn.execute('INSERT INTO sets (exercise_id, reps, weight, notes, date) VALUES (?, ?, ?, ?, ?)', (exercise_id, reps, weight, notes, date))
    conn.commit()
    conn.close()

    return jsonify({'success': True})