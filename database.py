import sqlite3
import hashlib
import json

def get_connection():
    conn = sqlite3.connect("study_planner.db")
    return conn

def create_users_table():
    conn = get_connection()
    cursor =conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def create_student_profile_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_profiles (
    user_id INTEGER,
    grade INTEGER,
    board TEXT,
    subjects TEXT,
    productive_time INTEGER,
    study_hours INTEGER)""")

    conn.commit()
    conn.close()

def create_task_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    task TEXT NOT NULL,
    priority TEXT, 
    due_date TEXT,
    is_done BOOLEAN DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    conn.commit()
    conn.close()

def create_exam_plans_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exam_plans (
        user_id INTEGER PRIMARY KEY,
        subject_list TEXT,
        chapter_list TEXT,
        exam_dates TEXT,
        exam_dates_subjects TEXT,
        day_wise_plan TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, hash_password(password)))
    generated_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return generated_id

def user_auth(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username  = ? AND password_hash = ?", (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def add_quest(user_id, task, priority, due_date, is_done):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks
        (user_id, task, priority, due_date, is_done)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, task, priority, due_date, is_done)
    )

    new_task_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return new_task_id


def update_quest(task_id, task_name, priority, due_date, is_done):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET task = ?, priority = ?, due_date = ?, is_done = ? WHERE task_id = ?",
        (task_name, priority, due_date, is_done, task_id)
    )
    conn.commit()
    conn.close()

def delete_quest(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
    conn.commit()
    conn.close()

def get_quests(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT task_id, task, priority, due_date, is_done FROM tasks WHERE user_id = ?", (user_id,))
    quests = cursor.fetchall()
    conn.close()
    return quests

def add_student_profile(user_id, grade, board, subjects, productive_time, study_hours):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO student_profiles (user_id, grade, board, subjects, productive_time, study_hours) VALUES (?, ?, ?, ?, ?, ?)", (user_id, grade, board, json.dumps(subjects), json.dumps(productive_time), study_hours))
    conn.commit()
    conn.close()

def get_student_profile(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT grade, board, subjects, productive_time, study_hours FROM student_profiles WHERE user_id = ?",
                   (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "grade": row[0],
            "board": row[1],
            "subjects": json.loads(row[2]),
            "productive_time": json.loads(row[3]),
            "study_hours": row[4]
        }
    return None


def save_exam_plan(user_id, subject_list, chapter_list, exam_dates, exam_dates_subjects, day_wise_plan):
    conn = get_connection()
    cursor = conn.cursor()

    # Convert Pydantic object to a JSON-serializable dictionary
    plan_dict = day_wise_plan.model_dump() if hasattr(day_wise_plan, "model_dump") else day_wise_plan

    cursor.execute(
        """INSERT OR REPLACE INTO exam_plans 
           (user_id, subject_list, chapter_list, exam_dates, exam_dates_subjects, day_wise_plan) 
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            user_id,
            json.dumps(subject_list),
            json.dumps(chapter_list),
            json.dumps(exam_dates),
            json.dumps(exam_dates_subjects),
            json.dumps(plan_dict)
        )
    )
    conn.commit()
    conn.close()


def get_exam_plan(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT subject_list, chapter_list, exam_dates, exam_dates_subjects, day_wise_plan FROM exam_plans WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "subject_list": json.loads(row[0]),
            "chapter_list": json.loads(row[1]),
            "exam_dates": json.loads(row[2]),
            "exam_dates_subjects_ordered": json.loads(row[3]),
            "day_wise_plan": json.loads(row[4])
        }
    return None


def change_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""ALTER TABLE users ADD COLUMN xp INTEGER DEFAULT 0""")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()

def update_xp_tasks_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TRIGGER IF EXISTS update_xp;")

    cursor.execute("""
            CREATE TRIGGER update_xp
            AFTER UPDATE OF is_done ON tasks
            FOR EACH ROW
            BEGIN
                UPDATE users
                SET xp = MAX(0, COALESCE(xp, 0) + CASE
                    WHEN OLD.is_done = 0 AND NEW.is_done = 1 THEN 20
                    WHEN OLD.is_done = 1 AND NEW.is_done = 0 THEN -20
                    ELSE 0
                END)
                WHERE user_id = NEW.user_id;
            END;
        """)

    conn.commit()
    conn.close()


def get_xp(userid):
    conn = get_connection()
    cursor = conn.cursor()
    xp = cursor.execute("SELECT xp from users WHERE user_id = ?", userid)
    conn.commit()
    conn.close()

    return xp


if __name__ == "__main__":
    create_users_table()
    print("Users Table created successfully")
    create_task_table()
    print("Tasks Table created Successfully")
    create_student_profile_table()
    print("Create Student Profile Table Successful")
    create_exam_plans_table()
    print("Plans Table Successful")
    change_users_table()
    print("Tasks changed")
    update_xp_tasks_table()
    print("Trigger ADDED")