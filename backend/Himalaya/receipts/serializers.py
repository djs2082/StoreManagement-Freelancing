from rest_framework import serializers
from .models import Receipts
from payment.models import PaymentModel
from payment.serializers import PaymentSerializer
from customers.serializers import CustomerSerializer

class ReceiptsSerializer(serializers.ModelSerializer):
	date_time=serializers.DateTimeField(format='%m/%d/%Y')
	payment_method=PaymentSerializer()
	customer=CustomerSerializer()
	class Meta:
		model=Receipts
		exclude=[]

class ReceiptsSerializerForSales(serializers.ModelSerializer):
	class Meta:
		model=Receipts
		exclude=['customer','payment_method']