import sqlite3

def init_db():
    conn = sqlite3.connect('workouts.db')
    cursor = conn.cursor()

    # Create table for workouts
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT
    )
    ''')

    # Create table for exercises
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workout_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (workout_id) REFERENCES workouts (id)
    )
    ''')

    # Create table for sets
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise_id INTEGER NOT NULL,
        reps INTEGER NOT NULL,
        weight REAL NOT NULL,
        notes TEXT,
        date TEXT NOT NULL,
        FOREIGN KEY (exercise_id) REFERENCES exercises (id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()