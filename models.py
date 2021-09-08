from django.db import models
import re

class LoginManager(models.Manager):
    def basic_validator(self, formInfo):
        errors = {}
        if len(formInfo['first_name']) < 2:
            errors['first_name'] = "Please enter a name longer than 1 character."
        if len(formInfo['last_name']) < 2:
            errors['last_name'] = "Please enter a last name longer than 1 character."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(formInfo['email']):        
            errors['email'] = "Invalid email address!"
        if len(formInfo['password']) < 7:
            errors['password'] = "Please enter a password of at least 8 characters"
        if formInfo['password'] != formInfo['confirm_password']:
            errors['confirm_password'] = "Your passwords don't match."
        return errors
    def user_validator(self, formInfo):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(formInfo['email']):        
            errors['email'] = "Invalid username!"
        if len(formInfo['password']) < 7:
            errors['password'] = "Please enter a password of at least 8 characters"
        return errors
    def message_validator(self, formInfo):
        errors = {}
        if len(formInfo['newMessage']) < 1:
            errors['post'] = "You need to type something first!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LoginManager()

class Message(models.Model):
    user_id = models.ForeignKey(User, related_name='posts', on_delete = models.CASCADE)
    post = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LoginManager()

class Comment(models.Model):
    message_id = models.ForeignKey(Message, related_name='comments', on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, related_name='user_comments', on_delete = models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

