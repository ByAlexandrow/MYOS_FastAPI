from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from app.admin.admin import init_admin
from app.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

init_admin(app)

templates = Jinja2Templates(directory='app/templates')

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/media", StaticFiles(directory="static/media"), name="media")


@app.get("/", response_class=HTMLResponse, name='homepage:index')
async def get_main(request: Request):
    return templates.TemplateResponse(request, 'homepage/index.html')
