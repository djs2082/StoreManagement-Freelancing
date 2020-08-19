from django.db import models

class SizeModel(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'

    def __str__(self):
        return self.name