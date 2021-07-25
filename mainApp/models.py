from django.db import models
import re
import bcrypt

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class CustomerManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name should be atleast 2 characters long'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name should be atleast 2 characters long'
        if len(postData['email']) == 0:
            errors["email"] = "You must enter an email"
        elif not email_regex.match(postData['email']):
            errors["email"] = "Your email must be valid"
        current_users = Customer.objects.filter(email=postData['email'])
        if len(current_users) > 0 :
            errors["duplicate"] = "Email input is already in use"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData['confirm_pass']:
            errors['pw_match'] = "Password must match!"
        
        return errors

class Customer(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.CharField(max_length=75)
    password = models.CharField(max_length=55)
    created_at = models.DateField(auto_now_add=True)
    objects = CustomerManager()

class Child(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    allergies = models.TextField()
    # allergies switch to ChoiceField/dropdown?
    #Fetch choices from API call
    parent = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)