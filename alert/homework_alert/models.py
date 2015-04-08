from django.db import models


class Homework(models.Model):
    lecture = models.CharField(max_length=64)
    name = models.CharField(max_length=64, null=True)
    deadline = models.DateTimeField('deadline')
    created_at = models.DateTimeField('create datetime', null=True)
    updated_at = models.DateTimeField('update datetime', null=True)


class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=512)
    created_at = models.DateTimeField('create datetime', null=True)
    updated_at = models.DateTimeField('update datetime', null=True)

class UserHomework(models.Model):
    user = models.ForeignKey(User)
    homework = models.ForeignKey(Homework)
    created_at = models.DateTimeField('create datetime', null=True)
