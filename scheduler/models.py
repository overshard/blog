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

    def __str__(self):
        return self.management_command

    def should_run(self):
        now = timezone.now()
        if self.last_run_at is None:
            return True
        return self.last_run_at + timezone.timedelta(seconds=self.run_interval) < now
