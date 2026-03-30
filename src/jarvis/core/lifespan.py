class AppState:
    _has_started: bool = False

    @property
    def has_started(self) -> bool:
        """Get the application started state."""
        return self._has_started

    @has_started.setter
    def has_started(self, value: bool) -> None:
        """Set the application started state."""
        self._has_started = value


# Single instance for application state
app_state = AppState()


def has_started() -> bool:
    """Check if the application has started."""
    return app_state.has_started


def starting() -> None:
    """Mark the application as starting."""
    app_state.has_started = False


def started() -> None:
    """Mark the application as started."""
    app_state.has_started = True


def stopping() -> None:
    """Mark the application as stopping."""
    app_state.has_started = False


def stopped() -> None:
    """Mark the application as stopped."""
    app_state.has_started = False
