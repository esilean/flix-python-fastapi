from app.domains.events.handler import event_handler

class EventDispatcher:
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, func):
        async def wrapper(*args, **kwargs):
            try:
                res = await func(*args, **kwargs)
            except Exception as e:
                raise e from None
            
            await event_handler.publish()

            return res
        
        return wrapper