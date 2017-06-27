

from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
import bcrypt
import re
from datetime import date, datetime, timedelta, time
import datetime

# Matches the email to make sure the format is atleast one letter (lower or uppercase),
# number, or of of there characters . + _ -  Then an @ sign with the same format and
# lastly make sure there is a . followed by the same pattern.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# The password is any characters and there are atleast 7.
PASSWORD_REGEX = re.compile(r'^.{7,}$')

# The username checks for numbers and letters that can contain _ or . just not next to
# eachother, plus there has to be 5 through 18 characters.
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9]([._](?![._])|[a-zA-Z0-9]){5,18}[a-zA-Z0-9]$')

# The date just checks for a year with 4 numbers a month with 2 numbers and a day with 2
# numbers.
DATE_REGEX = re.compile(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$')

class UserManager(models.Manager):
    # Call this function to check for validation of all field for registation.
    # How to call: Table.userManager.registration(request.POST)
    def registration(self, userInput):
        today=datetime.datetime.now()
        past=today+timedelta((-14*365)-4)
        # errorList - Keeps tracks of all errors with the validation.
        errorList = []

        # Checks to see if first_name is greater than 2 characters.
        if len(userInput['first_name']) < 2:
            errorList.append('First name needs to be greater than 2 letters!\n')

        # Checks to see if last_name is greater than 2 characters.
        if len(userInput['last_name']) < 2:
            errorList.append('Last name needs to be greater than 2 letters!\n')

        # Checks to see if first_name contains only alphabetical letters.
        if not userInput['first_name'].isalpha():
            errorList.append('First name may only contain letters!\n')

        # Checks to see if last_name contains only alphabetical letters.
        if not userInput['last_name'].isalpha():
            errorList.append('Last name may only contain letters!\n')

        # Checks if the username matches the USERNAME_REGEX.
        if not USERNAME_REGEX.match(userInput['username']):
            errorList.append('Username does not match the required conventions. Only alphabetical and numerical characters plus _ and . are accepted but not ._ or ._ !!!\n')

        # Checks if the date of birth matches the DATE_REGEX.
        if not DATE_REGEX.match(userInput['dob']):
            errorList.append('Incorrect format please re-enter the values with the date picker!\n')
        # Try to get the date if it exists otherwise go to the exception.
        try:

          if datetime.datetime.strptime(userInput['dob'],'%Y-%m-%d')>past:
            errorList.append('You have to be 14 or older to be a member!\n')
        except:
            if DATE_REGEX.match(userInput['dob']):
                errorList.append('This does not exist! Incorrect form!\n')

        # Checks if the email matches the EMAIL_REGEX.
        if not EMAIL_REGEX.match(userInput['email']):
            errorList.append('Email is not a valid email! Try this format: something@example.com\n')

        # Checks if the password matches the PASSWORD_REGEX.
        if not PASSWORD_REGEX.match(userInput['password']):
            errorList.append('Password is not long enough.\n')

        # Checks to make sure the password inputs match.
        if userInput['password'] != userInput['confirm_password']:
            errorList.append('Password match not confirmed.\n')

        # Checks the database to see if the username already exists.
        if self.filter(username = userInput['username']):
            errorList.append('This username already exists in our database.\n')

        # Checks the database to see if the email already exists.
        if self.filter(email = userInput['email']):
            errorList.append('This email already exists in our database.\n')

        # If the list has no errors.
        if not errorList:
            hashed = bcrypt.hashpw(userInput['password'].encode(), bcrypt.gensalt())
            current_user = self.create(first_name = userInput['first_name'], last_name = userInput['last_name'], username=userInput['username'], date_of_birth=userInput['dob'], email = userInput['email'], password = hashed)
            return True, current_user
        return False, errorList

    # Call this function to check for validation of all field for login.
    # How to call: Table.userManager.login(request.POST)
    def login(self, userInput):
        # errorList - Keeps tracks of all errors with the validation.
        errorList = []

        # Checks if the username and password don't match.
        if not userInput['username_email'] and not userInput['password']:
            errorList.append('Unsuccessful login. Please fill in the username and password field!\n')
            return False, errorList

        # Checks if the username is in the database.
        if self.filter(username = userInput['username_email']):
            hashed = self.get(username = userInput['username_email']).password.encode()
            password = userInput['password'].encode()

            # Checks if the password is the correct one to the hashed one.
            if bcrypt.hashpw(password, hashed) == hashed:
                return True, self.get(username=userInput['username_email'])
        elif self.filter(email = userInput['username_email']) :
            hashed = self.get(email = userInput['username_email']).password.encode()
            password = userInput['password'].encode()

            # Checks if the password is the correct one to the hashed one.
            if bcrypt.hashpw(password, hashed) == hashed:
                return True, self.get(email=userInput['username_email'])

            else:
                errorList.append('Unsuccessful login. Incorrect password!\n')
        else:
            errorList.append('Unsuccessful login. Your email or username is incorrect!\n')
        return False, errorList


class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    date_of_birth = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    model_pic = models.ImageField(upload_to = 'imageApp/images/users/', default = 'imageApp/images/users/no-img.png', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userManager = UserManager()


@receiver(pre_save, sender=User)
def delete_old_user_picture(sender, instance, *args, **kwargs):
    if instance.pk:
        existing_image = User.objects.get(pk=instance.pk)
        if instance.model_pic and existing_image.model_pic != instance.model_pic:
            existing_image.model_pic.delete(False)
