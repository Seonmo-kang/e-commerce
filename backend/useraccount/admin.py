import email
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .forms import UserRegisterationForm, UserChangeForm
from .models import User,Profile

# from .forms import User, UserChangeForm

# @admin.register(User, admin.site)
class UserAdmin(BaseUserAdmin):
    #The forms to add and change instances
    form = UserChangeForm
    add_form = UserRegisterationForm

    list_display = ['id','email', 'password','is_staff','is_active','is_superuser','created_at']
    list_display_links= ('email',)
    list_filter = ('email',)

    fieldsets = [
        ('Infomation',
        {'fields': ('email', 'password')})
    ]

    search_fields = ('email',)
    ordering = ('-created_at',)
    filter_horizontal = ()

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','user']
    list_filter = ('credit_method','state','zipcode')
    search_fields = ('first_name',)

admin.site.register(User,UserAdmin)
admin.site.register(Profile,ProfileAdmin)
