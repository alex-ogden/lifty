from app import app

from flask import render_template, jsonify, request, redirect
from collections import defaultdict
from datetime import datetime

import sqlite3

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

    # Group sets by date
    sets_by_date = defaultdict(list)
    for set in sets:
        # Convert the date string to a date object (assuming it's in the format 'YYYY-MM-DD HH:MM:SS')
        date_str = set['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').date()
        sets_by_date[date_obj].append(set)

    # Convert defaultdict to a regular dict and sort by date
    sorted_sets_by_date = dict(sorted(sets_by_date.items(), reverse=True))

    return render_template("exercise_detail.html", exercise=exercise, sets_by_date=sorted_sets_by_date)

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

@app.route("/delete_set/<int:set_id>", methods=["POST"])
def delete_set(set_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM sets WHERE id = ?', (set_id,))
    conn.commit()
    conn.close()
    # Redirect back to the exercise detail page
    return redirect(request.referrer)

@app.route("/delete_exercise/<int:exercise_id>", methods=["POST"])
def delete_exercise(exercise_id):
    conn = get_db_connection()
    # First, delete all sets associated with this exercise
    conn.execute('DELETE FROM sets WHERE exercise_id = ?', (exercise_id,))
    # Then, delete the exercise itself
    conn.execute('DELETE FROM exercises WHERE id = ?', (exercise_id,))
    conn.commit()
    conn.close()
    # Redirect back to the workout detail page
    return redirect(request.referrer)

@app.route("/delete_workout/<int:workout_id>", methods=["POST"])
def delete_workout(workout_id):
    conn = get_db_connection()
    # First, delete all exercises and their sets associated with this workout
    exercises = conn.execute('SELECT id FROM exercises WHERE workout_id = ?', (workout_id,)).fetchall()
    for exercise in exercises:
        conn.execute('DELETE FROM sets WHERE exercise_id = ?', (exercise['id'],))
    conn.execute('DELETE FROM exercises WHERE workout_id = ?', (workout_id,))
    # Then, delete the workout itself
    conn.execute('DELETE FROM workouts WHERE id = ?', (workout_id,))
    conn.commit()
    conn.close()
    # Redirect back to the main page
    return redirect("/")