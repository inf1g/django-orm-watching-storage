from django.shortcuts import render
from datacenter.models import Visit
from django.utils import timezone
from moduls import get_duration
from moduls import convert_to_moscow_time
from moduls import format_duration


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at=None)
    for visit in visits:
        entered_at = convert_to_moscow_time(visit.entered_at)
        now_time = convert_to_moscow_time(timezone.localtime())
        duration = get_duration(entered_at, now_time)
        duration = format_duration(duration)
        non_closed_visits = [
            {
                'who_entered': visit.passcard,
                'entered_at': entered_at,
                'duration': duration,
            }
        ]
        context = {
            'non_closed_visits': non_closed_visits,
        }
        return render(request, 'storage_information.html', context)
