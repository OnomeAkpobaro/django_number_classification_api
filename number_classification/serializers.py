from .models import NumberClassification
from rest_framework import serializers


class NumberClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumberClassification
        fields = ['number', 'is_prime', 'is_perfect', 'properties', 'digit_sum', 'fun_fact']
    
    def validate_number(self, value):
        """
        Validate that the number is a positive integer
        """
        if not isinstance(value, int) or value < 0:
            raise serializers.ValidationError("Number must be a positive integer.")
        return value

class NumberInputSeriailizer(serializers.Serializer):

    def validate_number(self, value):

        try:
            number = int(value)
            return number
        except (ValueError, TypeError):
            raise serializers.ValidationError("Invalid input. Please enter a valid integer.")