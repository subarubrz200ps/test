from __future__ import annotations

import os
from typing import Any

import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.evaluator import SearchItem, evaluate

app = FastAPI(title="Medical Evidence Evaluator")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def google_search(query: str, num: int = 8) -> list[SearchItem]:
    key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CSE_ID")

    if not key or not cx:
        demo = [
            SearchItem(
                title="WHO: Physical activity guidelines",
                snippet="Global recommendations include evidence summaries and systematic reviews.",
                url="https://www.who.int/news-room/fact-sheets/detail/physical-activity",
            ),
            SearchItem(
                title="NIH: Benefits of exercise",
                snippet="Review of health effects and references to randomized controlled trials.",
                url="https://www.nih.gov/news-events",
            ),
            SearchItem(
                title="Random blog about exercise",
                snippet="Personal experience and expert opinion only.",
                url="https://example-health-blog.com/exercise-tips",
            ),
        ]
        return demo

    params: dict[str, Any] = {
        "key": key,
        "cx": cx,
        "q": query,
        "num": min(max(num, 1), 10),
        "hl": "ja",
    }
    resp = requests.get("https://www.googleapis.com/customsearch/v1", params=params, timeout=15)
    resp.raise_for_status()
    payload = resp.json()

    items = []
    for item in payload.get("items", []):
        items.append(
            SearchItem(
                title=item.get("title", ""),
                snippet=item.get("snippet", ""),
                url=item.get("link", ""),
            )
        )
    return items


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/evaluate")
def api_evaluate(q: str, num: int = 8):
    try:
        items = google_search(q, num=num)
        result = evaluate(items)
        result["query"] = q
        result["count"] = len(items)
        return JSONResponse(result)
    except Exception as exc:  # noqa: BLE001
        return JSONResponse({"error": str(exc)}, status_code=400)
