from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os
import psycopg2

DB_HOST = os.getenv("DB_HOST", "analytics-db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "bfh_analytics")
DB_USER = os.getenv("DB_USER", "analytics")
DB_PASSWORD = os.getenv("DB_PASSWORD", "analytics_pass")

app = FastAPI(title="BFH Analytics Collector")

# Разрешаем запросы с фронта (поставь сюда IP сервера с сайтом)
origins = [
    "http://3.74.161.84",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

class PageViewEvent(BaseModel):
    event_type: str
    event_timestamp: datetime
    site_id: str
    page_path: str
    language: str | None = None
    device_type: str | None = None
    referrer_type: str | None = None
    referrer_domain: str | None = None
    extra: dict | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/collect")
def collect(event: PageViewEvent):
    # на всякий случай отфильтруем только page_view
    if event.event_type != "page_view":
        raise HTTPException(status_code=400, detail="Unsupported event_type")

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO page_events (
              event_timestamp,
              site_id,
              page_path,
              language,
              device_type,
              referrer_type,
              referrer_domain,
              extra
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                event.event_timestamp,
                event.site_id,
                event.page_path,
                event.language,
                event.device_type,
                event.referrer_type,
                event.referrer_domain,
                event.extra,
            ),
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception:
        # для прототипа без подробностей
        raise HTTPException(status_code=500, detail="DB insert failed")

    return {"status": "ok"}
