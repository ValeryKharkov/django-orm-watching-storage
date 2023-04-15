from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone


def storage_information_view(request):
    # Программируем здесь

    # non_closed_visits = [
    #     {
    #         'who_entered': 'Richard Shaw',
    #         'entered_at': '11-04-2018 25:34',
    #         'duration': '25:03',
    #     }
    # ]
    not_leaved_visit = Visit.objects.filter(leaved_at=None)


    def who_entered(visit_object):
        """
        Определение сотрудника, который не покинул хранилище
        :param visit_object: визит сотрудника
        :return: имя сотрудника
        """
        for visit in visit_object:
            return visit.passcard

    def entered_at(visit_object):
        """
        Определение времени входа в хранилище
        :param visit_object: визит сотрудника
        :return: время
        """
        for visit in visit_object:
            return visit.entered_at

    def duration(visit_object):
        """
        Определение времени нахождения в хранилище
        :param duration: визит сотрудника
        :return: время с момента входа
        """
        for visit in visit_object:  # Определение визита сотрудника, при котором сотрудник находится в хранилище
            now = timezone.now()
            mos_time = timezone.localtime(visit.entered_at)
            delta = now - mos_time
            return delta

    def format_duration(time_object):
        """
        Формат времен под читабельный вид
        :param time_object: исходный объект времени
        :return: модифицированный объект времени
        """
        total_second = time_object.total_seconds()
        hour = int(total_second // 3600)
        minute = int((total_second - hour * 3600) // 60)
        second = int(total_second - hour * 3600 - minute * 60)

        result = f'{hour}ч {minute}мин {second}сек'

        return result

    non_closed_visits = [
        {
            'who_entered': who_entered(not_leaved_visit),
            'entered_at': entered_at(not_leaved_visit),
            'duration': format_duration(duration(not_leaved_visit)),
        }
    ]

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
