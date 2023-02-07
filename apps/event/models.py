import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.calendar.models import Calendar


class Event(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    title = models.CharField(max_length=191)
    start_dt = models.DateTimeField(_("Start Datetime"), db_index=True)
    end_dt = models.DateTimeField(_("End Datetime"), db_index=True)
    description = models.TextField(null=True, blank=True)
    # TODO add location field
    # TODO add tags field

    class Meta:
        ordering = ['start_dt']

    def __str__(self):
        return self.title
