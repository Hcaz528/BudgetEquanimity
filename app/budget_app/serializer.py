from django.db.models import fields
from rest_framework import serializers
from budget_app.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('account_id', 'username', 'first_name', 'last_name')
