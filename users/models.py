from django.db import models


class Factor(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.TextField()
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Research(models.Model):
    name = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    pre_item_context = models.TextField(max_length=500)
    item_text = models.TextField(max_length=500)
    post_item_context = models.TextField(max_length=500)
    level = models.ForeignKey(Level, on_delete=models.PROTECT)
    judgement = models.IntegerField()
    research = models.ForeignKey(Research, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_text


class User(models.Model):
    email_address = models.EmailField(max_length=200)
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
