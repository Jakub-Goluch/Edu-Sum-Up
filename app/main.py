import os
import shutil
import uvicorn
from fastapi import FastAPI, Request
from fastapi import File
from fastapi import UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from utils.text_summarization import text_summarization

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")  # static files
templates = Jinja2Templates(directory="templates")  # templates


# main page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    response = templates.TemplateResponse("index_main.html", {"request": request})
    return response


# result page
@app.get("/result", response_class=HTMLResponse)
async def result(request: Request, summary: str):
    return templates.TemplateResponse(
        "result_page.html", {"request": request, "summary": summary}
    )


@app.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        summary = text_summarization(file.filename)
        os.remove(file.filename)  # remove the file after processing
    except Exception as e:
        print(f"Error: {e}")  # print the error message
        raise HTTPException(
            status_code=400, detail="An error occurred while processing the file."
        )
    return RedirectResponse(url=f"/result?summary={summary}", status_code=303)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # works on na 127.0.0.1:8000
    # working directory set to app folder
# run uvicorn main:app --reload
