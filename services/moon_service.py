# services/moon_service.py
import math
from datetime import datetime, timezone

def moon_phase_for_date(date):
    """Возвращает ключ фазы: 'new', 'waxing', 'full', 'waning'"""
    y = date.year
    m = date.month
    d = date.day

    if m < 3:
        y -= 1
        m += 12

    a = math.floor(y / 100)
    b = 2 - a + math.floor(a / 4)
    jd = math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d + b - 1524.5
    days_since_new = jd - 2451550.1
    lunations = days_since_new / 29.530588853
    phase_index = int((lunations % 1) * 8 + 0.5) % 8

    if phase_index == 0:
        return "new"
    elif phase_index in [1, 2, 3]:
        return "waxing"
    elif phase_index == 4:
        return "full"
    else:
        return "waning"

def get_current_moon_phase():
    today = datetime.now(timezone.utc).date()
    return moon_phase_for_date(today)