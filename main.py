from fastapi import FastAPI, Depends, Request
import uvicorn
import sqlite3
import os

import tools
from route.user import login, register

app = FastAPI()

# 라우터
app.include_router(login.router)


if __name__ == "__main__":
    if not os.path.isfile('./db.sqlite'):
        tools.db.db_init()

    conn = sqlite3.connect('./db.sqlite')
    curs = conn.cursor()
    curs.execute('select value from setting where name = ?', ('port',))
    port = int(curs.fetchone()[0])
    uvicorn.run(app, host="0.0.0.0", port=port)