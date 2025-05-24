from django.contrib import admin
from .models import NumberClassification

@admin.register(NumberClassification)
class NumberClassificationAdmin(admin.ModelAdmin):
    list_display = ('number', 'is_prime', 'is_perfect', 'is_armstrong', 'digit_sum', 'fun_fact')
    search_fields = ('number',)
    list_filter = ('is_prime', 'is_perfect', 'is_armstrong')

