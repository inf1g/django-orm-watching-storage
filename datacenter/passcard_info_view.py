from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from django.http import Http404
from moduls import get_duration
from moduls import convert_to_moscow_time
from moduls import format_duration
from moduls import is_visit_long


def passcard_info_view(request, passcode):
    try:
        passcard = Passcard.objects.get(passcode=passcode, is_active=True)
        visits = Visit.objects.filter(passcard=passcard)
        this_passcard_visits = []
        for visit in visits:
            entered_at_moscow_time = convert_to_moscow_time(visit.entered_at)
            if not visit.leaved_at:
                leaved_at_moscow_time = convert_to_moscow_time(timezone.localtime())
            else:
                leaved_at_moscow_time = convert_to_moscow_time(visit.leaved_at)
            total_duration = get_duration(entered_at_moscow_time, leaved_at_moscow_time)
            duration = format_duration(total_duration)
            if is_visit_long(total_duration):
                is_strange = True
            else:
                is_strange = False
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
    except ObjectDoesNotExist:
        raise Http404("Пропуск с таким кодом не найден")
    except MultipleObjectsReturned:
        raise Http404("Найдено несколько пропусков с таким кодом")
