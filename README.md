# URL Shortener

A simple URL shortener built with FastAPI and a vanilla HTML/JS frontend. Shorten links, use custom aliases, and track click counts.

## Features

- Shorten any URL, with an optional custom alias
- Redirect via short link with click tracking
- List and delete existing links
- No database — in-memory storage, no build step for the frontend

## Tech Stack

- **Backend:** FastAPI, served with Uvicorn
- **Frontend:** Plain HTML/CSS/JS, served directly by FastAPI via `StaticFiles`
- **Package management:** [uv](https://docs.astral.sh/uv/)

## Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Setup

```bash
uv sync
```

### Run locally

```bash
uv run uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) for the app, or [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API docs.

## API

| Method | Path             | Description                                  |
|--------|------------------|-----------------------------------------------|
| POST   | `/api/shorten`   | Body: `{"url": "...", "alias": "optional"}`   |
| GET    | `/r/{code}`      | Redirects to the original URL, counts clicks |
| GET    | `/api/urls`      | Lists all shortened links                     |
| DELETE | `/api/r/{code}`  | Deletes a shortened link                      |

## Deployment

This repo supports either Render or Railway — pick whichever you prefer.

### Railway

Uses [`railway.json`](railway.json), built via Nixpacks (which natively supports `uv.lock`, no `requirements.txt` needed):

1. Push this repo to GitHub
2. On Railway, create a new project and link the repo
3. Railway picks up `railway.json` automatically (start: `uvicorn main:app --host 0.0.0.0 --port $PORT`)

### Render

Uses [`render.yaml`](render.yaml):

1. Push this repo to GitHub
2. On Render, create a new Web Service and connect the repo
3. Render picks up `render.yaml` automatically (build: `pip install -r requirements.txt`, start: `uvicorn main:app --host 0.0.0.0 --port $PORT`)

If you update dependencies, regenerate `requirements.txt` (only needed for Render):

```bash
uv export --no-hashes --no-dev -o requirements.txt
```

## License

MIT
