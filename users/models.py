from django.db import models
from django.contrib.auth.models import User, Group
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='media/profile_pics/default.png', upload_to='profile_pics')
    role = models.CharField(
        max_length=20,
        default='student',
        choices=[
            ('student', 'Student'),
            ('admin', 'Admin'),
        ]
    )
    course = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.course}'