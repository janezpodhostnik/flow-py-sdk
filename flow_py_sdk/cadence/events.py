from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type

from flow_py_sdk.cadence.value import Value
from flow_py_sdk.cadence.address import Address
from flow_py_sdk.cadence.decode import add_cadence_decoder
from flow_py_sdk.cadence.composite import Composite, CompositeType

import flow_py_sdk.cadence.constants as c


class EventType(CompositeType):
    pass


class EventTypeRegistry(object):
    event_types: dict[str, Type[BaseEvent]] = {}

    @classmethod
    def register_event_type(cls, event_type: Type[BaseEvent]):
        EventTypeRegistry.event_types[event_type.event_id_constraint()] = event_type


class BaseEvent(Value, ABC):
    def __init__(self, fields: list[Value], event_type: EventType) -> None:
        super().__init__()
        self.event_type: EventType = event_type
        self.fields: list[Value] = fields

    def __str__(self):
        return Composite.format_composite(
            self.event_type.id(),
            self.event_type.fields,
            self.fields,
        )

    def encode_value(self) -> dict:
        return Composite.encode_composite(
            c.eventTypeStr,
            self.event_type.id(),
            self.event_type.fields,
            self.fields,
        )

    @classmethod
    def type_str(cls) -> str:
        return c.eventTypeStr

    @classmethod
    def decode(cls, value) -> BaseEvent:
        composite = Composite.decode(value[c.valueKey])

        event_type = EventType(
            composite.location,
            composite.qualified_identifier,
            composite.field_types,
        )

        if event_type.id() in EventTypeRegistry.event_types:
            event_class = EventTypeRegistry.event_types[event_type.id()]
        else:
            event_class = Event

        event = event_class(composite.field_values, event_type)

        return event

    @classmethod
    @abstractmethod
    def event_id_constraint(cls) -> str:
        pass


class Event(BaseEvent):
    @classmethod
    def event_id_constraint(cls) -> str:
        return ""


add_cadence_decoder(Event)


class AccountCreatedEvent(BaseEvent):
    def __init__(self, fields: list[Value], event_type: EventType) -> None:
        super().__init__(fields, event_type)
        self.address: Address = self.fields[0].as_type(Address)

    @classmethod
    def event_id_constraint(cls) -> str:
        return "flow.AccountCreated"


EventTypeRegistry.register_event_type(AccountCreatedEvent)
