from rest_framework import serializers

from app.finance.models import Account, Tag, Transaction, Limit


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TagInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color')


class TransactionListSerializer(serializers.HyperlinkedModelSerializer):
    tag = TagInlineSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'tag', 'amount', 'description', 'created_at')


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'


class LimitListSerializer(serializers.HyperlinkedModelSerializer):
    tag = TagInlineSerializer(read_only=True)

    class Meta:
        model = Limit
        fields = ('id', 'tag', 'amount', 'created_at', 'start_date', 'end_date')


class LimitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Limit
        fields = '__all__'
