from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine

from app.database import engine, Base
from app.admin.admin import setup_admin


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await create_tables(engine)

@app.on_event('startup')
async def on_startup():
    await create_tables(engine)


setup_admin(app)

templates = Jinja2Templates(directory='app/templates')

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse, name='homepage:index')
async def get_main(request: Request):
    return templates.TemplateResponse(request, 'homepage/index.html')
