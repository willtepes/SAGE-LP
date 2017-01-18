from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import re, bcrypt, string


# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def login(self, request_post):
        try:
            user = self.get(user_name=request_post['login_user_name'])
            password = request_post['login_password'].encode()
            if bcrypt.hashpw(password, user.pw_hash.encode()) == user.pw_hash.encode():
                return (True, user)
        except ObjectDoesNotExist:
            pass

        return (False, ["Username/password not found."])

    def register(self, user):
        errors = []
        if len(user['name'])< 3:
            errors.append("Name must be at least 3 charecters.")
        if len(user['user_name']) < 3:
            errors.append("Username must be at least 3 charecters.")
        if len(user['password']) < 8:
            errors.append("Password must be at least 8 charecters.")
        if user['confirm_password'] != user['password']:
            errors.append("Passwords do not match.")
        try:
            user = self.get(user_name=user['user_name'])
            errors.append("Username already in use")
        except ObjectDoesNotExist:
            pass

        if len(errors) > 0:
            return (False, errors)

        pw_hash = bcrypt.hashpw(user['password'].encode(), bcrypt.gensalt())
        returnuser = self.create(name=user['name'], user_name=user['user_name'], pw_hash=pw_hash)
        if 'admin' in user:
            returnuser.is_admin = True
            returnuser.save()
        return (True, returnuser)

    def admin_exists(self):
        admin = self.filter(is_admin=True)
        if admin:
            return True
        else:
            return False

    def delete_user(self, user_id):
        self.get(id=user_id).delete()
        return

class User(models.Model):
    name = models.CharField(max_length=45)
    user_name = models.CharField(max_length=45)
    pw_hash = models.CharField(max_length=255)
    question_on = models.IntegerField(default=1)
    stars = models.IntegerField(default=0)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def pic_url(self):
        return 'learning_app/img/third-grade-' +str(self.question_on) + '.jpg'


    objects = UserManager()
