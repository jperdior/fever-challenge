from abc import ABC, abstractmethod

from flask import Response


class ControllerInterface(ABC):
    """Controller interface"""

    @abstractmethod
    def execute(self,) -> Response:
        pass