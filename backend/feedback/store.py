from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
import uuid

from .models import FeedbackCreate, FeedbackRecord, ReviewStatus, TriageStatus


ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "new": {"reviewed"},
    "reviewed": {"accepted_bad_case", "not_a_system_error", "duplicate"},
    "accepted_bad_case": set(),
    "not_a_system_error": set(),
    "duplicate": set(),
}

TRIAGE_TO_REVIEW: dict[str, ReviewStatus] = {
    "new": "new",
    "reviewed": "triaged",
    "accepted_bad_case": "regression_candidate",
    "not_a_system_error": "ignored",
    "duplicate": "ignored",
}
REVIEW_STATUSES = {"new", "triaged", "regression_candidate", "fixed", "ignored"}


class FeedbackStore:
    def __init__(self, data_dir: Path):
        self.path = data_dir.resolve() / "feedback.sqlite3"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=30)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS feedback (
                    feedback_id TEXT PRIMARY KEY,
                    trace_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    helpful INTEGER CHECK (helpful IN (0, 1) OR helpful IS NULL),
                    category TEXT NOT NULL,
                    user_comment TEXT,
                    triage_status TEXT NOT NULL CHECK (
                        triage_status IN ('new', 'reviewed', 'accepted_bad_case',
                                          'not_a_system_error', 'duplicate')
                    ),
                    review_status TEXT NOT NULL DEFAULT 'new' CHECK (
                        review_status IN ('new', 'triaged', 'regression_candidate',
                                          'fixed', 'ignored')
                    ),
                    reviewer_note TEXT
                )
                """
            )
            columns = {row[1] for row in connection.execute("PRAGMA table_info(feedback)")}
            if "review_status" not in columns:
                connection.execute(
                    """ALTER TABLE feedback ADD COLUMN review_status TEXT NOT NULL
                    DEFAULT 'new' CHECK (review_status IN
                    ('new', 'triaged', 'regression_candidate', 'fixed', 'ignored'))"""
                )
                connection.execute(
                    """UPDATE feedback SET review_status = CASE triage_status
                    WHEN 'reviewed' THEN 'triaged'
                    WHEN 'accepted_bad_case' THEN 'regression_candidate'
                    WHEN 'not_a_system_error' THEN 'ignored'
                    WHEN 'duplicate' THEN 'ignored'
                    ELSE 'new' END"""
                )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS feedback_trace_idx ON feedback(trace_id)"
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS feedback_triage_idx ON feedback(triage_status, created_at)"
            )

    @staticmethod
    def _record(row: sqlite3.Row) -> FeedbackRecord:
        value = dict(row)
        value["helpful"] = None if value["helpful"] is None else bool(value["helpful"])
        value["created_at"] = datetime.fromisoformat(value["created_at"])
        return FeedbackRecord.model_validate(value)

    def create(self, request: FeedbackCreate) -> FeedbackRecord:
        with self._connect() as connection:
            existing = connection.execute(
                "SELECT * FROM feedback WHERE trace_id = ? AND helpful IS ? ORDER BY created_at DESC LIMIT 1",
                (request.trace_id, None if request.helpful is None else int(request.helpful)),
            ).fetchone()
        if existing:
            return self._record(existing)
        record = FeedbackRecord(
            feedback_id=uuid.uuid4().hex,
            trace_id=request.trace_id,
            created_at=datetime.now(timezone.utc),
            helpful=request.helpful,
            category=request.category,
            user_comment=request.user_comment,
            triage_status="new",
            review_status="new",
            reviewer_note=None,
        )
        with self._connect() as connection:
            connection.execute(
                """INSERT INTO feedback
                (feedback_id, trace_id, created_at, helpful, category, user_comment,
                 triage_status, review_status, reviewer_note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    record.feedback_id,
                    record.trace_id,
                    record.created_at.isoformat(),
                    None if record.helpful is None else int(record.helpful),
                    record.category,
                    record.user_comment,
                    record.triage_status,
                    record.review_status,
                    record.reviewer_note,
                ),
            )
        return record

    def get(self, feedback_id: str) -> FeedbackRecord | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM feedback WHERE feedback_id = ?", (feedback_id,)
            ).fetchone()
        return self._record(row) if row else None

    def list(self, status: TriageStatus | None = None) -> list[FeedbackRecord]:
        with self._connect() as connection:
            if status is None:
                rows = connection.execute(
                    "SELECT * FROM feedback ORDER BY created_at DESC, feedback_id DESC"
                ).fetchall()
            else:
                rows = connection.execute(
                    "SELECT * FROM feedback WHERE triage_status = ? ORDER BY created_at DESC, feedback_id DESC",
                    (status,),
                ).fetchall()
        return [self._record(row) for row in rows]

    def triage(
        self, feedback_id: str, status: TriageStatus, reviewer_note: str | None
    ) -> FeedbackRecord:
        current = self.get(feedback_id)
        if current is None:
            raise ValueError("feedback_not_found")
        if status not in ALLOWED_TRANSITIONS[current.triage_status]:
            raise ValueError("invalid_triage_transition")
        note = reviewer_note.strip() if reviewer_note else None
        with self._connect() as connection:
            connection.execute(
                """UPDATE feedback
                SET triage_status = ?, review_status = ?, reviewer_note = ?
                WHERE feedback_id = ?""",
                (status, TRIAGE_TO_REVIEW[status], note, feedback_id),
            )
        return self.get(feedback_id)

    def review(
        self, feedback_id: str, status: ReviewStatus, reviewer_note: str | None
    ) -> FeedbackRecord:
        if status not in REVIEW_STATUSES:
            raise ValueError("invalid_review_status")
        if self.get(feedback_id) is None:
            raise ValueError("feedback_not_found")
        note = reviewer_note.strip() if reviewer_note else None
        with self._connect() as connection:
            connection.execute(
                "UPDATE feedback SET review_status = ?, reviewer_note = ? WHERE feedback_id = ?",
                (status, note, feedback_id),
            )
        return self.get(feedback_id)
