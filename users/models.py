from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Factor(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.TextField()
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Experiment(models.Model):
    name = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.IntegerField

    def __str__(self):
        return self.name


class Item(models.Model):
    pre_item_context = models.TextField(max_length=500)
    item_text = models.TextField(max_length=500)
    post_item_context = models.TextField(max_length=500)
    level = models.ForeignKey(Level, on_delete=models.PROTECT)
    judgement = models.FloatField()
    research = models.ForeignKey(Experiment, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_text
