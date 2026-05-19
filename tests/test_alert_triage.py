from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.alert_triage import score_alert, summarize_backlog, triage_alert
from app.models import Alert

NOW = datetime(2026, 5, 17, 15, 0, tzinfo=UTC)


def make_alert(**overrides: object) -> Alert:
    values = {
        "id": "CCA-999",
        "title": "Demo alert",
        "severity": "medium",
        "environment": "staging",
        "created_at": NOW - timedelta(hours=6),
        "updated_at": NOW - timedelta(hours=1),
        "tags": (),
    }
    values.update(overrides)
    return Alert(**values)  # type: ignore[arg-type]


def test_score_alert_weights_severity_environment_age_and_security_tag() -> None:
    alert = make_alert(
        severity="high",
        environment="prod",
        created_at=NOW - timedelta(hours=30),
        tags=("security",),
    )

    assert score_alert(alert, now=NOW) == 100


def test_critical_alert_routes_to_incident_command() -> None:
    alert = make_alert(severity="critical", environment="dev")

    decision = triage_alert(alert, now=NOW)

    assert decision.lane == "incident-command"
    assert decision.priority_score == 90


def test_dependency_alert_routes_to_platform_risk() -> None:
    alert = make_alert(severity="medium", environment="prod", tags=("dependency",))

    decision = triage_alert(alert, now=NOW)

    assert decision.lane == "platform-risk"


def test_summarize_backlog_counts_each_lane() -> None:
    alerts = [
        make_alert(id="1", severity="critical"),
        make_alert(id="2", severity="medium", tags=("dependency",)),
        make_alert(id="3", severity="high"),
        make_alert(id="4", severity="low"),
    ]

    assert summarize_backlog(alerts, now=NOW) == {
        "incident-command": 1,
        "platform-risk": 1,
        "expedite": 1,
        "standard-queue": 1,
    }
