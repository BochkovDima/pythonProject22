import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from backend.app import models
from backend.app.database import engine
from backend.app.routers import users_router, tasks_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(tasks_router)

# Подключение статических файлов
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/static"))
if not os.path.isdir(static_dir):
    raise FileNotFoundError(f"Static files directory not found: {static_dir}")
print(f"Static files directory: {static_dir}")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Настройка Jinja2 для рендеринга шаблонов
templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/templates"))
if not os.path.isdir(templates_dir):
    raise FileNotFoundError(f"Templates directory not found: {templates_dir}")
print(f"Templates directory: {templates_dir}")
templates = Environment(loader=FileSystemLoader(templates_dir))

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        template = templates.get_template("index.html")
        return HTMLResponse(template.render())
    except TemplateNotFound:
        raise HTTPException(status_code=404, detail="Template not found")
