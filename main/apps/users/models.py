# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        users = User.objects.all()
        for user in users:
            if user.email == postData['email']:
                errors['duplicate_email'] = "Email already in database"
        if len(postData['email']) < 1:
            errors["empty_email"] = "Email cannot be empty!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['invalid_email'] = "Invalid Email Address!"
        if len(postData['first_name']) < 1:
            errors["empty_first_name"] = "First name cannot be empty!"
        if any(i.isdigit() for i in postData['first_name']) == True:
            errors["invalid_first_name"] = "Invalid first name!"
        if len(postData['last_name']) < 1:
            errors["empty_last_name"] = "Last name cannot be empty!"
        if any(i.isdigit() for i in postData['last_name']) == True:
            errors["invalid_last_name"] = "Invalid last name!"
        if len(postData['password']) < 8:
            errors["short_password"] = "Password must contain at least eight characters!"
        if postData['confirm_password'] != postData['password']:
            errors["password_does_not_match"] = "Passwords must match!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()