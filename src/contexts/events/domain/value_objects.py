"""Domain value objects for events context."""


class EventBaseIdVo:
    """Value object for event base id."""

    def __init__(self, value: str | int):
        self.value: int = int(value)
        self.guard_value()

    def guard_value(self) -> None:
        """Guard method to check the value."""
        if not isinstance(self.value, int):
            raise ValueError("Event id must be an integer.")


class EventTitleVo:
    """Value object for event title."""

    def __init__(self, value: str):
        self.value: str = value
        self.guard_value()

    def guard_value(self) -> None:
        """Guard method to check the value."""
        if not isinstance(self.value, str):
            raise ValueError("Event title must be a string.")
