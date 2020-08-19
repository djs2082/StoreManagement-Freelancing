from django.db import models

class ItemModel(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.name
