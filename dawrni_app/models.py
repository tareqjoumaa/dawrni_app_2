from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_ar = models.CharField(max_length=255, verbose_name=_("Name (Arabic)"), null=True, blank=True)
    name_en = models.CharField(max_length=255, verbose_name=_("Name (English)"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Category"))
    address_ar = models.TextField(verbose_name=_("Address (Arabic)"), null=True, blank=True)
    address_en = models.TextField(verbose_name=_("Address (English)"))
    is_certified = models.BooleanField(default=False, verbose_name=_("Is Certified"))
    about_ar = models.TextField(verbose_name=_("About (Arabic)"), null=True, blank=True)
    about_en = models.TextField(verbose_name=_("About (English)"))

    def __str__(self):
        return self.name_en


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255) 
    photo = models.ImageField(upload_to='client_photos/', null=True, blank=True)
    
    def __str__(self):
        return self.name_en  


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)  
    body = models.TextField()
    
    def __str__(self):
        return self.name    


class CompanyPhoto(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='company_photos/')
