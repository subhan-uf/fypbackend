from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import Advisor

from .models import (
    CustomUser, DEO, Advisor, Chairman,
    Department, Year, Batch, Section,
    Teacher, Room, Course,
    TeacherCourseAssignment, BatchCourseTeacherAssignment
)


admin.site.site_header = "NED Administration"
admin.site.site_title = "NED Admin Portal"
admin.site.index_title = "Welcome to the NED Admin Panel"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'profile_picture', 'staff_id', 'phone_number')}),
    )
    list_display = ('username', 'email', 'role', 'staff_id')
    list_filter = ('role',)


@admin.register(DEO)
class DEOAdmin(admin.ModelAdmin):
    list_display = ('user', 'department_name')
    search_fields = ('user__username', 'department_name')


@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    list_display = ('username', 'year', 'faculty', 'seniority', 'profile_pic')
    search_fields = ('username', 'faculty', 'seniority')
    list_filter = ('year', 'seniority','deo','faculty')
    ordering = ('username',)


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
    list_display = (
        'Assignment_ID', 'Batch_ID', 'Course_ID',
        'Teacher_ID', 'Course_type'
    )
