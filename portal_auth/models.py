from django.contrib.auth.models import User

# Create your models here.
from django.db import models


class SystemUser(User):
    avatar = models.ImageField()
