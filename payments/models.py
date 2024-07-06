from django.db import models
from base.models import CustomUser

class UserPayment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)

    def __str__(self):
        return self.user.email