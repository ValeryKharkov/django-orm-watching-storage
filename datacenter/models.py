from django.db import models


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(arg_visit):
    """
    Расчёт длительности визита
    :param visit: визит
    :return: объект datetime.timedelta
    """

    return arg_visit.leaved_at - arg_visit.entered_at


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
