from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import Advisor
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import (
    CustomUser, DEO, Advisor, Chairman,
    Department, Year, Batch, Section,
    Teacher, Room, Course,
    TeacherCourseAssignment, BatchCourseTeacherAssignment
)


admin.site.site_header = "NED Administration"
admin.site.site_title = "NED Admin Portal"
admin.site.index_title = "Welcome to the NED Admin Panel"


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'staff_id',
            'phone_number',
        )

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Use our custom creation form for adding a user
    add_form = CustomUserCreationForm
    form = UserChangeForm  # For editing, you can use the default change form or a custom one

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'role',
                'staff_id',
                'phone_number',
                'password1',
                'password2',
            ),
        }),
    )

    # Extend the default fieldsets for the change view
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'profile_picture', 'staff_id', 'phone_number')}),
    )

    list_display = ('username', 'email', 'role', 'staff_id')
    list_filter = ('role',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Create the related profile after saving if needed
        if obj.role == 'deo' and not hasattr(obj, 'deo'):
            DEO.objects.get_or_create(user=obj, defaults={'department_name': ''})
        elif obj.role == 'advisor' and not hasattr(obj, 'advisor_profile'):
            Advisor.objects.get_or_create(user=obj, defaults={
                'year': '', 'faculty': '', 'seniority': '', 'deo': None
            })
@admin.register(DEO)
class DEOAdmin(admin.ModelAdmin):
    list_display = ('user', 'department_name')
    search_fields = ('user__username', 'department_name')


@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'year', 'faculty', 'seniority', 'profile_pic')
    search_fields = ('user__username', 'faculty', 'seniority')
    list_filter = ('year', 'seniority', 'deo', 'faculty')
    ordering = ('user__username',)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'



@admin.register(Chairman)
class ChairmanAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')
    search_fields = ('user__username', 'department')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'chairman')
    search_fields = ('name',)
    list_filter = ('chairman',)


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ('academic_year', 'academic_start', 'academic_end')
    search_fields = ('academic_year',)
    list_filter = ('academic_start', 'academic_end')



@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('Batch_ID','Discipline', 'Batch_name', 'Year')
    search_fields = ('Batch_name','Discipline',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('Section_ID', 'Batch_ID', 'Section_name', 'Max_students', 'Max_gaps')
    search_fields = ('Section_name',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('Teacher_ID', 'Name', 'Email', 'NIC', 'Phone', 'Max_classes')
    search_fields = ('Name', 'Email', 'NIC')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'Room_ID', 'Room_no', 'Max_capacity', 'Floor',
        'Room_type', 'Multimedia', 'Speaker', 'Room_status'
    )
    search_fields = ('Room_no',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'Course_ID', 'Course_name', 'Course_code', 'Batch_ID',
        'Max_classes_per_day', 'Credit_hours'
    )
    search_fields = ('Course_name', 'Course_code')


@admin.register(TeacherCourseAssignment)
class TeacherCourseAssignmentAdmin(admin.ModelAdmin):
    list_display = ('Assignment_ID', 'Teacher_ID', 'Course_ID', 'Teacher_type')


@admin.register(BatchCourseTeacherAssignment)
class BatchCourseTeacherAssignmentAdmin(admin.ModelAdmin):
    list_display = ('Batch_ID', 'Course_ID', 'Teacher_ID', 'Course_type', 'Section')
    list_filter = ('Batch_ID', 'Course_ID', 'Teacher_ID', 'Course_type', 'Section')
    search_fields = ('Batch_ID__Batch_name', 'Course_ID__Course_name', 'Teacher_ID__Name', 'Section__Section_name')
