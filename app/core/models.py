import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class AbstractBase(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def clean(self):
        if self.updated_by is None and self.created_by is not None:
            self.updated_by = self.created_by

    class Meta:
        abstract = True
