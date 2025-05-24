from django.shortcuts import render
from .models import NumberClassification
from .serializers import NumberClassificationSerializer, NumberInputSeriailizer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .utils import NumberClassifier
from django.db import IntegrityError
# Create your views here.

class NumberClassificationViewset(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing number classification instances.
    """
    queryset = NumberClassification.objects.all()
    serializer_class = NumberClassificationSerializer
    
    @action(detail=False, methods=['get'], url_path='classify-number')
    def classify_number(self, request):
        """
        Classify a number and return its properties
        """
        number_param = request.query_params.get('number')
        if not number_param:
            return Response(
                {'number': '', 'error': True},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate the input number
        try:
            number = int(number_param)
        except (ValueError, TypeError):
            return Response(
                {'number': number_param, 'error': True},
                status=status.HTTP_400_BAD_REQUEST
            )
        #Check if classification already exists
        try:
            existing_classification = NumberClassification.objects.get(number=number)
            serializer = NumberClassificationSerializer(existing_classification)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NumberClassification.DoesNotExist:
            pass

        #Perform classification
        classifier = NumberClassifier()

        is_prime = classifier.is_prime(number)
        is_perfect = classifier.is_perfect(number)
        is_armstrong = classifier.is_armstrong(number)
        properties = classifier.get_properties(number)
        digit_sum = classifier.digit_sum(number)
        fun_fact = classifier.fun_fact(number)


        # Create and save classification

        try:
            classification = NumberClassification.objects.create(
                number=number,
                is_prime=is_prime,
                is_perfect=is_perfect,
                is_armstrong=is_armstrong,
                properties=properties,
                digit_sum=digit_sum,
                fun_fact=fun_fact
            )
            serializer = NumberClassificationSerializer(classification)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except IntegrityError:
            existing_classification = NumberClassification.objects.get(number=number)
            serializer = NumberClassificationSerializer(existing_classification)
            return Response(serializer.data, status=status.HTTP_200_OK)







        