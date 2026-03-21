"""SQLite store for consultation metadata."""

import sqlite3
from datetime import datetime
from pathlib import Path

from app.config import settings
from app.models.schemas import ConsultationResponse

DB_PATH = settings.database_url.replace("sqlite:///", "")


def _get_db() -> sqlite3.Connection:
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS consultations (
            id TEXT PRIMARY KEY,
            patient_id TEXT NOT NULL,
            doctor_name TEXT DEFAULT '',
            consultation_date TEXT NOT NULL,
            transcript TEXT DEFAULT '',
            summary TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_patient_id ON consultations(patient_id)
    """)
    conn.commit()
    return conn


async def save_consultation(
    consultation_id: str,
    patient_id: str,
    doctor_name: str,
    consultation_date: str,
    transcript: str,
    summary: str,
    notes: str = "",
) -> None:
    conn = _get_db()
    conn.execute(
        """INSERT INTO consultations
           (id, patient_id, doctor_name, consultation_date, transcript, summary, notes, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            consultation_id,
            patient_id,
            doctor_name,
            consultation_date,
            transcript,
            summary,
            notes,
            datetime.now().isoformat(),
        ),
    )
    conn.commit()
    conn.close()


async def get_consultations(patient_id: str) -> list[ConsultationResponse]:
    conn = _get_db()
    rows = conn.execute(
        "SELECT * FROM consultations WHERE patient_id = ? ORDER BY consultation_date DESC",
        (patient_id,),
    ).fetchall()
    conn.close()
    return [ConsultationResponse(**dict(row)) for row in rows]


async def get_consultation_by_id(consultation_id: str) -> ConsultationResponse:
    conn = _get_db()
    row = conn.execute(
        "SELECT * FROM consultations WHERE id = ?", (consultation_id,)
    ).fetchone()
    conn.close()
    if not row:
        raise ValueError(f"Consultation {consultation_id} not found")
    return ConsultationResponse(**dict(row))
