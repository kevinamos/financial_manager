import django_filters
from rest_framework import filters

from app.finance.models import Transaction


class TransactionFilter(filters.SearchFilter):
    created_at_gte = django_filters.DateTimeFilter(name="timestamp", lookup_expr='gte')

    class Meta:
        model = Transaction
        fields = ['tag', 'created_at_gte']