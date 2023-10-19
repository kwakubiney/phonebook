from django.db import models

class PhoneBook(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    number = models.CharField(max_length=100, default='')
    is_blacklisted = models.BooleanField(default='white', max_length=100)
    class Meta:
        ordering = ['created_at']