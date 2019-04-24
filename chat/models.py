from django.db import models
from django.utils import timezone
from chat.models import *
import re, bcrypt, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class MyObjManager(models.Manager):
    #VALIDATE REGISTER
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        if len(postData['email']) < 6:
            errors["email"] = "Email should be at least 6 characters"
        if User.objects.filter(email = postData['email']):
            errors["used_email"] = "Email is already used"
        if not EMAIL_REGEX.match(postData['email']):
            errors["not_email"] = "Please enter an email"
        if len(postData['password']) < 6:
            errors["password"] = "Password should be at least 6 characters"
        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Not matching Password"
        return errors
    #VALIDATE LOGIN
    def validate_login(self, postData):
        errors = {}
        user_login = User.objects.filter(email=postData["email_login"])
        if len(user_login) == 0:
            errors["failed_login"] = "Failed Login, Try again"
        else:
            this_user = User.objects.get(email=postData["email_login"])
            check_password = bcrypt.checkpw(postData["password_login"].encode(), this_user.password.encode())
            if check_password == False:
                errors["wrong_pass"] = "Wrong Password"
        return errors

    def edit_1_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["not_email"] = "Please enter an email"
        if len(postData['email']) < 6:
            errors["email"] = "Email should be at least 6 characters"
        if User.objects.filter(email = postData['email']):
            errors["used_email"] = "Email is already used"
        return errors

    def password_validator(self, postData):
        errors = {}
        if len(postData['password']) < 6:
            errors["password"] = "Password should be at least 6 characters"
        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Not matching Password"
        return errors

    def desc_validator(self, postData):
        errors = {}
        if len(postData['description']) < 1:
            errors["description"] = "Description should be at least 1 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.CharField(max_length=55)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MyObjManager()
    def __repr__(self):
        return f"<User: {self.first_name}  {self.email}: ({self.id})>"
