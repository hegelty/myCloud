import sqlite3
import aiosqlite
import os


def db_init():
    conn = sqlite3.connect('./db.sqlite')
    curs = conn.cursor()
    curs.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id TEXT PRIMARY KEY,
        nickname TEXT NOT NULL,
        pw TEXT NOT NULL,
        email TEXT,
        size INTEGER NOT NULL,
        grade TEXT NOT NULL
    )
    ''')
    curs.execute('''
    CREATE TABLE IF NOT EXISTS shared_file (
        id TEXT PRIMARY KEY,
        owner TEXT NOT NULL,
        share_type TEXT NOT NULL,
        route TEXT NOT NULL,
        allowed INTEGER NOT NULL,
        pw TEXT,
        expire TEXT,
        url INTEGER NOT NULL,
        allowed_users TEXT
    )
    ''')
    curs.execute('''
    CREATE TABLE IF NOT EXISTS shared_folder (
        id TEXT PRIMARY KEY,
        owner TEXT NOT NULL,
        share_type TEXT NOT NULL,
        route TEXT NOT NULL,
        allowed INTEGER NOT NULL,
        pw TEXT,
        expire TEXT,
        url INTEGER NOT NULL,
        allowed_users TEXT
    )
    ''')
    curs.execute('''
    CREATE TABLE IF NOT EXISTS log (
        log_type TEXT NOT NULL,
        id TEXT NOT NULL,
        time TEXT NOT NULL,
        detail TEXT NOT NULL
    )
    ''')
    curs.execute('''
    CREATE TABLE IF NOT EXISTS setting (
        name TEXT PRIMARY KEY,
        value TEXT
    )
    ''')
    curs.execute('''
    CREATE TABLE IF NOT EXISTS session (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        expire TEXT
    )
    ''')

    print('DB init\n====================\nPort(8818): ', end='')
    port = input()
    if port == '':
        port = 8818
    else:
        try:
            port = int(port)
        except Exception as e:
            print('Port must be integer')
            conn.close()
            os.remove('./db.sqlite')
            exit()
    curs.execute('''
    INSERT INTO setting (name, value) VALUES (?, ?)
    ''', ('port', str(port))
    )
    conn.commit()
    conn.close()
    print('DB init completed')


async def get_db():
    db = await aiosqlite.connect('./db.sqlite')
    try:
        yield db
    finally:
        await db.close()
