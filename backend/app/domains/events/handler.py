import anyio

from typing import Type

from app.domains.events.event import BaseEvent
from app.domains.events.movies.movie import MovieCreated

class EventHandlerValidator:
    async def validate(self, event: BaseEvent):
        print(f'Event Type: {type(event)}')

class EventHandler:
    def __init__(self):
        self.validator = EventHandlerValidator()
        self.events: list[BaseEvent] = []

    async def store(self, event: BaseEvent):
        await self.validator.validate(event=event)
        self.events.append(event)

    async def publish(self):
        event: BaseEvent
        async with anyio.create_task_group() as task_group:
            for event in self.events:
                #task_group.start(event.handle, param)
                print(f'Publishing event: {event}')
        self.events.clear()

event_handler: Type[EventHandler] = EventHandler()