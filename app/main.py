import os
import shutil
import threading
import uvicorn
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from urllib.parse import quote_plus, unquote_plus
import json

from utils.keywords import search_keyphrases
from utils.related_publications_searcher import SemanticScholarScraper
from utils.text_summarization import text_summarization

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index_main.html", {"request": request})


@app.get("/result", response_class=HTMLResponse)
async def result(request: Request, summary: str, publications: str, keywords: str):
    decoded_publications = json.loads(unquote_plus(publications))
    decoded_keywords = json.loads(unquote_plus(keywords))
    return templates.TemplateResponse(
        "result_page.html",
        {
            "request": request,
            "summary": summary,
            "publications": decoded_publications,
            "keywords": decoded_keywords,
        },
    )


def process_text(file_name, results):
    try:
        print("Text processing...")
        summary = text_summarization(file_name)
        results.update({"summary": summary})
    except Exception as e:
        print(f"Text processing error: {e}")


def fetch_publications(file_name, results):
    try:
        keywords = search_keyphrases(file_name)
        scraper = SemanticScholarScraper()
        print("Publications fetching...")
        publications = scraper.get_related_publications(keywords)
        results.update({"publications": [
            pub["title"] + ' - ' + ', '.join(pub["authors"]) + ' - ' + pub["publication_date"] for pub in publications],
                        "keywords": keywords})
    except Exception as e:
        print(f"Publication fetching error: {e}")


@app.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        results = {}
        # Creating threads
        text_thread = threading.Thread(
            target=process_text, args=(file.filename, results)
        )
        publications_thread = threading.Thread(
            target=fetch_publications, args=(file.filename, results)
        )

        # Starting threads
        text_thread.start()
        publications_thread.start()

        # Joining threads
        text_thread.join()
        publications_thread.join()

        if "summary" not in results or "keywords" not in results:
            raise Exception("Error during text processing.")

        publications_json = json.dumps(results.get("publications", []))
        encoded_publications = quote_plus(publications_json)

        keywords_json = json.dumps(results.get("keywords", []))
        encoded_keywords = quote_plus(keywords_json)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=400, detail="An error occurred while processing the file."
        )
    finally:
        if os.path.exists(file.filename):
            os.remove(file.filename)

    return RedirectResponse(
        url=f"/result?summary={quote_plus(results.get('summary', ''))}&publications={encoded_publications}&keywords={encoded_keywords}",
        status_code=303,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
