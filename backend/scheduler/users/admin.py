from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import (
    CustomUser, DEO, Advisor, Chairman,
    Department, Year, Batch, Section,
    Teacher, Room, Course,
    TeacherCourseAssignment, BatchCourseTeacherAssignment
)

# ─── Admin site branding ───────────────────────────────────────────────────────
admin.site.site_header  = "NED Administration"
admin.site.site_title   = "NED Admin Portal"
admin.site.index_title  = "Welcome to the NED Admin Panel"

# ─── Unregister unwanted models ────────────────────────────────────────────────
# Remove the entire “Authentication and Authorization” group
admin.site.unregister(Group)

# Under “Users” we only want:
#   CustomUser, DEO, Advisor, Chairman, Teacher
# Everything else (the “rest”) gets unregistered here:
for m in (
    Department, Year, Batch, Section,
    Room, Course,
    TeacherCourseAssignment, BatchCourseTeacherAssignment
):
    try:
        admin.site.unregister(m)
    except admin.sites.NotRegistered:
        pass


# ─── YOUR “Users” SECTION ─────────────────────────────────────────────────────
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username','email','first_name','last_name',
            'role','staff_id','phone_number',
        )

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form      = CustomUserCreationForm
    form          = UserChangeForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username','email','first_name','last_name',
                'role','staff_id','phone_number',
                'password1','password2',
            ),
        }),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role','profile_picture','staff_id','phone_number')}),
    )
    list_display = ('username','email','role','staff_id')
    list_filter  = ('role',)

    def save_model(self, request, obj, form, change):
        # If we’re editing (not creating), fetch the old role
        old_role = None
        if change:
            # pull the original from the DB
            old_role = CustomUser.objects.get(pk=obj.pk).role

        # First call super to save the user object itself
        super().save_model(request, obj, form, change)

        new_role = obj.role

        # 1) If the role changed, delete the old profile
        if change and old_role != new_role:
            if old_role == 'advisor':
                Advisor.objects.filter(user=obj).delete()
            elif old_role == 'deo':
                DEO.objects.filter(user=obj).delete()
            # (you could also handle 'chairman' here if you had a profile model)

        # 2) Ensure the new profile exists
        if new_role == 'deo':
            DEO.objects.get_or_create(user=obj, defaults={'department_name': ''})
        elif new_role == 'advisor':
            Advisor.objects.get_or_create(
                user=obj,
                defaults={'year': '', 'faculty': '', 'seniority': '', 'deo': None}
            )

@admin.register(DEO)
class DEOAdmin(admin.ModelAdmin):
    list_display   = ('user','department_name')
    search_fields = ('user__username','department_name')

@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    list_display   = ('get_username','year','faculty','seniority','profile_pic')
    search_fields = ('user__username','faculty','seniority')
    list_filter   = ('year','seniority','deo','faculty')
    ordering      = ('user__username',)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

@admin.register(Chairman)
class ChairmanAdmin(admin.ModelAdmin):
    list_display   = ('user','department')
    search_fields = ('user__username','department')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display   = ('Teacher_ID','Name','Email','NIC','Phone','Max_classes')
    search_fields = ('Name','Email','NIC')


# ─── SCHEMA SECTION (new heading!) ─────────────────────────────────────────────
# We use proxy‐models with app_label='schema' so Django groups them under "Schema"

def make_proxy(model):
    return type(
        model.__name__ + 'Schema',
        (model,),
        {
            '__module__': model.__module__,
            'Meta': type('Meta', (), {
                'proxy': True,
                'app_label': 'schema',
                'verbose_name': model._meta.verbose_name,
                'verbose_name_plural': model._meta.verbose_name_plural,
            })
        }
    )

schema_models = [
    Department, Batch, Section,
    Room, Course
    
]

for real in schema_models:
    proxy = make_proxy(real)

    # reuse any list_display / filters you already defined, or fall back to all fields
    orig_admin = globals().get(real.__name__ + 'Admin', None)
    list_display = getattr(orig_admin, 'list_display', [f.name for f in real._meta.fields])
    search_fields = getattr(orig_admin, 'search_fields', [])
    list_filter = getattr(orig_admin, 'list_filter', [])

    admin.site.register(
        proxy,
        type(
            proxy.__name__ + 'Admin',
            (admin.ModelAdmin,),
            {
                'list_display': list_display,
                'search_fields': search_fields,
                'list_filter': list_filter,
            }
        )
    )
