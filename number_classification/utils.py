import math
import requests
import logging
from .models import NumberClassification

logger = logging.getLogger(__name__)


class NumberClassifier:

    @classmethod
    def analyse_number(cls, number):
        """
        Analyse a number and return its properties
        """
        # Validate input first
        validated_number = cls._validate_number(number)
        
        try:
            # Try to get existing classification from database
            classification = NumberClassification.objects.get(number=validated_number)
            return classification.to_dict()
        except NumberClassification.DoesNotExist:
            # Calculate properties if not in database
            classification_data = cls._calculate_properties(validated_number)

            # Create new classification record
            classification = NumberClassification.objects.create(
                number=validated_number,
                is_prime=classification_data['is_prime'],
                is_perfect=classification_data['is_perfect'],
                is_armstrong=classification_data['is_armstrong'],
                properties=classification_data['properties'],
                digit_sum=classification_data['digit_sum'],
                fun_fact=classification_data['fun_fact']
            )
            return classification.to_dict()

    @staticmethod
    def _validate_number(number):
        """
        Check if the input is a valid number and return the integer
        """
        try:
            return int(number)
        except (ValueError, TypeError):
            raise ValueError("Invalid input. Please enter a valid integer.")

    @staticmethod
    def _calculate_digit_sum(number):
        """
        Calculate the sum of digits of a number
        """
        if not isinstance(number, int):
            raise ValueError("Number must be an integer.")
        return sum(int(digit) for digit in str(abs(number)))

    @staticmethod
    def _get_fun_fact(number):
        """
        Get a fun fact about the number using Numbers API
        """
        try:
            # Use the math type for mathematical facts, with notfound=floor for better coverage
            # and fragment=true for better sentence integration
            url = f"http://numbersapi.com/{number}/math"
            params = {
                'notfound': 'floor',  # Round down to nearest number with a fact if exact number not found
                'fragment': 'true'    # Return as sentence fragment for better integration
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200 and response.text.strip():
                # Capitalize first letter since we're getting a fragment
                fact = response.text.strip()
                if fact and not fact[0].isupper():
                    fact = fact[0].upper() + fact[1:] if len(fact) > 1 else fact.upper()
                # Add period if not present
                if fact and not fact.endswith('.'):
                    fact += '.'
                return fact
            else:
                return f"{number} is a number with its own unique mathematical properties."
                
        except requests.RequestException as e:
            logger.warning(f"Network error fetching fun fact for {number}: {e}")
            return f"{number} is a number with its own unique mathematical properties."
        except Exception as e:
            logger.warning(f"Unexpected error fetching fun fact for {number}: {e}")
            return f"{number} is a number with its own unique mathematical properties."

    @staticmethod
    def _get_properties(number, is_prime, is_perfect, is_armstrong):
        """
        Get list of properties for the number
        """
        properties = []
        
        if is_prime:
            properties.append("Prime")
        if is_perfect:
            properties.append("Perfect")
        if is_armstrong:
            properties.append("Armstrong")
        if number % 2 == 0:
            properties.append("Even")
        else:
            properties.append("Odd")
        
        return properties

    @staticmethod
    def _calculate_properties(number):
        """
        Calculate all properties of the number
        """
        is_prime = NumberClassifier._is_prime(number)
        is_perfect = NumberClassifier._is_perfect(number)
        is_armstrong = NumberClassifier._is_armstrong(number)
        digit_sum = NumberClassifier._calculate_digit_sum(number)
        fun_fact = NumberClassifier._get_fun_fact(number)
        properties = NumberClassifier._get_properties(number, is_prime, is_perfect, is_armstrong)
        
        return {
            'is_prime': is_prime,
            'is_perfect': is_perfect,
            'is_armstrong': is_armstrong,
            'digit_sum': digit_sum,
            'fun_fact': fun_fact,
            'properties': properties
        }

    @staticmethod
    def _is_prime(number):
        """
        Check if a number is prime
        """
        if number < 2:
            return False
        if number == 2:
            return True
        if number % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(number)) + 1, 2):
            if number % i == 0:
                return False
        return True

    @staticmethod
    def _is_perfect(number):
        """
        Check if a number is perfect
        """
        if number < 2:
            return False
        divisors_sum = 1
        for i in range(2, int(math.sqrt(number)) + 1):
            if number % i == 0:
                divisors_sum += i
                if i != number // i:
                    divisors_sum += number // i
        return divisors_sum == number

    @staticmethod
    def _is_armstrong(number):
        """
        Check if a number is an Armstrong number
        """
        if number < 0:
            return False
        
        digits = str(abs(number))
        num_length = len(digits)
        digit_sum = sum(int(digit) ** num_length for digit in digits)
        return digit_sum == abs(number)

    # Public instance methods for external access
    def is_prime(self, number):
        """
        Check if a number is prime (instance method for external use)
        """
        validated_number = self._validate_number(number)
        return self._is_prime(validated_number)

    def is_perfect(self, number):
        """
        Check if a number is perfect (instance method for external use)
        """
        validated_number = self._validate_number(number)
        return self._is_perfect(validated_number)

    def is_armstrong(self, number):
        """
        Check if a number is an Armstrong number (instance method for external use)
        """
        validated_number = self._validate_number(number)
        return self._is_armstrong(validated_number)

    def digit_sum(self, number):
        """
        Calculate the sum of digits of a number (instance method for external use)
        """
        validated_number = self._validate_number(number)
        return self._calculate_digit_sum(validated_number)

    def fun_fact(self, number):
        """
        Get a fun fact about the number (instance method for external use)
        """
        validated_number = self._validate_number(number)
        return self._get_fun_fact(validated_number)

    def get_properties(self, number):
        """
        Get all properties of a number as a dictionary (instance method for external use)
        """
        validated_number = self._validate_number(number)
        
        is_prime = self._is_prime(validated_number)
        is_perfect = self._is_perfect(validated_number)
        is_armstrong = self._is_armstrong(validated_number)
        digit_sum = self._calculate_digit_sum(validated_number)
        fun_fact = self._get_fun_fact(validated_number)
        properties = self._get_properties(validated_number, is_prime, is_perfect, is_armstrong)

        return {
            'number': validated_number,
            'is_prime': is_prime,
            'is_perfect': is_perfect,
            'is_armstrong': is_armstrong,
            'digit_sum': digit_sum,
            'fun_fact': fun_fact,
            'properties': properties
        }