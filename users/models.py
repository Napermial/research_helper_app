from django.db import models
from django.contrib.auth.models import User


class Experiment(models.Model):
    name = models.TextField()
    intro_text = models.TextField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Factor(models.Model):
    name = models.TextField()
    experiment_id = models.ForeignKey(Experiment, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.TextField()
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Item(models.Model):
    pre_item_context = models.TextField(max_length=500, null=True)
    item_text = models.TextField(max_length=500)
    post_item_context = models.TextField(max_length=500, null=True)
    lexicalization = models.IntegerField(null=True)
    experiment_id = models.ForeignKey(Experiment, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_text


class ItemLevel(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)


class Judgement(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    judgement = models.FloatField()

    def __str__(self):
        return self.judgement


class Intro(models.Model):
    text = models.TextField(max_length=400)
    last = models.BooleanField()

    def __str__(self):
        return self.text
