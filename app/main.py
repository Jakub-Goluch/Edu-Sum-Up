from typing import Union
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static") # static files
templates = Jinja2Templates(directory="templates") # templates

# main page
@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    response = templates.TemplateResponse("index_main.html", {"request": request})
    return response

# result page
@app.get('/result', response_class=HTMLResponse)
async def result(request: Request):
    response = templates.TemplateResponse("result_page.html", {"request": request})
    return response


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
        # działa na 127.0.0.1:8000
    # terminal musi być na direcory app tzn. working directory to app
#run uvicorn main:app --reload