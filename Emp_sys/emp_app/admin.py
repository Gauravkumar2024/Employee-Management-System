from django.contrib import admin

# Register your models here.
from .models import Department, Role, Employee
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(Employee)