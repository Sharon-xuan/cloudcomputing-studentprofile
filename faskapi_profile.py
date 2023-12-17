from urllib import request

from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 示例数据存储（在实际应用中应该替换为数据库）
students = [
    {'uni':'zl3218','name':'Zixuan Li','schedule':'Monday','interests':'cloud computing'},
    {'uni':'yf2633','name':'Yuxiao Fei','schedule':'Monday','interests':'cloud computing'},
    {'uni':'rw2959','name':'Ruobing Wang','schedule':'Monday','interests':'cloud computing'},
    {'uni':'ym2876','name':'Philip Ma','schedule':'Monday','interests':'cloud computing'},
    {'uni':'lz2933','name':'Lanyue Zhang','schedule':'Monday','interests':'cloud computing'},
    {'uni':'qf2172','name':'Quan Fang','schedule':'Monday','interests':'cloud computing'}
]

@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/")
async def process_login(username: str = Form(...), password: str = Form(...)):
    if username == 'admin' and password == '123456':
        return RedirectResponse(url="/admin", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request, "students": students})


# 程序入口
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8013)
