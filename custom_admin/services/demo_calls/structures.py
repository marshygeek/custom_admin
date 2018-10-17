from sys import maxsize
from timeit import default_timer


class CachedObject:
    def __init__(self, value=None) -> None:
        self._value = value

        if value:
            self._last_update = default_timer()
        else:
            self._last_update = -maxsize

    def update_value(self, value) -> None:
        self.__init__(value)

    def get_value(self):
        return self._value

    def get_downtime(self) -> float:
        return default_timer() - self._last_update
