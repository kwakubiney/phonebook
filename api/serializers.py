from rest_framework import serializers
from .models import PhoneBook

class PhoneBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneBook
        fields = ('id', 'number', 'created_at', 'updated_at', 'is_blacklisted')