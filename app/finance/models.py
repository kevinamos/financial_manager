import datetime

from django.db import models
from django.utils import timezone

from app.core.helpers import random_color
from app.core.models import AbstractBase


class Account(AbstractBase):
    balance = models.DecimalField(
        blank=True,
        default=0,
        decimal_places=2,
        max_digits=100
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        app_label = 'finance'

    def __str__(self):
        return "%s - %s - %s" % (
            self.created_by.full_name,
            self.name,
            self.balance
        )


class Tag(AbstractBase):
    name = models.CharField(max_length=255)
    description = models.TextField(
        null=True,
        blank=True,
    )
    color = models.CharField(
        max_length=7,
        null=True,
        blank=True,
        default=random_color
    )

    def clean(self):
        # All tag names should be in lower case
        self.name = self.name.lower()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.name = self.name.lower()

        super(Tag, self).save()

    class Meta:
        app_label = 'finance'
        unique_together = (
            'name',
            'created_by'
        )

    def __str__(self):
        return '%s - %s' % (self.created_by.email, self.name)


class Transaction(AbstractBase):
    """
    This is the most import table in this project.
    All other reports rely on this table as the absolute source of truth.
    All reports are generated from processing of data from this table.
    """
    amount = models.DecimalField(
        help_text='Negative amounts indicate expenses, positive indicate income',
        blank=True,
        default=0,
        decimal_places=2,
        max_digits=100
    )
    description = models.TextField()
    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    tag = models.ForeignKey(
        Tag,
        help_text='The associated tag, important for grouping similar '
                  'transactions for better reporting',
        on_delete=models.PROTECT,
        related_name='transactions'
    )
    transaction_date = models.DateTimeField(
        help_text='Transaction date and time could be set to be different '
                  'from the date and time of creation of record in the '
                  'database.',
        auto_now_add=True,
        null=False,
        blank=False
    )
    deleted = models.BooleanField(
        help_text='If this transaction will be factored in in reports',
        default=False,
        null=False,
        blank=False
    )

    class Meta:
        app_label = 'finance'
        ordering = ('-transaction_date',)

    def __str__(self):
        return '%s - %s - %s' % (
            self.account.name if self.account else 'General',
            self.tag.name,
            self.amount
        )


def get_start_of_month(date=None):
    if date is None:
        date = datetime.datetime.now()

    date = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return date


def get_end_of_month(date=None):
    if date is None:
        date = datetime.datetime.now()

    next_month = date.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


class Limit(AbstractBase):
    tag = models.ForeignKey(
        Tag,
        help_text='The tag whose limit is being added',
        on_delete=models.PROTECT,
        related_name='limits'
    )

    amount = models.DecimalField(
        help_text='The maximum amount allowed for this tag',
        blank=True,
        default=0,
        decimal_places=2,
        max_digits=100
    )

    start_date = models.DateTimeField(
        help_text='The day from which transactions under this tag will count'
                  'in the limit.',
        default=get_start_of_month,
        null=False,
        blank=True
    )

    end_date = models.DateTimeField(
        help_text='The end date for this limit.',
        default=get_end_of_month,
        null=False,
        blank=True
    )

    def __str__(self):
        return '%s - %s - %s - %s - %s' % (
            self.created_by.email,
            self.tag.name,
            self.start_date.date(),
            self.end_date.date(),
            self.amount
        )


class Budget(AbstractBase):
    tag = models.ForeignKey(
        Tag,
        help_text='The tag whose budget is being added',
        on_delete=models.PROTECT,
        related_name='budgets'
    )

    amount = models.DecimalField(
        blank=True,
        default=0,
        decimal_places=2,
        max_digits=100,
        help_text='The maximum amount allowed for the tag in this m',
    )

    overflow = models.BooleanField(
        blank=True,
        default=False,
        help_text='Whether the budget remains will overflow into the next cycle.'
    )