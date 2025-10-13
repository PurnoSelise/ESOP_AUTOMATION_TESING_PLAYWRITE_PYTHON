def assert_contains(actual: str, expected: str):
    assert expected in actual, f"Expected '{expected}' in '{actual}'"
