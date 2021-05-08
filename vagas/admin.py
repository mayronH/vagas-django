from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Company, Applicant, Opportunity, Salary, Schooling, CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

# Register your models here.
admin.site.register(Company)
admin.site.register(Applicant)
admin.site.register(Opportunity)
admin.site.register(Salary)
admin.site.register(Schooling)