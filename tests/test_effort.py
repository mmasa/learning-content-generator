import pytest

from learning_content_generator.domain.effort import (
    person_hours,
    total_person_hours,
    variance_hours,
    variance_rate,
)
from learning_content_generator.domain.models import Participant


class TestPersonHours:
    def test_single_person_one_hour(self) -> None:
        assert person_hours(1.0, 1) == 1.0

    def test_two_people_thirty_minutes(self) -> None:
        assert person_hours(0.5, 2) == 1.0

    def test_three_people_twenty_minutes(self) -> None:
        assert person_hours(1 / 3, 3) == pytest.approx(1.0)

    def test_two_people_two_hours(self) -> None:
        assert person_hours(2.0, 2) == 4.0

    def test_rejects_negative_elapsed(self) -> None:
        with pytest.raises(ValueError):
            person_hours(-1.0, 1)

    def test_rejects_zero_participants(self) -> None:
        with pytest.raises(ValueError):
            person_hours(1.0, 0)


class TestTotalPersonHours:
    def test_sums_different_individual_hours(self) -> None:
        participants = [
            Participant(name="A", hours=1.0),
            Participant(name="B", hours=0.5),
            Participant(name="C", hours=0.25),
        ]
        assert total_person_hours(participants) == 1.75

    def test_empty_is_zero(self) -> None:
        assert total_person_hours([]) == 0.0


class TestVariance:
    def test_variance_hours(self) -> None:
        assert variance_hours(actual=5.0, estimated=4.0) == 1.0
        assert variance_hours(actual=3.0, estimated=4.0) == -1.0

    def test_variance_rate(self) -> None:
        assert variance_rate(actual=5.0, estimated=4.0) == pytest.approx(25.0)
        assert variance_rate(actual=3.0, estimated=4.0) == pytest.approx(-25.0)

    def test_variance_rate_undefined_for_zero_estimate(self) -> None:
        assert variance_rate(actual=5.0, estimated=0.0) is None
        assert variance_rate(actual=5.0, estimated=-1.0) is None
