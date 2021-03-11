import datetime

from django.db import models


# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()

    def baby_boomer_status(self):
        """
        """
        if self.birth_date < datetime.date(1945, 8, 1):
            return 'Pre-boomer'
        elif self.birth_date < datetime.date(1965, 1, 1):
            return 'Baby-boomer'
        else:
            return 'Post-boomer'

    @property
    def full_name(self):
        """
        Returns the person's full name
        """
        return


# abstract base classes
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True


class UnManaged(models.Model):
    class Meta:
        abstract = True
        managed = False


class Student(CommonInfo):
    home_group = models.CharField(max_length=5)

    class Meta(CommonInfo.Meta):
        db_table = 'student_info'


# Multi-table inheritance
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)


class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)


# Proxy models
class MyPerson(Person):
    class Meta:
        proxy = True

    def do_something(self):
        pass


class OrderedPerson(Person):
    class Meta:
        proxy = True
        ordering = ['last_name']
