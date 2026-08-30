import os  # deliberately unused import, for CI negative-path testing (issue #6)


def test_deliberately_broken() -> None:
    assert False, "intentional failure for CI negative-path testing (issue #6)"
