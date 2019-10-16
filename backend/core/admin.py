from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import Event, Sponsorship, SponsorshipCategory, User

admin.site.register(Event)
admin.site.register(Sponsorship)
admin.site.register(SponsorshipCategory)
admin.site.register(User, UserAdmin)
