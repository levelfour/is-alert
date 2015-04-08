from django.db import models


class Homework(models.Model):
    lecture = models.CharField(max_length=64)
    deadline = models.DateTimeField('deadline')


class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=512)


class UserHomework(models.Model):
    user = models.ForeignField(User)
    homework = models.ForeignField(Homework)
    created_at = models.DateTimeField('create datetime')
