from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
# Register your models here.
class UserAdmin(BaseUserAdmin):
    fieldsets=(
        (None,{'fields':('username','email','password','role','first_name','last_name')}),
        ('Permissions',{'fields':(
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets=(
        (
            None,
            {
                'classes':('wide',),
                'fields':('username','email','role','password1','password2')
            }
        ),
    )

    list_display = ('email','username','role', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User,UserAdmin)











