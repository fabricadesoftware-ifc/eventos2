from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from eventos2.core.models import Event, EventOwnership, EventRegistration, User

admin.site.register(Event)
admin.site.register(EventOwnership)
admin.site.register(EventRegistration)
admin.site.register(User, UserAdmin)
