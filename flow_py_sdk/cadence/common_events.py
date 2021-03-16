from flow_py_sdk.cadence.address import Address
from flow_py_sdk.cadence.value import Value
from flow_py_sdk.cadence.types import EventType, Event


class AccountCreatedEvent(Event):
    def __init__(self, fields: list[Value], event_type: EventType) -> None:
        super().__init__(fields, event_type)
        self.address: Address = fields[0]

    @classmethod
    def from_event(cls, event: "Event") -> "Event":
        return AccountCreatedEvent(event.fields, event.event_type)

    @classmethod
    def event_id_constraint(cls) -> str:
        return "flow.AccountCreated"


Event.add_event_type(AccountCreatedEvent)
