import json
import os
from pathlib import Path

from .models import TurnTrace


class TurnTraceStore:
    def __init__(self, data_dir: Path):
        self.directory = data_dir.resolve() / "turn-traces"
        self.directory.mkdir(parents=True, exist_ok=True)

    def save(self, trace: TurnTrace) -> None:
        path = self.directory / f"{trace.trace_id}.json"
        temporary = path.with_suffix(".json.tmp")
        temporary.write_text(trace.model_dump_json(indent=2), encoding="utf-8")
        os.replace(temporary, path)

    def get(self, trace_id: str) -> TurnTrace | None:
        if not trace_id or any(character not in "0123456789abcdef" for character in trace_id):
            return None
        try:
            return TurnTrace.model_validate_json(
                (self.directory / f"{trace_id}.json").read_text(encoding="utf-8")
            )
        except (OSError, ValueError):
            return None
