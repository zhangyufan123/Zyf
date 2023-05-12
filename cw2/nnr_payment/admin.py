from django.contrib import admin
from .models import user, consumption_record


# Register your models here.
admin.site.register(user)
admin.site.register(consumption_record)
