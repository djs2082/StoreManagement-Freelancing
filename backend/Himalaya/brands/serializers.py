from rest_framework import serializers
from .models import BrandModel
from items.serializers import ItemSerializer

class BrandSerializer(serializers.ModelSerializer):
	item=ItemSerializer()
	discount_given = serializers.SerializerMethodField('get_discount_given')
	actual_cost_price = serializers.SerializerMethodField('get_actual_cost_price')

	def get_discount_given(self, obj):
		return obj.cost_price*(obj.initial_discount/100)

	def get_actual_cost_price(self, obj):
		return obj.cost_price-obj.cost_price*(obj.initial_discount/100)

	class Meta:
		model=BrandModel
		fields=('__all__')