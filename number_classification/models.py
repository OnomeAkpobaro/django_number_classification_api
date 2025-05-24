from django.db import models
import logging

logger = logging.getLogger(__name__)

class NumberClassification(models.Model):
    number = models.BigIntegerField(unique=True)
    is_prime = models.BooleanField()
    is_perfect = models.BooleanField()
    is_armstrong = models.BooleanField()
    properties = models.JSONField()
    digit_sum = models.PositiveIntegerField()
    fun_fact = models.TextField()

    class Meta:
        verbose_name = "Number Classification"
        verbose_name_plural = "Number Classifications"
        ordering = ['number']

    def __str__(self):
        return f"Classification of {self.number}"
        
    