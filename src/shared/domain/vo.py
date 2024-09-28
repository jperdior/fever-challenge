"""Value objects for the domain."""

from datetime import datetime

class DateRangeVo:
    """Value Object for date ranges."""

    def __init__(self, start_datetime: str, end_datetime: str) -> None:
        self.start_datetime = self.parse_datetime(start_datetime)
        self.end_datetime = self.parse_datetime(end_datetime)
        self.guard_values()

    @staticmethod
    def parse_datetime(datetime_str: str) -> datetime:
        """Parse a string to a datetime object."""
        formats = [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
            "%a, %d %b %Y %H:%M:%S %Z",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(datetime_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Invalid datetime format: {datetime_str}")


    def guard_values(self) -> None:
        """Guard method to check the values."""
        if self.start_datetime > self.end_datetime:
            raise ValueError("Start datetime must be before end datetime.")

    @property
    def start_date(self) -> str:
        """Get the start date."""
        return self.start_datetime.date().isoformat()

    @property
    def end_date(self) -> str:
        """Get the end date."""
        return self.end_datetime.date().isoformat()

    @property
    def start_time(self) -> str:
        """Get the start time."""
        return self.start_datetime.time().isoformat()

    @property
    def end_time(self) -> str:
        """Get the end time."""
        return self.end_datetime.time().isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "start_date": self.start_date,
            "start_time": self.start_time,
            "end_date": self.end_date,
            "end_time": self.end_time,
        }
