from django.contrib import admin
from .models import CustomUser, DEO, Advisor, Chairman,Department, Year, Batch, Section, Equipment, Room, Lab, Course, Teacher, TeacherPreference, Timetable
from django.contrib.auth.admin import UserAdmin

# Register CustomUser with UserAdmin for role selection in admin    
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'profile_picture', 'staff_id', 'phone_number')}),
    )
    list_display = ('username', 'email', 'role', 'staff_id')
    list_filter = ('role',)

# Register DEO
@admin.register(DEO)
class DEOAdmin(admin.ModelAdmin):
    list_display = ('user', 'department_name')
    search_fields = ('user__username', 'department_name')

# Register Advisor
@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    list_display = ('username', 'year', 'faculty', 'seniority', 'profile_pic')  #
    search_fields = ('username', 'faculty', 'seniority') 
    list_filter = ('year', 'seniority','deo','faculty')  
    ordering = ('username',)  

    def save_model(self, request, obj, form, change):
        # Custom logic can be added here when saving an Advisor instance
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # Custom logic can be added here when deleting an Advisor instance
        super().delete_model(request, obj)

# Register Chairman
@admin.register(Chairman)
class ChairmanAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')
    search_fields = ('user__username', 'department')





# Register Department
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'chairman')
    search_fields = ('name',)
    list_filter = ('chairman',)

# Register Year
@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ('academic_year', 'academic_start', 'academic_end')
    search_fields = ('academic_year',)
    list_filter = ('academic_start', 'academic_end')

# Register Batch
@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('year', 'batch_id')
    search_fields = ('batch_id',)
    list_filter = ('year',)

# Register Section
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('batch', 'section_id', 'students_count')
    search_fields = ('section_id',)
    list_filter = ('batch',)

# Register Equipment
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('projector', 'speaker', 'pc_connection', 'wifi')

# Register Room
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('floor', 'department', 'max_std_limit', 'room_no', 'equipment')
    search_fields = ('room_no',)
    list_filter = ('department',)

# Register Lab
@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ('floor', 'lab_no', 'max_capacity', 'department', 'equipment')
    search_fields = ('lab_no',)
    list_filter = ('department',)

# Register Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'title', 'theory_hours', 'practical_hours', 'credit_hours', 'department', 'year')
    search_fields = ('course_code', 'title')
    list_filter = ('department', 'year')

# Register Teacher
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email', 'faculty', 'department', 'designation')
    search_fields = ('name', 'username', 'email')
    list_filter = ('faculty', 'department', 'designation')

# Register TeacherPreference
@admin.register(TeacherPreference)
class TeacherPreferenceAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'preferred_days', 'max_hours_per_day', 'preferred_time_slots', 'unavailable_days')
    search_fields = ('teacher__name', 'preferred_days')
    list_filter = ('teacher',)

# Register Timetable
@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('course', 'teacher', 'room', 'time_slot', 'day_of_week', 'section', 'batch')
    search_fields = ('course__title', 'teacher__name', 'room__room_no')
    list_filter = ('day_of_week', 'batch')