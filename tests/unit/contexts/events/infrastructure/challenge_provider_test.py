"""Test for ChallengeProvider class"""

import pytest
import requests
from unittest.mock import patch
from src.contexts.events.infrastructure.providers.challenge_provider import (
    ChallengeProvider,
)
from src.contexts.events.domain.event import Event


@pytest.fixture
def mock_response():
    xml_data = """
    <eventList xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0" xsi:noNamespaceSchemaLocation="eventList.xsd">
    <script/>
    <output>
    <base_event base_event_id="291" sell_mode="online" title="Camela en concierto">
    <event event_start_date="2021-06-30T21:00:00" event_end_date="2021-06-30T22:00:00" event_id="291" sell_from="2020-07-01T00:00:00" sell_to="2021-06-30T20:00:00" sold_out="false">
    <zone zone_id="40" capacity="243" price="20.00" name="Platea" numbered="true"/>
    <zone zone_id="38" capacity="100" price="15.00" name="Grada 2" numbered="false"/>
    <zone zone_id="30" capacity="90" price="30.00" name="A28" numbered="true"/>
    </event>
    </base_event>
    <base_event base_event_id="322" sell_mode="online" organizer_company_id="2" title="Pantomima Full">
    <event event_start_date="2021-02-10T20:00:00" event_end_date="2021-02-10T21:30:00" event_id="1642" sell_from="2021-01-01T00:00:00" sell_to="2021-02-09T19:50:00" sold_out="false">
    <zone zone_id="311" capacity="2" price="55.00" name="A42" numbered="true"/>
    </event>
    </base_event>
    <base_event base_event_id="1591" sell_mode="online" organizer_company_id="1" title="Los Morancos">
    <event event_start_date="2021-07-31T20:00:00" event_end_date="2021-07-31T21:00:00" event_id="1642" sell_from="2021-06-26T00:00:00" sell_to="2021-07-31T19:50:00" sold_out="false">
    <zone zone_id="186" capacity="2" price="75.00" name="Amfiteatre" numbered="true"/>
    <zone zone_id="186" capacity="16" price="65.00" name="Amfiteatre" numbered="false"/>
    </event>
    </base_event>
    </output>
    </eventList>
    """
    return xml_data


@pytest.fixture
def mock_invalid_date_response():
    xml_data = """
     <eventList xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0" xsi:noNamespaceSchemaLocation="eventList.xsd">
    <script/>
    <output>
    <base_event base_event_id="291" sell_mode="online" title="Camela en concierto">
    <event event_start_date="2021-06-31T21:00:00" event_end_date="2021-06-30T22:00:00" event_id="291" sell_from="2020-07-01T00:00:00" sell_to="2021-06-30T20:00:00" sold_out="false">
    <zone zone_id="40" capacity="243" price="20.00" name="Platea" numbered="true"/>
    <zone zone_id="38" capacity="100" price="15.00" name="Grada 2" numbered="false"/>
    <zone zone_id="30" capacity="90" price="30.00" name="A28" numbered="true"/>
    </event>
    </base_event>
    </output>
    </eventList>
    """
    return xml_data


@pytest.fixture
def invalid_xml_response():
    return "invalid xml"


@patch("requests.get")
def test_fetch_events(mock_get, mock_response):
    """Should return a list of events."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = mock_response

    provider = ChallengeProvider()
    events_data = provider.fetch_events()

    assert len(events_data) == 3
    assert isinstance(events_data[0], str)


@patch("requests.get")
def test_fetch_events_bad_response(mock_get, mock_invalid_date_response):
    """Should return an empty list of events."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = mock_invalid_date_response

    provider = ChallengeProvider()
    events = provider.fetch_events()

    assert len(events) == 0


@patch("requests.get")
def test_fetch_events_invalid_xml_response(mock_get, invalid_xml_response):
    """Should return an empty list of events."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = invalid_xml_response

    provider = ChallengeProvider()
    events = provider.fetch_events()

    assert len(events) == 0
