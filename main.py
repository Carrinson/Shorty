import re
import secrets

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl, field_validator

app = FastAPI(title="URL Shortener")

db: dict[str, dict] = {}

ALIAS_RE = re.compile(r"^[A-Za-z0-9_-]{3,32}$")


class ShortenRequest(BaseModel):
    url: HttpUrl
    alias: str | None = None

    @field_validator("alias")
    @classmethod
    def validate_alias(cls, v: str | None) -> str | None:
        if v is not None and not ALIAS_RE.match(v):
            raise ValueError("alias must be 3-32 chars: letters, numbers, _ or -")
        return v


def make_short_url(code: str) -> str:
    return f"/r/{code}"


@app.post("/api/shorten", status_code=201)
def shorten(body: ShortenRequest):
    if body.alias:
        if body.alias in db:
            raise HTTPException(status_code=409, detail="Alias already taken")
        code = body.alias
    else:
        code = secrets.token_urlsafe(6)[:6]
        while code in db:
            code = secrets.token_urlsafe(6)[:6]

    db[code] = {"url": str(body.url), "clicks": 0}
    return {"code": code, "short_url": make_short_url(code)}


@app.get("/api/urls")
def list_urls():
    return [
        {"code": code, "url": entry["url"], "clicks": entry["clicks"], "short_url": make_short_url(code)}
        for code, entry in db.items()
    ]


@app.delete("/api/r/{code}", status_code=204)
def delete(code: str):
    if code not in db:
        raise HTTPException(status_code=404, detail="Short code not found")
    del db[code]


@app.get("/r/{code}")
def redirect(code: str):
    entry = db.get(code)
    if not entry:
        raise HTTPException(status_code=404, detail="Short code not found")
    entry["clicks"] += 1
    return RedirectResponse(url=entry["url"], status_code=307)


app.mount("/", StaticFiles(directory="static", html=True), name="static")
