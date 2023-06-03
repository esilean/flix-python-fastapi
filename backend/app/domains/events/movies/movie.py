from app.domains.events.event import BaseEvent

class MovieCreated(BaseEvent):
    id: str
    title: str