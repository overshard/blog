from django.db import models
from django.utils import timezone


class ScheduledTask(models.Model):
    RUN_INTERVAL_CHOICES = (
        (300, "Every 5 minutes"),
        (900, "Every 15 minutes"),
        (1800, "Every 30 minutes"),
        (3600, "Every hour"),
        (86400, "Every day"),
    )
    MANAGEMENT_COMMAND_CHOICES = (
        ("publish_scheduled_pages", "Publish scheduled pages (recommended every hour)"),
        ("clearsessions", "Clear sessions (recommended every day)"),
    )

    management_command = models.CharField(
        max_length=255, choices=MANAGEMENT_COMMAND_CHOICES, unique=True
    )
    run_interval = models.IntegerField(choices=RUN_INTERVAL_CHOICES)
    last_run_at = models.DateTimeField(blank=True, null=True)
    next_run_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.management_command

    def should_run(self):
        now = timezone.now()
        if self.last_run_at is None:
            return True
        if self.next_run_at is None:
            return True
        return self.next_run_at <= now

    def get_next_run_at(self, now):
        """
        Returns the next run datetime. Should be in whole increments of the run
        interval.

        Every 5 minutes should be rounded to the nearest 5 minutes.
        Every 15 minutes should be rounded to the nearest 15 minutes.
        Every 30 minutes should be rounded to the nearest 30 minutes.
        Every hour should be rounded to the nearest hour.
        Every day should be rounded to the nearest day.
        """

        if self.run_interval == 300:
            return now.replace(minute=(now.minute // 5) * 5, second=0, microsecond=0) + timezone.timedelta(minutes=5)
        elif self.run_interval == 900:
            return now.replace(minute=(now.minute // 15) * 15, second=0, microsecond=0) + timezone.timedelta(minutes=15)
        elif self.run_interval == 1800:
            return now.replace(minute=(now.minute // 30) * 30, second=0, microsecond=0) + timezone.timedelta(minutes=30)
        elif self.run_interval == 3600:
            return now.replace(minute=0, second=0, microsecond=0) + timezone.timedelta(hours=1)
        elif self.run_interval == 86400:
            return now.replace(hour=0, minute=0, second=0, microsecond=0) + timezone.timedelta(days=1)
        else:
            raise ValueError("Invalid run interval")
