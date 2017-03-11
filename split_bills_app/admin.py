from django.contrib import admin
from .models import Group, Bill, CustomUser
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Group)
admin.site.register(Bill)
