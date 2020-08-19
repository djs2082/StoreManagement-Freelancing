from django.db import models

class PaymentModel(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Payment Method'
        verbose_name_plural = 'Payment Methods'

    def __str__(self):
        return self.name
