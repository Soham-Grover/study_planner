import sqlite3
import hashlib

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



if __name__ == "__main__":
    create_users_table()
    print("Users Table created successfully")
    create_task_table()
    print("Tasks Table created Successfully")