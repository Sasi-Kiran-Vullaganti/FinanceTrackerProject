from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('userid', 'name', 'email','password', 'phone', 'gender', 'currency', 'date_created', 'last_login', 'last_updated')
    search_fields = ('name', 'email', 'phone', 'userid')
    list_filter = ('gender', 'currency', 'date_created')
    readonly_fields = ('userid', 'date_created', 'last_login', 'last_updated')

admin.site.register(UserProfile, UserProfileAdmin)
