from django.db import models
# from django.contrib.postgres.fields import JSONField
from django.db.models import JSONField

# Account model from Database


class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=350, blank=False)
    email = models.EmailField()
    password = models.CharField(max_length=350, blank=False)
    first_name = models.CharField(max_length=350, blank=False)
    last_name = models.CharField(max_length=350, blank=False)

    class Meta:
        db_table = "accounts"

    def __str__(self):
        return self.first_name + ' ' + self.last_name

# Budget model from Database


class Budget(models.Model):
    budget_id = models.AutoField(primary_key=True)
    year = models.DateField()
    type = models.CharField(max_length=350)
    budgets = JSONField()

    class Meta:
        db_table = "budgets"

    def __int__(self):
        return self.budget_id


class account_budget(models.Model):
    class Meta:
        db_table = "account_budget"

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
