from email.policy import default
from enum import Enum
from django.forms import ValidationError
from django.utils.text import slugify
from django.db import models
from uuid import uuid4


class Event(models.Model):
    name = models.CharField(max_length=100, verbose_name='Event name')
    start_datetime = models.DateTimeField(verbose_name="Start date & time", blank=True, null=True)
    end_datetime = models.DateTimeField(verbose_name="End date & time", blank=True, null=True)
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    location = models.CharField(max_length=200, verbose_name='Location', blank=True, null=True)
    slug = models.SlugField(unique=True, default=uuid4)
    admin_code = models.SlugField(unique=True, default=uuid4)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Status(Enum):
    INVITED = 'Invited'
    CONFIRMED = 'Confirmed'
    DECLINED = 'Declined'
    MAYBE = 'Maybe'
    WAITING_LIST = 'Waiting list'

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]

    @classmethod
    def default(cls):
        return cls.INVITED.value

class Response(models.Model):
    participant = models.CharField(max_length=100, verbose_name='Name')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    status = models.CharField(max_length=20, verbose_name='Status', choices=Status.choices(), default=Status.default())
    slug = models.SlugField(unique=True, default=uuid4)
    is_admin = models.BooleanField(default=False, verbose_name='Is Admin')

    def clean(self):
        if self.status not in dict(Status.choices()).keys():
            raise ValidationError('Invalid status')
        if not self.status:
            raise ValidationError('Please select a status')
    def __str__(self):
        return self.participant