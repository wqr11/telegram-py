from os import getenv
from dotenv import load_dotenv

import psycopg2

_ = load_dotenv()

POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
POSTGRES_DB = getenv("POSTGRES_DB")

print(POSTGRES_USER, POSTGRES_PASSWORD)

db_client = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host="127.0.0.1",
    port="5432",
)

# Init DB
cursor = db_client.cursor()

cursor.executemany(
    """
    CREATE TABLE IF NOT EXISTS "group" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
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
    group_id INTEGER REFERENCES group,
    task_id INTEGER REFERENCES task
    );

    CREATE TABLE IF NOT EXISTS "student" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    last_name VARCHAR(100),
    group_id INTEGER REFERENCES group
    );
    """,
    [],
)

db_client.commit()
