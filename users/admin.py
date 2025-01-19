from unfold import admin as uadmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User, Contact


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
