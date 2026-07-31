"""
scanner_events.py

Scanner event dispatcher.

Author: Andrew Kyalo
Project: Andy Scanner
"""


class ScannerEvents:
    """
    Manages scanner events.
    """

    def __init__(self):

        self._listeners = {}

    # ==================================================
    # Register Listener
    # ==================================================

    def register(
        self,
        event,
        callback,
    ):

        self._listeners.setdefault(
            event,
            [],
        ).append(callback)

    # ==================================================
    # Remove Listener
    # ==================================================

    def unregister(
        self,
        event,
        callback,
    ):

        if event not in self._listeners:
            return

        if callback in self._listeners[event]:

            self._listeners[event].remove(
                callback
            )

    # ==================================================
    # Dispatch Event
    # ==================================================

    def dispatch(
        self,
        event,
        *args,
        **kwargs,
    ):

        listeners = self._listeners.get(
            event,
            [],
        )

        for callback in listeners:

            callback(
                *args,
                **kwargs,
            )

    # ==================================================
    # Utilities
    # ==================================================

    def clear(self):

        self._listeners.clear()

    def count(self):

        return len(self._listeners)

    def events(self):

        return sorted(self._listeners.keys())