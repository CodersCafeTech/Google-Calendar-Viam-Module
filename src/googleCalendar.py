from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List
from typing_extensions import Self

from viam.resource.types import RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_SERVICE, Subtype
from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.services.generic import Generic
from viam.logging import getLogger

import time
import asyncio

from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

LOGGER = getLogger(__name__)

class googleCalendar(Generic, Reconfigurable):
    
    """
    A Viam Service To Interact With Google Calendar
    """


    MODEL: ClassVar[Model] = Model(ModelFamily("coderscafe", "calendar"), "google-calendar")
    
    SCOPES: Final = ["https://www.googleapis.com/auth/calendar"]
    calendar_id: str
    service_account_file: str

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        service = cls(config.name)
        service.reconfigure(config, dependencies)
        return service

    # Validate JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        if not config.attributes.fields.get("calendar_id"):
            raise Exception("A 'calendar_id' must be defined in the configuration.")
        if not config.attributes.fields.get("service_account_file"):
            raise Exception("A 'service_account_file' must be defined in the configuration.")

    # Reconfigure Service
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.calendar_id = config.attributes.fields["calendar_id"].string_value
        self.service_account_file = config.attributes.fields["service_account_file"].string_value

        self.credentials = service_account.Credentials.from_service_account_file(
            self.service_account_file, scopes=self.SCOPES
        )
        self.service = build("calendar", "v3", credentials=self.credentials)
        LOGGER.info(f"Google Calendar Service initialized for calendar ID: {self.calendar_id}")

    # Implement the `do_command` method
    async def do_command(
        self,
        command: Mapping[str, Any],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, Any]:
        if "get_events" in command:
            return {"events": self.get_events(command["get_events"].get("max_results", 10))}
        elif "add_event" in command:
            event_data = command["add_event"]
            return {"event_id": self.add_event(event_data)}
        elif "delete_event" in command:
            event_id = command["delete_event"].get("event_id")
            self.delete_event(event_id)
            return {"status": "Event deleted successfully."}
        else:
            raise Exception("Unknown command")

    # Fetch upcoming events
    def get_events(self, max_results: int = 10) -> List[Dict[str, Any]]:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = self.service.events().list(
            calendarId=self.calendar_id,
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        events = events_result.get("items", [])
        LOGGER.info(f"Fetched {len(events)} events.")
        return [{"summary": e.get("summary", "No Title"), "start": e["start"].get("dateTime", e["start"].get("date")), "end": e["end"].get("dateTime", e["end"].get("date"))} for e in events]

    # Add a new event
    def add_event(self, event_data: Dict[str, Any]) -> str:
        event = self.service.events().insert(calendarId=self.calendar_id, body=event_data).execute()
        LOGGER.info(f"Event created: {event.get('id')}")
        return event.get("id")

    # Delete an event
    def delete_event(self, event_id: str):
        self.service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()
        LOGGER.info(f"Event {event_id} deleted.")

    SUBTYPE: Final = Subtype(  # pyright: ignore [reportIncompatibleVariableOverride]
        RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_SERVICE, "generic"
    )
