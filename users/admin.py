from unfold import admin as uadmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User, Contact, VerificationCode


@admin.register(User)
class UserModelAdmin(UserAdmin, uadmin.ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ["username", "first_name", "last_name", "middle_name", "city", "town", ]
    model = User
    fieldsets = (
        ("Foydalanuvchini tahrirlash", {
            "fields": ("username", "first_name", "last_name", "middle_name", "city", "town", "password", )
        }), 
    )
    add_fieldsets = (
        ("Yangi foydalanuvchi qo'shish", {
            "fields": ("username", "password1", "password2", "first_name", "last_name", "middle_name", "city", "town", )
        }), 
    )


@admin.register(Contact)
class ContactModelAdmin(uadmin.ModelAdmin):
    list_display = ["name", "phone", "telegram"]


@admin.register(VerificationCode)
class CodeModelAdmin(uadmin.ModelAdmin):
    list_display = ["user", "code"]

admin.site.unregister(Group)

admin.site.index_title = 'IMedTeam admin panelga xush kelibsiz'
admin.site.site_header = 'IMedTeam'
admin.site.site_title = 'IMedTeam Admin'