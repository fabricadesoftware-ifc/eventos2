from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from eventos2.core.models import Event, User

admin.site.register(Event)
admin.site.register(User, UserAdmin)
