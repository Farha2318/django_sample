from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin_name = models.CharField(max_length=10)
    buy_price = models.FloatField()
    quantity = models.FloatField()
    purchase_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.coin_name}"
