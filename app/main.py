from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory='app/templates')


@app.get("/", response_class=HTMLResponse, name='homepage:index')
async def get_main(request: Request):
    return templates.TemplateResponse(request, 'homepage/index.html')
