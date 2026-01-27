# backoff-sleeper

`backoff-sleeper` is a small utility that increases sleep time in steps when
repeated events are spaced beyond a configured threshold, and resets back to
the minimum sleep when events are too close together.

## Install

```bash
pip install backoff-sleeper
```

## Usage

```python
from backoff_sleeper import BackoffSleeper

sleeper = BackoffSleeper(
    min_sleep_seconds=0.5,
    max_sleep_seconds=5.0,
    steps_to_max=5,
    threshold_seconds=10.0,
)

# Call on each repeat; sleep time increases when elapsed >= threshold_seconds.
sleeper.sleep()
```

## Behavior

- The first call sleeps for `min_sleep_seconds`.
- If the time since the previous sleep is greater than or equal to
  `threshold_seconds`, the sleep duration increases by one step (up to
  `max_sleep_seconds`).
- If the time since the previous sleep is less than `threshold_seconds`, the
  sleep duration resets to `min_sleep_seconds`.
