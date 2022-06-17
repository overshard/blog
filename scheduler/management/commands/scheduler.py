import time

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone

from ...models import ScheduledTask


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('[Scheduler] Starting scheduler...')

        while True:
            tasks = ScheduledTask.objects.all()

            for task in tasks:
                if task.should_run():
                    now = timezone.now()
                    timestamp = now.strftime('%d/%b/%Y %H:%M:%S %z')
                    self.stdout.write(f'[Scheduler] [{timestamp}] Running task {task.management_command}')
                    call_command(task.management_command)
                    task.last_run_at = now
                    task.next_run_at = task.get_next_run_at(now)
                    task.save()

            self.stdout.write('[Scheduler] Sleeping scheduler for 60 seconds...')

            try:
                time.sleep(60)
            except KeyboardInterrupt:
                self.stdout.write('[Scheduler] Stopping scheduler...')
                break
