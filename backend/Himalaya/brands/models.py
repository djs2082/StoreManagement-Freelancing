from django.db import models
from items.models import ItemModel
class BrandModel(models.Model):
    id=models.AutoField(primary_key=True)
    item=models.ForeignKey(ItemModel,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=50)
    initial_quantity=models.IntegerField(null=True)
    quantity=models.IntegerField(null=True)
    price=models.FloatField("Cost Price",null=False, blank=0.0, default=0.0)
    cost_price=models.FloatField("Selling Price",null=False, blank=0.0, default=0.0)
    initial_discount=models.FloatField(null=True, blank=0.0, default=0.0)
    gst=models.FloatField(null=True, blank=0.0, default=0.0)
    transport_charge=models.FloatField(null=True, blank=0.0, default=0.0)

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.item.name+" "+self.name+" "+str(self.quantity)


