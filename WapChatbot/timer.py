from datetime import *

def find_seconds_for_waiting():
    time = datetime.now()
    if time.hour >= 8:
        time_for_calculate = time + timedelta(days = 1)
        time_want = datetime(year = time_for_calculate.year, month = time_for_calculate.month, day = time_for_calculate.day, hour = 8)
    else:
        time_want = datetime(year = time.year, month = time.month, day = time.day, hour = 8)

    return (time_want - time).total_seconds()
