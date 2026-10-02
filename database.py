import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB = "database/resume_system.db"


def connect():
    return sqlite3.connect(DB)


def init_db():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT,
            job_role TEXT,
            match_score REAL,
            skills TEXT,
            missing_skills TEXT,
            llm_analysis TEXT
        )
    """)

    conn.commit()
    conn.close()


def register_user(name, email, password):

    try:

        conn = connect()

        conn.execute(
            """
            INSERT INTO users
            (name, email, password)
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                generate_password_hash(password)
            )
        )

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:

        return False


def login_user(email, password):

    conn = connect()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    conn.close()

    if user and check_password_hash(user[3], password):
        return user

    return None


def save_analysis(
    user_id,
    filename,
    job_role,
    score,
    skills,
    missing,
    llm
):

    conn = connect()

    conn.execute(
        """
        INSERT INTO analyses
        (
            user_id,
            filename,
            job_role,
            match_score,
            skills,
            missing_skills,
            llm_analysis
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            filename,
            job_role,
            score,
            ", ".join(skills),
            ", ".join(missing),
            llm
        )
    )

    conn.commit()
    conn.close()


def get_user_analyses(user_id):

    conn = connect()

    data = conn.execute(
        """
        SELECT *
        FROM analyses
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    ).fetchall()

    conn.close()

    return data