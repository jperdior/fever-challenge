"""Domain errors"""


class DomainError(Exception):
    """Domain error class"""

    def __init__(self, message: str, key: str, code: str) -> None:
        self.message = message
        self.key = key
        self.code = code


class InvalidStartDateError(DomainError):
    """Invalid start date error"""

    def __init__(self, key: str) -> None:
        super().__init__("Invalid start date", key, "invalid_start_date")


class InvalidEndDateError(DomainError):
    """Invalid end date error"""

    def __init__(self, key: str) -> None:
        super().__init__("Invalid end date", key, "invalid_end_date")
