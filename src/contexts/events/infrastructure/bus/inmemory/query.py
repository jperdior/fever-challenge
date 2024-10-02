"""In memory query bus implementation"""

import logging
from typing import Any, Dict

from src.shared.infrastructure.bus.query import QueryBus, Handler


class QueryBusImpl(QueryBus):
    """In memory query bus implementation"""

    def __init__(self):
        self.handlers: Dict[str, Handler] = {}

    def ask(self, query: Any) -> Any:
        """Ask a query"""
        query_type = query.type()
        handler = self.handlers.get(query_type)
        if not handler:
            return None
        print("Asking a query")
        try:
            answer = handler.handle(query)
        except Exception as e:
            logging.error("Error while handling %s - %s", query_type, e)
            raise e
        return answer

    def register(self, query_type: str, handler: Handler) -> None:
        """Register a query handler"""
        self.handlers[query_type] = handler
