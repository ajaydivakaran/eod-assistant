from datetime import datetime

import pytz


def formatted_date_in_local_timezone(datetime, local_timezone):
    return datetime.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(local_timezone))


def time_of_day(current_datetime, hour, minute):
    return datetime(year=current_datetime.year, month=current_datetime.month,
                    day=current_datetime.day, hour=hour, minute=minute)
