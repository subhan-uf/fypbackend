from django.db import models
from users.models import *



class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    time_slot = models.CharField(max_length=50)  # e.g., "9:00 AM - 10:30 AM"
    day_of_week = models.CharField(max_length=10)  # e.g., "Monday"
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    locked = models.BooleanField(default=False)  # Indicates if the slot is locked by the advisor

    def __str__(self):
        return f"{self.course.title} by {self.teacher.name} in {self.room} on {self.day_of_week}"




class TeacherPreference(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, related_name='preferences')  # Link to Teacher model
    preferred_rooms = models.ManyToManyField(Room, blank=True, related_name='preferred_by_teachers')
    max_classes_per_day = models.PositiveIntegerField(default=4, help_text="Maximum number of classes the teacher can handle per day")
    health_limitations = models.TextField(blank=True, null=True, help_text="Any health constraints for the teacher")
    preferred_subjects = models.ManyToManyField(Course, blank=True, related_name='preferred_by_teachers')
    additional_preferences = models.JSONField(default=dict, blank=True, null=True, help_text="Additional or unknown preferences (stored as key-value pairs)")
    unavailable_days = models.CharField(max_length=100, null=True, blank=True, help_text="Days when the teacher is unavailable (e.g., 'Monday, Wednesday')")
    
    def __str__(self):
        return f"Preferences for {self.teacher.name}"




class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"






class Constraint(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    day_of_week = models.CharField(max_length=10)  # e.g., "Monday"
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    is_hard_constraint = models.BooleanField(default=True, help_text="If true, this is a hard constraint that must be followed.")

    def __str__(self):
        return f"Constraint for {self.teacher} or {self.room} on {self.day_of_week} during {self.time_slot}"






class TimetableGenerationLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed')])
    message = models.TextField(blank=True, null=True)  # Optional error/success message

    def __str__(self):
        return f"{self.timestamp} - {self.status}"
