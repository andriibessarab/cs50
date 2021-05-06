from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

import datetime


class UsersManagement(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None):
        if not username:
            raise ValueError('User must provide a username')
        if not email:
            raise ValueError('User must provide an email')
        if not first_name:
            raise ValueError('User must provide his first name')
        if not last_name:
            raise ValueError('User must provide his last name')

        user = self.model(
            username = username,
            email = self.normalize_email(email),
            first_name =first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)

    def create_superuser(self, username, email, first_name, last_name, password=None):
        if not username:
            raise ValueError('User must provide a username')
        if not email:
            raise ValueError('User must provide an email')
        if not first_name:
            raise ValueError('User must provide his first name')
        if not last_name:
            raise ValueError('User must provide his last name')
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)


class User(AbstractBaseUser):

    username = models.CharField(max_length=255, unique=True)

    email = models.EmailField(max_length=320, unique=True)

    first_name = models.CharField(max_length=255, unique=False)

    last_name = models.CharField(max_length=255, unique=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    last_login = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password', 'first_name', 'last_name']

    objects = UsersManagement()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Categorie(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    transactionTypesChoices = [
        ('+', 'Earnings'),
        ('-', 'Expencies'),
    ]

    transactionType = models.CharField(max_length=2, choices=transactionTypesChoices)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=18, decimal_places=2)

    def __str__(self):
        return str(self.id)


class Familie(models.Model):
    users = models.ManyToManyField(User)
    transactions = models.ManyToManyField(Transaction)
    categories = models.ManyToManyField(Categorie)

    def __str__(self):
        return str(self.id)


class ContactUsForm(models.Model):
    statusTypeChoices = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
    ]

    email = models.EmailField(max_length=320)

    name = models.CharField(max_length=255)

    topic = models.CharField(max_length=50)

    message = models.TextField()

    status = models.CharField(max_length=8, choices=statusTypeChoices, default='Pending')

    last_login = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return f'{self.id}({self.status})'