from django.db import models


class Author(models.Model):
    """
    作者
    """
    name = models.CharField(max_length=100)
    age = models.IntegerField()


class Publisher(models.Model):
    """
    出版社
    """
    name = models.CharField(max_length=100)


class PockyBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(author='Pocky')


class Book(models.Model):
    """
    书籍
    """
    objects = models.Manager()
    pocky_objects = PockyBookManager()
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()


class Store(models.Model):
    """
    书店
    """
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)
