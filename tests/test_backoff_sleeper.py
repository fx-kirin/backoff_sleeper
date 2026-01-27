#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import logging
import os

import kanilog
import pytest
import stdlogging
from add_parent_path import add_parent_path


with add_parent_path():
    from backoff_sleeper import BackoffSleeper


def _set_monotonic(times):
    iterator = iter(times)

    def _monotonic():
        return next(iterator)

    return _monotonic


def test_backoff_increases_when_elapsed_meets_threshold(monkeypatch):
    sleeper = BackoffSleeper(
        min_sleep_seconds=1.0,
        max_sleep_seconds=3.0,
        steps_to_max=2,
        threshold_seconds=5.0,
    )

    slept = []
    monkeypatch.setattr("time.sleep", lambda seconds: slept.append(seconds))
    monkeypatch.setattr(
        "time.monotonic",
        _set_monotonic([0.0, 0.0, 6.0, 6.0, 12.0, 12.0]),
    )

    assert sleeper.sleep() == pytest.approx(1.0)
    assert sleeper.sleep() == pytest.approx(2.0)
    assert sleeper.sleep() == pytest.approx(3.0)
    assert slept == [1.0, 2.0, 3.0]


def test_backoff_resets_when_elapsed_below_threshold(monkeypatch):
    sleeper = BackoffSleeper(
        min_sleep_seconds=2.0,
        max_sleep_seconds=6.0,
        steps_to_max=2,
        threshold_seconds=4.0,
    )

    slept = []
    monkeypatch.setattr("time.sleep", lambda seconds: slept.append(seconds))
    monkeypatch.setattr(
        "time.monotonic",
        _set_monotonic([0.0, 0.0, 5.0, 5.0, 7.0, 7.0]),
    )

    assert sleeper.sleep() == pytest.approx(2.0)
    assert sleeper.sleep() == pytest.approx(4.0)
    assert sleeper.sleep() == pytest.approx(2.0)
    assert slept == [2.0, 4.0, 2.0]

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    kanilog.setup_logger(logfile='/tmp/%s.log' % (os.path.basename(__file__)), level=logging.INFO)
    stdlogging.enable()

    pytest.main([__file__, '-k test_', '-s'])
