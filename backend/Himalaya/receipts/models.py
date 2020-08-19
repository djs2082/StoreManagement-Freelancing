from django.db import models
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator
import datetime
from customers.models import Customer
from payment.models import PaymentModel
from brands.models import BrandModel
# from gdstorage.storage import GoogleDriveStorage

# # Define Google Drive Storage
# gd_storage = GoogleDriveStorage()

class Receipts(models.Model):
	id=models.AutoField(primary_key=True)
	customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
	payment_method=models.ForeignKey(PaymentModel,on_delete=models.SET_NULL,null=True)
	total_discount=models.FloatField(null=True, blank=0.0, default=0.0)
	total_amount=models.FloatField(null=True, blank=0.0, default=0.0)
	amount_payable=models.FloatField(null=True, blank=0.0, default=0.0)
	receipt_pdf=models.FileField(null=True,blank=True)
	date_time=models.DateTimeField(default=datetime.datetime.now().replace(tzinfo=None),auto_now=False, auto_now_add=False,null=True,blank=False)
	def __str__(self):
		return str(self.id)+"-"+str(self.date_time)


class Sales(models.Model):
	receipt=models.ForeignKey(Receipts,on_delete=models.CASCADE,null=True)
	brand=models.ForeignKey(BrandModel,on_delete=models.SET_NULL,null=True)
	size=models.CharField(max_length=20,default="")
	quantity=models.IntegerField(null=True,default=1,blank=False)
	selling_price=models.FloatField(null=True, blank=0.0, default=0.0)
	def __str__(self):
		if self.brand is None or self.brand.item is None:
			return str(self.receipt.id)
		return self.brand.item.name
