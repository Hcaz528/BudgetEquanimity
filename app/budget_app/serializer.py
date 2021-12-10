from django.db.models import fields
from rest_framework import serializers
from budget_app.models import Account, Budget


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('account_id', 'username', 'first_name', 'last_name')


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ('budget_id', 'year', 'budgets')


class BudgetSerializer_mini(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ('year', 'budgets')
