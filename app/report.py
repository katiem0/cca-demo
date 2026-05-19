from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from dateutil.parser import isoparse

from app.alert_triage import summarize_backlog, triage_alert
from app.models import Alert

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "sample_alerts.json"


def load_alerts(path: Path = DATA_FILE) -> list[Alert]:
    records = json.loads(path.read_text())
    return [
        Alert(
            id=record["id"],
            title=record["title"],
            severity=record["severity"],
            environment=record["environment"],
            created_at=isoparse(record["created_at"]),
            updated_at=isoparse(record["updated_at"]),
            tags=tuple(record.get("tags", [])),
        )
        for record in records
    ]


def main() -> None:
    alerts = load_alerts()
    now = datetime.fromisoformat("2026-05-17T15:00:00+00:00")
    for alert in alerts:
        decision = triage_alert(alert, now=now)
        print(f"{alert.id}: {decision.lane} ({decision.priority_score}) - {alert.title}")
    print(json.dumps(summarize_backlog(alerts, now=now), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
