from django.db import models


class Animal(models.Model):
    name = models.CharField(max_length=100)
    sound = models.CharField(max_length=100)

    def speak(self):
        return 'The {name} says "{sound}"'.format(name=self.name, sound=self.sound)
