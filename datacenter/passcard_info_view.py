from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone
from datacenter.modules import get_duration
from datacenter.modules import convert_to_moscow_time
from datacenter.modules import format_duration
from datacenter.modules import is_visit_long
from django.shortcuts import get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode, is_active=True)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    for visit in visits:
        if not visit.leaved_at:
            leaved_at_moscow_time = convert_to_moscow_time(timezone.localtime())
        else:
            leaved_at_moscow_time = convert_to_moscow_time(visit.leaved_at)
        entered_at_moscow_time = convert_to_moscow_time(visit.entered_at)
        total_duration = get_duration(entered_at_moscow_time, leaved_at_moscow_time)
        duration = format_duration(total_duration)
        is_strange = is_visit_long(total_duration)
        passcard_visits = [
            {
                'entered_at': visit.entered_at,
                'duration': duration,
                'is_strange': is_strange
            },
        ]
        this_passcard_visits.extend(passcard_visits)
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
