"""Sleep backoff utility.

A helper that gradually increases sleep time when events repeat before a
threshold and resets when they are far enough apart.
"""

__version__ = "0.1.0"
__author__ = "fx-kirin <fx.kirin@gmail.com>"
__all__: list = []


import time
from dataclasses import dataclass


@dataclass
class BackoffSleeper:
    """Increase sleep time in steps and reset when repeats are too fast.

    Args:
        min_sleep_seconds: Minimum sleep duration in seconds.
        max_sleep_seconds: Maximum sleep duration in seconds.
        steps_to_max: Number of steps to reach max sleep.
        threshold_seconds: Increase sleep when elapsed time is less than this.
    """

    min_sleep_seconds: float
    max_sleep_seconds: float
    steps_to_max: int
    threshold_seconds: float

    def __post_init__(self) -> None:
        if self.min_sleep_seconds <= 0:
            raise ValueError("min_sleep_seconds must be positive")
        if self.max_sleep_seconds < self.min_sleep_seconds:
            raise ValueError("max_sleep_seconds must be >= min_sleep_seconds")
        if self.steps_to_max <= 0:
            raise ValueError("steps_to_max must be positive")
        if self.threshold_seconds <= 0:
            raise ValueError("threshold_seconds must be positive")
        self._step = 0
        self._last_sleep_at: float | None = None

    def sleep(self) -> float:
        """Sleep for the current duration and return it.

        If the time since the previous sleep is < threshold_seconds, the sleep
        duration increases by one step (up to max). Otherwise, the sleep
        duration resets to the minimum.
        """

        now = time.monotonic()

        if self._last_sleep_at is None:
            self._step = 0
        else:
            elapsed = now - self._last_sleep_at
            if elapsed < self.threshold_seconds:
                self._step = min(self._step + 1, self.steps_to_max)
            else:
                self._step = 0

        sleep_seconds = self._current_sleep_seconds()
        time.sleep(sleep_seconds)
        self._last_sleep_at = time.monotonic()
        return sleep_seconds

    def _current_sleep_seconds(self) -> float:
        if self.steps_to_max == 0:
            return self.min_sleep_seconds
        ratio = self._step / self.steps_to_max
        return self.min_sleep_seconds + (
            (self.max_sleep_seconds - self.min_sleep_seconds) * ratio
        )
