"""Challenge provider module."""
import logging
import requests
import pandas as pd
from xml.etree import ElementTree
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
        base_events_data = []

        # Collect base event information
        for base_event in root.findall("output/base_event"):
            base_event_id = base_event.get("base_event_id", "")
            title = base_event.get("title", "")
            sell_mode = base_event.get("sell_mode", "") == self.SELL_MODE_TRUE

            # Collect event-level information
            for event in base_event.findall("event"):
                event_start_date = event.get("event_start_date", "")
                event_end_date = event.get("event_end_date", "")

                # Collect zone-level information (prices)
                zones = [
                    float(zone.get("price", 0.0)) for zone in event.findall("zone")
                ]

                base_events_data.append({
                    "base_event_id": base_event_id,
                    "title": title,
                    "sell_mode": sell_mode,
                    "event_start_date": event_start_date,
                    "event_end_date": event_end_date,
                    "min_price": min(zones) if zones else 0.0,
                    "max_price": max(zones) if zones else 0.0
                })

        # Convert to DataFrame for easier processing
        df = pd.DataFrame(base_events_data)

        # Create events based on parsed data
        for _, row in df.iterrows():
            logging.info(
                "Processing event with title: %s and base id: %s", row["title"], row["base_event_id"]
            )
            try:
                event_instance = Event.create(
                    base_id=EventBaseIdVo(row["base_event_id"]),
                    title=EventTitleVo(row["title"]),
                    date_range=DateRangeVo(
                        start_datetime=row["event_start_date"],
                        end_datetime=row["event_end_date"],
                    ),
                    min_price=row["min_price"],
                    max_price=row["max_price"],
                    sell_mode=row["sell_mode"],
                )
                events.append(event_instance)
            except (ValueError, TypeError) as e:
                logging.warning("Event instance could not be parsed due to %s.", e)
                continue

        return events
