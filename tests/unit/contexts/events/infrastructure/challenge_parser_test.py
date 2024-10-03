import pytest
from datetime import datetime
from src.contexts.events.infrastructure.providers.challenge_provider import (
    ChallengeEventParser,
)
from src.contexts.events.domain.event import Event
from xml.etree import ElementTree


class TestChallengeEventParser:
    class TestChallengeEventParser:

        @pytest.fixture
        def valid_xml(self):
            return """
            <base_event base_event_id="291" sell_mode="online" title="Camela en concierto">
                <event event_start_date="2021-06-30T21:00:00" event_end_date="2021-06-30T21:30:00" event_id="291" sell_from="2020-07-01T00:00:00" sell_to="2021-06-30T20:00:00" sold_out="false">
                    <zone zone_id="40" capacity="200" price="20.00" name="Platea" numbered="true"/>
                    <zone zone_id="38" capacity="0" price="15.00" name="Grada 2" numbered="false"/>
                    <zone zone_id="30" capacity="80" price="30.00" name="A28" numbered="true"/>
                </event>
            </base_event>
            """

        @pytest.fixture
        def invalid_xml(self):
            return "<base_event>"

        @pytest.fixture
        def parser(self):
            return ChallengeEventParser()

        def test_parse_valid_xml(self, parser, valid_xml):
            event = parser.parse(valid_xml)
            assert event is not None
            assert isinstance(event, Event)
            assert event.base_id == 291
            assert event.title == "Camela en concierto"
            assert event.start_datetime == datetime.strptime(
                "2021-06-30T21:00:00", "%Y-%m-%dT%H:%M:%S"
            )
            assert event.end_datetime == datetime.strptime(
                "2021-06-30T21:30:00", "%Y-%m-%dT%H:%M:%S"
            )
            assert event.min_price == 15.00
            assert event.max_price == 30.00
            assert event.sell_mode is True

        def test_parse_invalid_xml(self, parser, invalid_xml):
            event = parser.parse(invalid_xml)
            assert event is None

        def test_parse_no_base_event(self, parser):
            xml = "<root></root>"
            event = parser.parse(xml)
            assert event is None

        def test_parse_no_event(self, parser):
            xml = """
            <base_event base_event_id="291" sell_mode="online" title="Camela en concierto">
            </base_event>
            """
            event = parser.parse(xml)
            assert event is None

        def test_parse_no_zones(self, parser):
            xml = """
            <base_event base_event_id="291" sell_mode="online" title="Camela en concierto">
                <event event_start_date="2021-06-30T21:00:00" event_end_date="2021-06-30T21:30:00" event_id="291" sell_from="2020-07-01T00:00:00" sell_to="2021-06-30T20:00:00" sold_out="false">
                </event>
            </base_event>
            """
            event = parser.parse(xml)
            assert event is not None
            assert event.min_price == 0.0
            assert event.max_price == 0.0
