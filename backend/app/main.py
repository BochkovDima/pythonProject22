from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
import os

from backend.app import models
from backend.app.database import engine
from backend.app.routers import users_router, tasks_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(tasks_router)

# Подключение статических файлов
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../../frontend/static")), name="static")

# Настройка Jinja2 для рендеринга шаблонов
templates = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "../../frontend/templates")))

@app.get("/", response_class=HTMLResponse)
async def read_root():
    template = templates.get_template("index.html")
    return HTMLResponse(template.render())