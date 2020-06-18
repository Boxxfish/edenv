"""
Event system for EDEnv.

@author Ben Giacalone
"""
import functools

COMPONENTS = []
HANDLERS = {}


# Decorator for event handlers
def handler(event_queue_name="main"):
    def wrapper(func):
        # If event queue name is not in HANDLERS, create a new dict
        if event_queue_name not in HANDLERS:
            HANDLERS[event_queue_name] = {}

        # If event name is not in HANDLERS[event_queue_name], create a new list
        event_name = func.__name__[len("handle_"):]
        if event_name not in HANDLERS[event_queue_name]:
            HANDLERS[event_queue_name][event_name] = []

        HANDLERS[event_queue_name][event_name].append(func)

    return wrapper


# Sends event to event queue
def send_event(event_queue_name, event_name, *args, **kwargs):
    # If no such handler is registered, quit early
    if event_queue_name not in HANDLERS or event_name not in HANDLERS[event_queue_name]:
        return

    # Broadcast the event
    handlers = HANDLERS[event_queue_name][event_name]
    for handler in handlers:
        for component in COMPONENTS:
            if type(component).__name__ == handler.__qualname__.split(".")[0]:
                handler(component, *args, **kwargs)


# Registers a component to the event system
def register_component(component):
    COMPONENTS.append(component)
