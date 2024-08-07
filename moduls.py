from datetime import datetime
from django.utils import timezone


def convert_to_moscow_time(dt):
    moscow_tz = timezone.pytz.timezone('Europe/Moscow')
    moscow_time = dt.astimezone(moscow_tz).replace(microsecond=0)
    return moscow_time


def get_duration(entered_at, leaved_at):
    return leaved_at - entered_at


def format_duration(td):
    td = str(td)
    time = datetime.strptime(td, '%H:%M:%S')
    return f'{time:%H:%M:%S}'


def is_visit_long(time):
    if int(time.total_seconds()) > 3600:
        return True
