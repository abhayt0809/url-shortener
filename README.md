# URL Shortener

A fast URL shortener with click tracking, built with FastAPI, SQLAlchemy and PostgreSQL.

**Live demo:** https://url-shortener-udcn.onrender.com

**API docs:** https://url-shortener-udcn.onrender.com/docs

> Hosted on free tiers, so the first request after a period of inactivity may take up to a minute to wake the server.

## Features
- Shorten any http/https URL
- Base62-encoded short codes generated from database IDs (no collisions)
- 302 redirects, so every click reaches the server and is counted
- Per-link stats endpoint (original URL, click count, creation time)
- Input validation with Pydantic
- Interactive API documentation (Swagger UI) at `/docs`
- Works with SQLite locally and PostgreSQL in production, switched with one environment variable

## Tech stack
| Layer | Technology |
|---|---|
| Language | Python 3 |
| Backend | FastAPI, Uvicorn |
| Database | SQLAlchemy, SQLite (local), PostgreSQL on Neon (production) |
| Frontend | HTML, CSS, JavaScript (React dashboard planned) |
| Hosting | Render (app), Neon (database) |

## How it works
1. The client sends a long URL to `POST /api/shorten`.
2. The server validates it, saves it, and encodes the row ID in Base62 to produce the short code.
3. Opening `/{code}` looks up the link, increments its click counter, and redirects to the original URL.

## API endpoints
| Method | Route | Description |
|---|---|---|
| GET | `/` | Home page |
| POST | `/api/shorten` | Create a short link. Body: `{"url": "https://example.com"}` |
| GET | `/api/stats/{code}` | Click count and details for a link |
| GET | `/{code}` | Redirect to the original URL |

## Run locally
```bash
git clone https://github.com/abhayt0809/url-shortener.git
cd url-shortener
python -m venv venv
venv\Scripts\activate        # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open `http://localhost:8000` for the app and `http://localhost:8000/docs` for the API docs.

## Environment variables
| Variable | Purpose | Default |
|---|---|---|
| `DATABASE_URL` | Database connection string | `sqlite:///./local.db` |
| `BASE_URL` | Public URL used in generated short links | `http://localhost:8000` |

Create a `.env` file for local overrides. It is git-ignored, so secrets never reach GitHub.

## Project structure
```
url-shortener/
  app/
    database.py    # engine and session setup
    models.py      # Link table
    utils.py       # Base62 encoding
    main.py        # routes
  static/
    index.html     # simple frontend
  requirements.txt
```

## Roadmap
- [x] MVP: shorten, redirect, click counting
- [x] Deploy with Render and Neon
- [ ] Custom aliases and link expiry
- [ ] Better URL validation and abuse protection
- [ ] Alembic database migrations
- [ ] Redis caching and rate limiting
- [ ] React analytics dashboard
- [ ] Docker, tests and load testing

## License
MIT. See [LICENSE](LICENSE).