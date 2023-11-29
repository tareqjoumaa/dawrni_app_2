from django.contrib import admin
from .models import Company, Client, Notification, Category, CompanyPhoto

# Register your models here.
admin.site.register(Company)
admin.site.register(Client)
admin.site.register(Notification)
admin.site.register(Category)
admin.site.register(CompanyPhoto)
