import math

from datetime import time
from typing import List


def time_to_seconds(time_: time) -> int:
    """Return total seconds from time object."""
    minutes = time_.hour * 60
    seconds = (time_.minute + minutes) * 60
    return seconds


def seconds_to_time(seconds: int) -> time:
    """Return time object from total seconds."""
    seconds_off = seconds % 60
    minutes = int(seconds / 60)
    minutes_off = minutes % 60
    hours = int(minutes / 60)
    return time(hours, minutes_off, seconds_off)


def calc_max_step_size(obj_list: List[time]) -> int:
    """Return largest possible step size in seconds to include every time from list."""
    unique_ordered_list = sorted(set(obj_list))
    diffs = []
    for i in range(len(unique_ordered_list)):
        if i == 0:
            continue
        diff = time_to_seconds(unique_ordered_list[i]) - time_to_seconds(unique_ordered_list[i-1])
        diffs.append(diff)
    return math.gcd(*diffs)
