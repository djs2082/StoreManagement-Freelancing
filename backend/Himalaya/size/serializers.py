from rest_framework import serializers
from .models import SizeModel

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model=SizeModel
        fields=('__all__')