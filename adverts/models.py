from django.db import models
from django.contrib.auth.models import User


class VWUser(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    username = models.CharField(max_length=300)
    email = models.CharField(max_length=300)
    password = models.CharField(max_length=300)
    keywords = models.CharField(max_length=300)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

    class Meta:
        app_label = "adverts"



