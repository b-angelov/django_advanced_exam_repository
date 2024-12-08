from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin

from izpitnik.accounts.models import Profile

# Register your models here.

MyUser  = get_user_model()

# admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(MyUser)
class UserAdmin(UserAdmin, ModelAdmin):
    pass

@admin.register(Group)
class UserAdmin(GroupAdmin, ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    pass
