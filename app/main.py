import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Link
from .utils import encode_base62

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


class ShortenRequest(BaseModel):
    url: HttpUrl


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/api/shorten")
def shorten(payload: ShortenRequest, db: Session = Depends(get_db)):
    link = Link(original_url=str(payload.url))
    db.add(link)
    db.flush()  # gets the auto-generated id
    link.code = encode_base62(link.id + 100000)
    db.commit()
    return {"code": link.code, "short_url": f"{BASE_URL}/{link.code}"}


@app.get("/api/stats/{code}")
def stats(code: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.code == code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return {
        "code": link.code,
        "original_url": link.original_url,
        "clicks": link.clicks,
        "created_at": link.created_at,
    }


@app.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.code == code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    link.clicks += 1
    db.commit()
    return RedirectResponse(link.original_url, status_code=302)