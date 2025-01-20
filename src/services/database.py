import os
import asyncpg

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

async def connect_db() -> asyncpg.Connection:
    conn = await asyncpg.connect(DATABASE_URL)
    return conn

async def close_db(conn: asyncpg.Connection):
    await conn.close()

async def create_tables(conn: asyncpg.Connection):
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS skills(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL        
        );
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS portfolio(
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            image VARCHAR(255) NOT NULL,
            alt VARCHAR(255) NOT NULL,
            href VARCHAR(255) NOT NULL,
            types VARCHAR(255) NOT NULL
        );
    ''')