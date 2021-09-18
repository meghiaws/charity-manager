from django.db import models
from django.db.models import Q
from django.utils import timezone

from accounts.models import User


class Benefactor(models.Model):
    EXPERIENCE_CHOICES = [
        (0, 'Beginner'),
        (1, 'Intermediate'),
        (2, 'Expert')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.SmallIntegerField(choices=EXPERIENCE_CHOICES, default=0)
    free_time_per_week = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.user.username


class Charity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.user.username}, {self.reg_number}'


class TaskManager(models.Manager):
    def related_tasks_to_charity(self, user):
        return self.filter(charity__user=user)

    def related_tasks_to_benefactor(self, user):
        return self.filter(assigned_benefactor__user=user)

    def all_related_tasks_to_user(self, user):
        return self.filter(Q(charity__user=user) | Q(assigned_benefactor__user=user) | Q(state='P'))


class Task(models.Model):
    PENDING = 'P'
    WAITING = 'W'
    ASSIGNED = 'A'
    DONE = 'D'
    STATE_CHOICES = [
        (PENDING, 'Pending'),
        (WAITING, 'Waiting'),
        (ASSIGNED, 'Assigned'),
        (DONE, 'DONE'),
    ]

    MALE = 'M'
    FEMALE = 'F'
    GENDER_LIMIT_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    assigned_benefactor = models.ForeignKey(Benefactor, null=True, on_delete=models.SET_NULL)
    charity = models.ForeignKey(Charity, on_delete=models.DO_NOTHING)
    age_limit_from = models.IntegerField(blank=True, null=True)
    age_limit_to = models.IntegerField(blank=True, null=True)
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)
    gender_limit = models.CharField(choices=GENDER_LIMIT_CHOICES, default=PENDING, max_length=1)
    state = models.CharField(choices=STATE_CHOICES, max_length=1)
    title = models.CharField(max_length=100)
    objects = TaskManager()
    

    def __str__(self):
        return f'{self.title} "{self.assigned_benefactor}"'
