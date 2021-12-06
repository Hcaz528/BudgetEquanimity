from django.db import models

# Create your models here.
# CREATE TABLE accounts (
#     account_id SERIAL,
#     username TEXT NOT NULL,
#     email TEXT NOT NULL,
#     password TEXT NOT NULL,
#     first_name TEXT,
#     last_name TEXT,
#     PRIMARY KEY (account_id)
# );


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

# DROP TABLE IF EXISTS budgets;
# CREATE TABLE budgets (
#     budget_id SERIAL,
#     year DATE NOT NULL,
#     type TEXT NOT NULL,
#     budgets JSONB,
#     PRIMARY KEY (budget_id)
# );

# DROP TABLE IF EXISTS account_budget;
# CREATE TABLE account_budget (
#     account_id INT NOT NULL,
#     budget_id INT NOT NULL,
#     PRIMARY KEY (account_id, budget_id)
# );
