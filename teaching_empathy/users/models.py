from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    POLITICAL_CHOICES = (
        ("Democrat", "Democrat"),
        ("Republican", "Republican"),
        ("Libertarian", "Libertarian"),
        ("Green Party", "Green Party"),
        ("Other", "Other"),
    )

    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)
    email = models.EmailField()
    age = models.IntegerField(null=True)
    gender = models.TextField(choices=GENDER_CHOICES, null=True)
    political_status = models.TextField(choices=POLITICAL_CHOICES, null=True)

    # Metadata
    class Meta: 
        ordering = ['last_name']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of User."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the User object (in Admin site etc.)."""
        return f"{self.first_name} {self.last_name}"