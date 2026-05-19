from __future__ import annotations

from datetime import UTC, datetime

from app.models import Alert, TriageDecision

SEVERITY_WEIGHT = {
    "low": 10,
    "medium": 30,
    "high": 60,
    "critical": 90,
}

ENVIRONMENT_WEIGHT = {
    "dev": 0,
    "staging": 10,
    "prod": 20,
}


def score_alert(alert: Alert, *, now: datetime | None = None) -> int:
    current_time = now or datetime.now(UTC)
    age_hours = max((current_time - alert.created_at).total_seconds() / 3600, 0)
    age_weight = min(int(age_hours // 12) * 5, 25)
    security_weight = 15 if "security" in alert.tags else 0

    return min(
        SEVERITY_WEIGHT[alert.severity]
        + ENVIRONMENT_WEIGHT[alert.environment]
        + age_weight
        + security_weight,
        100,
    )


def choose_lane(alert: Alert, priority_score: int) -> str:
    if alert.severity == "critical" or priority_score >= 90:
        return "incident-command"
    if "dependency" in alert.tags or "security" in alert.tags:
        return "platform-risk"
    if priority_score >= 60:
        return "expedite"
    return "standard-queue"


def triage_alert(alert: Alert, *, now: datetime | None = None) -> TriageDecision:
    priority_score = score_alert(alert, now=now)
    lane = choose_lane(alert, priority_score)
    rationale = (
        f"{alert.severity} severity in {alert.environment} environment routed to {lane}"
    )
    return TriageDecision(
        alert_id=alert.id,
        priority_score=priority_score,
        lane=lane,
        rationale=rationale,
    )


def summarize_backlog(alerts: list[Alert], *, now: datetime | None = None) -> dict[str, int]:
    summary = {"incident-command": 0, "platform-risk": 0, "expedite": 0, "standard-queue": 0}
    for alert in alerts:
        decision = triage_alert(alert, now=now)
        summary[decision.lane] += 1
    return summary
