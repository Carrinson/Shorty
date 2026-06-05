import secrets
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="URL Shortener")

db: dict[str, str] = {}


class ShortenRequest(BaseModel):
    url: HttpUrl


@app.get("/")
def root():
    return {"message": "URL Shortener API", "docs": "/docs"}


@app.post("/shorten", status_code=201)
def shorten(body: ShortenRequest):
    code = secrets.token_urlsafe(6)[:6]
    while code in db:
        code = secrets.token_urlsafe(6)[:6]
    db[code] = str(body.url)
    return {"code": code, "short_url": f"http://localhost:8000/r/{code}"}


@app.get("/r/{code}")
def redirect(code: str):
    url = db.get(code)
    if not url:
        raise HTTPException(status_code=404, detail="Short code not found")
    return RedirectResponse(url=url, status_code=307)


@app.get("/urls")
def list_urls():
    return db


@app.delete("/r/{code}", status_code=204)
def delete(code: str):
    if code not in db:
        raise HTTPException(status_code=404, detail="Short code not found")
    del db[code]
