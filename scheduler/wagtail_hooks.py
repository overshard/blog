from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import ScheduledTask


class ScheduledTaskAdmin(ModelAdmin):
    model = ScheduledTask
    menu_label = 'Scheduler'
    menu_icon = 'list-ul'
    exclude_from_explorer = True
    menu_order = 250
    list_display = ('management_command', 'run_interval', 'last_run_at',)
    list_filter = ('run_interval',)
    search_fields = ('management_command',)
    ordering = ('-run_interval',)


modeladmin_register(ScheduledTaskAdmin)
