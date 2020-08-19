from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
	fname=serializers.CharField(required=False)
	lname=serializers.CharField(required=False)
	mobile=serializers.CharField(required=False)
	birth_date=serializers.DateField(required=False)
	date=serializers.DateField(required=False)
	class Meta:
		model=Customer
		exclude=[]

	def update(self,customer):
		if('first_name' in self.validated_data.keys()):
			customer.fname=fname
		if('last_name' in self.validated_data.keys()):
			customer.lname=lname
		if('birth_date' in self.validated_data.keys()):
			customer.birth_day=birth_day
		customer.save()
		return customer