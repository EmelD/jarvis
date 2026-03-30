class AppState:
    _has_started: bool = False

    @property
    def has_started(self) -> bool:
        return self._has_started

    @has_started.setter
    def has_started(self, value: bool) -> None:
        self._has_started = value


app_state = AppState()


def has_started() -> bool:
    return app_state.has_started


def starting() -> None:
    app_state.has_started = False


def started() -> None:
    app_state.has_started = True


def stopping() -> None:
    app_state.has_started = False


def stopped() -> None:
    app_state.has_started = False
