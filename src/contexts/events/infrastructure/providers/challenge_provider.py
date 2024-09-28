"""Challenge provider module."""

from xml.etree import ElementTree
import logging
import requests
from src.contexts.events.domain.provider import EventProvider
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

    def fetch_events(self) -> list[Event]:
        response = requests.get(self.PROVIDER_URL)
        if response.status_code == 200:
            events_data = response.text
            return self.parse_events(events_data)
        return []

    def parse_events(self, data: str) -> list[Event]:
        events = []
        root = ElementTree.fromstring(data)

        for base_event in root.findall("output/base_event"):
            base_event_id = base_event.get("base_event_id", "")
            title = base_event.get("title", "")
            sell_mode_string = base_event.get("sell_mode", "")
            sell_mode = sell_mode_string == self.SELL_MODE_TRUE
            logging.info("Processing event with title: %s and base id: %s", title, base_event_id)
            for event in base_event.findall("event"):
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

                try:
                    event_instance = Event(
                        base_id=EventBaseIdVo(base_event_id),
                        title=EventTitleVo(title),
                        date_range=DateRangeVo(
                            start_datetime=event_start_date,
                            end_datetime=event_end_date,
                        ),
                        min_price=min_price,
                        max_price=max_price,
                        sell_mode=sell_mode,
                    )
                except (ValueError, TypeError) as e:
                    logging.warning("Event instance could not be parsed due to %s.",e)
                    continue

                events.append(event_instance)
        return events
