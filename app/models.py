from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

Severity = Literal["low", "medium", "high", "critical"]
Environment = Literal["dev", "staging", "prod"]


@dataclass(frozen=True)
class Alert:
    id: str
    title: str
    severity: Severity
    environment: Environment
    created_at: datetime
    updated_at: datetime
    tags: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class TriageDecision:
    alert_id: str
    priority_score: int
    lane: str
    rationale: str
