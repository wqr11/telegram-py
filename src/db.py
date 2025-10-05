from os import getenv
from dotenv import load_dotenv

import psycopg2

_ = load_dotenv()

POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
POSTGRES_DB = getenv("POSTGRES_DB")

db_client = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host="127.0.0.1",
    port="5432",
)

# Init DB
cursor = db_client.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS "group" (
    name VARCHAR(100) PRIMARY KEY
    );

    CREATE TABLE IF NOT EXISTS "task" (
    id SERIAL PRIMARY KEY,
    text TEXT,
    attachment TEXT,
    completed BOOLEAN,
    deleted BOOLEAN,
    due_date TIMESTAMP WITH TIME ZONE,
    CONSTRAINT not_empty CHECK (text IS NOT NULL OR attachment IS NOT NULL)
    );

    CREATE TABLE IF NOT EXISTS "_groupToTask" (
    group_name VARCHAR(100) REFERENCES "group"(name),
    task_id INTEGER REFERENCES "task"(id)
    );

    CREATE TABLE IF NOT EXISTS "student" (
    id TEXT PRIMARY KEY,
    full_name VARCHAR(100),
    group_name VARCHAR(100) REFERENCES "group"(name)
    );
    """,
)

db_client.commit()
cursor.close()
