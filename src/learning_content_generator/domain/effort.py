"""Person-hour calculations.

Person-Hours = Elapsed Hours x Number of Participants.
When participants worked different durations, the actual total is the sum
of each participant's individual hours.
"""

from __future__ import annotations

from collections.abc import Iterable

from learning_content_generator.domain.models import Participant


def person_hours(elapsed_hours: float, participant_count: int) -> float:
    """Planned person-hours for participants working the same duration."""
    if elapsed_hours < 0:
        raise ValueError("elapsed_hours must be >= 0")
    if participant_count < 1:
        raise ValueError("participant_count must be >= 1")
    return elapsed_hours * participant_count


def total_person_hours(participants: Iterable[Participant]) -> float:
    """Actual person-hours: sum of each participant's individual hours."""
    return sum(p.hours for p in participants)


def variance_hours(actual: float, estimated: float) -> float:
    """Variance Hours = Actual Person-Hours - Estimated Person-Hours."""
    return actual - estimated


def variance_rate(actual: float, estimated: float) -> float | None:
    """Variance rate in percent; None when the estimate is not positive."""
    if estimated <= 0:
        return None
    return (actual - estimated) / estimated * 100
