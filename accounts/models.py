from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    address = models.TextField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)
