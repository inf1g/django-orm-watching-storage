from datetime import datetime
from django.utils import timezone


def convert_to_moscow_time(time):
    moscow_tz = timezone.pytz.timezone('Europe/Moscow')
    moscow_time = time.astimezone(moscow_tz).replace(microsecond=0)
    return moscow_time


def get_duration(entered_at, leaved_at):
    return leaved_at - entered_at


def format_duration(time):
    time = str(time)
    format_time = datetime.strptime(time, '%H:%M:%S')
    return f'{format_time:%H:%M:%S}'


def is_visit_long(time):
    suspicious_visit_in_seconds = 3600
    return int(time.total_seconds()) > suspicious_visit_in_seconds

