from django.db import models

# Create your models here.
# custom_auth/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, mobile_number, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not mobile_number:
            raise ValueError("The Mobile Number field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, mobile_number, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_number']

    def __str__(self):
        return self.email

# models.py

from django.db import models

class Dashboard(models.Model):
    date = models.DateTimeField(
        ["%Y-%m-%d %H:%M:%S"],  # Add your desired date format here
    )
    total_stock = models.DecimalField(max_digits=10, decimal_places=2)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    profit_loss = models.DecimalField(max_digits=10, decimal_places=2)
    new_orders = models.TextField()

    def __str__(self):
        return f'Dashboard for {self.date}'


# models.py

from django.db import models

class Order(models.Model):
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    # Add more fields as needed

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)