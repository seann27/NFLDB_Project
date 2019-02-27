from django.contrib import admin

# Register your models here.
from .models import Teams
from .models import Players

admin.site.register(Teams)
admin.site.register(Players)