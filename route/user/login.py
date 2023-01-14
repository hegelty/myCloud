from typing import Union

import aiosqlite
from fastapi import APIRouter, Cookie, Request, Form, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from tools import tool
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="templates")


class LoginData(BaseModel):
    user_id: str
    pw: str


@router.get("/login")
async def login_get(request: Request, session_id: Union[str, None] = Cookie(default=None)):
    if tool.user.login_check(session_id):
        return RedirectResponse(url="/")

    return templates.TemplateResponse("/user/login.html", {"request": request,
                                                           "error": ""})


@router.post("/login")
async def login_post(request: Request, user_id: str = Form(...), pw: str = Form(...), db: aiosqlite.Connection = Depends(tool.db.get_db)):
    data = await db.execute("select * from user where id = ?", (user_id,))
    data = await data.fetchone()

    if data is None:
        return templates.TemplateResponse("/user/login.html", {"request": request,
                                                               "error": "유저를 찾을 수 없습니다. id를 확인해주세요."})

    if tool.user.pw_hash(pw) != data[2]:
        return templates.TemplateResponse("/user/login.html", {"request": request,
                                                               "error": "비밀번호가 일치하지 않습니다."})

    session_id, expire = tool.user.session_create(user_id)
    await db.execute("insert into session (id, user_id, expire) values (?, ?, ?)",
                     (session_id, user_id, str(expire)))
    await db.commit()
    response = RedirectResponse(url="/")
    response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True, expires=600, max_age=3600)
    return response
