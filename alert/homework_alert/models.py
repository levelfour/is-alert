import hashlib
from django.db import models


def get_nextautoincrement(mymodel):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT seq FROM SQLITE_SEQUENCE WHERE name='%s';" % \
                   mymodel._meta.db_table)
    row = cursor.fetchone()
    cursor.close()
    return row[0]

class Homework(models.Model):
    lecture = models.CharField(max_length=64)
    name = models.CharField(max_length=64, null=True)
    deadline = models.DateTimeField('deadline')
    created_at = models.DateTimeField('create datetime', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('update datetime', auto_now=True, null=True)

    def is_done(self, user_id):
        try:
            user_work = UserHomework.objects.get(user_id=user_id, homework_id=self.id)
            return user_work != None
        except UserHomework.DoesNotExist as e:
            return False


class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=512, null=True)
    user_token = models.CharField(max_length=128, null=True)
    access_token = models.CharField(max_length=128, null=True)
    created_at = models.DateTimeField('create datetime', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('update datetime', auto_now=True, null=True)
    
    @classmethod
    def generate_random_string(cls, length):
        import string
        import random
        return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])

    @classmethod
    def hash_password(cls, password_str):
        salt = 'PdnzQnXf9RaB2m5QtnfubTTXLxL6HRKuY73fwbsZ'
        return hashlib.sha256("{}{}{}".format(salt, int(get_nextautoincrement(cls))+1, password_str)).hexdigest()

    def check_password(self, password_str):
        salt = 'PdnzQnXf9RaB2m5QtnfubTTXLxL6HRKuY73fwbsZ'
        return self.password == hashlib.sha256("{}{}{}".format(salt, self.id, password_str)).hexdigest()

    def generate_user_token(self):
        self.user_token = User.generate_random_string(128)
        self.save()

    def update_token(self):
        self.access_token = User.generate_random_string(128)
        self.save()

    def check_token(self, token):
        return self.access_token == token

class UserHomework(models.Model):
    user = models.ForeignKey(User)
    homework = models.ForeignKey(Homework)
    created_at = models.DateTimeField('create datetime', auto_now_add=True, null=True)
