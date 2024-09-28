from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime
import os
import time


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.role

class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100)
    dept_abbr = models.CharField(max_length=100, blank=True, null=True)
    authority = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.dept_name

class StaffCategory(models.Model):
    st_cat_id = models.AutoField(primary_key=True)
    st_cat_name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.st_cat_name

def dp_upload_to(instance, filename):
    timestamp = int(time.time())    
    extension = os.path.splitext(filename)[1]    
    new_filename = f"{instance.username}_{timestamp}{extension}"
    year = time.strftime('%Y')  # Get the current year
    # role = instance.role.role
    return f'profile_images/{year}/{instance.role.role}/{instance.username}/{new_filename}'


def signature_upload_to(instance, filename):
    timestamp = int(time.time())    
    extension = os.path.splitext(filename)[1]    
    new_filename = f"{instance.username}_{timestamp}{extension}"
    year = time.strftime('%Y')  # Get the current year
    # role = instance.role.role
    return f'signatures/{year}/{instance.role.role}/{instance.username}/{new_filename}'

class UserManager(BaseUserManager):
    def create_user(self,email, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username,email=email ,**extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self,email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)  
        extra_fields.setdefault('is_active', True)
        return self.create_user(email=email, password=password, username=username ,**extra_fields)

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20, unique=True, editable=False, blank=True, null=True) 
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)
    st_cat = models.ForeignKey('StaffCategory', on_delete=models.SET_NULL, null=True, blank=True)
    dept = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    dob = models.DateField(blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    first_name = models.CharField(max_length=100)  
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20)  
    status = models.BooleanField(default=True)  
    dp_image = models.ImageField(upload_to=dp_upload_to, blank=True, null=True) 
    signature = models.ImageField(upload_to=signature_upload_to, blank=True, null=True) 
    address = models.CharField(max_length=200, blank=True, null=True)
    is_password_renew = models.BooleanField(default=False) 
    renew_password = models.CharField(max_length=200, default="No")  
    last_login = models.DateTimeField(blank=True, null=True)
    is_login = models.BooleanField(default=False) 
    created_by = models.IntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True) 
    last_ip_address = models.GenericIPAddressField(blank=True, null=True)

    # Fields for admin and permissions
    is_staff = models.BooleanField(default=False)  # Required for accessing the Django admin
    is_active = models.BooleanField(default=True)  # Active users
    is_superuser = models.BooleanField(default=False)  # Superuser flag

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'phone']

    objects = UserManager()

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if not self.user_id and self.id:
            user_id = f"USER{self.id}"  # Format 'USER{id}'
            User.objects.filter(id=self.id).update(user_id = user_id)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
