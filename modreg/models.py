from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse

class Module(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField(unique=True)
    credit = models.IntegerField()
    availability = models.BooleanField(default=False)
    description = models.TextField()
    category = models.CharField(max_length=100)
    courses_registered = models.ManyToManyField(Group, blank=True)
    students = models.ManyToManyField(User, related_name='registered_modules', blank=True)
    author = models.ForeignKey(User, related_name='modules', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.code})'

    def get_absolute_url(self):
        return reverse('modreg:module-detail', kwargs={'code': self.code})
