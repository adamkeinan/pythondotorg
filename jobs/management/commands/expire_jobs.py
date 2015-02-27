import datetime

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.utils import timezone

from jobs.models import Job


class Command(NoArgsCommand):
    """ Expire jobs older than settings.JOB_THRESHOLD_DAYS """

    def handle_noargs(self, **options):
        days = getattr(settings, 'JOB_THRESHOLD_DAYS', 90)
        expiration = timezone.now() - datetime.timedelta(days=days)

        Job.objects.filter(
            status=Job.STATUS_APPROVED,
            expires__lte=expiration,
        ).update(
            status=Job.STATUS_EXPIRED
        )

