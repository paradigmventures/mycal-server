import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.calendar.models import Calendar


class Event(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    title = models.CharField(max_length=191)
    is_all_day = models.BooleanField(default=True)
    start_date = models.DateField(_("Start Date"), db_index=True, null=True, blank=True)
    start_datetime = models.DateTimeField(_("Start Datetime"), db_index=True, null=True, blank=True)
    end_date = models.DateField(_("End Date"), db_index=True, null=True, blank=True)
    end_datetime = models.DateTimeField(_("End Datetime"), db_index=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    # TODO add location field
    # TODO add tags field

    @property
    def calendars(self):
        # NOTE: stub field for query_param filtering
        return

    class Meta:
        ordering = ['start_date', 'start_datetime']

    def __str__(self):
        return self.title
