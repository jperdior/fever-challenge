"""Challenge provider module."""

from xml.etree import ElementTree
from typing import List
import logging
import requests
from src.contexts.events.domain.provider import EventParser, EventProvider
from src.contexts.events.domain.event import Event
from src.contexts.events.domain.value_objects import EventTitleVo, EventBaseIdVo
from src.shared.domain.vo import DateRangeVo


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class ChallengeProvider(EventProvider):
    """Challenge provider class."""

    PROVIDER_URL = "https://provider.code-challenge.feverup.com/api/events"
    SELL_MODE_TRUE = "online"

    def fetch_events(self) -> List[str]:
        try:
            response = requests.get(self.PROVIDER_URL, timeout=10)
            if response.status_code == 200:
                data = response.text
                try:
                    events_data: List[str] = []
                    root = ElementTree.fromstring(data)

                    for base_event in root.findall("output/base_event"):
                        event_bytes = ElementTree.tostring(base_event, encoding="utf-8")
                        event_string = event_bytes.decode("utf-8")
                        events_data.append(event_string)

                except ElementTree.ParseError as e:
                    logging.error("Could not parse data due to %s.", e)
                    return events_data
            return []
        except requests.RequestException as e:
            logging.error("Request failed: %s", e)
        return []


class ChallengeEventParser(EventParser):
    """Event parser class."""

    ONLINE_SELL_MODE = "online"

    def parse(self, data: str) -> Event | None:
        """Parse the fetched data into an Event instance."""
        try:
            root = ElementTree.fromstring(data)
            base_event = root.find("base_event")

            if base_event is None:
                logging.warning("No base_event found in the XML.")
                return None

            base_event_id = base_event.get("base_event_id", "")
            sell_mode = base_event.get("sell_mode", "")
            title = base_event.get("title", "")

            event = base_event.find("event")
            if event is None:
                logging.error("No event found in the base_event.")
                return None

            event_start_date = event.get("event_start_date", "")
            event_end_date = event.get("event_end_date", "")

            min_price = float("inf")
            max_price = float("-inf")

            for zone in event.findall("zone"):
                price_str = zone.get("price")
                if price_str is not None:
                    price = float(price_str)
                else:
                    price = 0.0
                min_price = min(min_price, price)
                max_price = max(max_price, price)

            event_instance = Event.create(
                base_id=EventBaseIdVo(base_event_id),
                title=EventTitleVo(title),
                date_range=DateRangeVo(
                    start_datetime=event_start_date,
                    end_datetime=event_end_date,
                ),
                min_price=min_price if min_price != float("inf") else 0.0,
                max_price=max_price if max_price != float("-inf") else 0.0,
                sell_mode=sell_mode == self.ONLINE_SELL_MODE,
            )

            return event_instance

        except (ElementTree.ParseError, ValueError, TypeError) as e:
            logging.warning("Event instance could not be parsed due to %s.", e)
            return None
