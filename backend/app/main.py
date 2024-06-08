import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

from backend.app import models
from backend.app.database import engine
from backend.app.routers import users_router, tasks_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(tasks_router)

# Подключение статических файлов
static_dir = os.path.join(os.path.dirname(__file__), "../../frontend/static")
print(f"Static files directory: {static_dir}")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Настройка Jinja2 для рендеринга шаблонов
templates_dir = os.path.join(os.path.dirname(__file__), "../../frontend/templates")
print(f"Templates directory: {templates_dir}")
templates = Environment(loader=FileSystemLoader(templates_dir))

@app.get("/", response_class=HTMLResponse)
async def read_root():
    template = templates.get_template("index.html")
    return HTMLResponse(template.render())
