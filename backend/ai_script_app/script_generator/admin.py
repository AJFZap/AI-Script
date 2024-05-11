from django.contrib import admin
from .models import ScriptsList, CustomUser

# Register your models here.To be able to see them as an Admin.

admin.site.register(ScriptsList)
admin.site.register(CustomUser)
