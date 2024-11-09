from django.db import models
from users.models import *


# class TeacherPreference(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     preferred_days = models.CharField(max_length=100)  # e.g., "Monday, Wednesday"
#     max_hours_per_day = models.PositiveIntegerField()
#     preferred_time_slots = models.CharField(max_length=100)  # e.g., "9:00-10:30, 14:00-15:30"
#     unavailable_days = models.CharField(max_length=100, null=True, blank=True)  # e.g., "Friday"

#     def __str__(self):
#         return f"{self.teacher.name} Preferences"


# class Timetable(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
#     time_slot = models.CharField(max_length=50)  # e.g., "9:00 AM - 10:30 AM"
#     day_of_week = models.CharField(max_length=10)  # e.g., "Monday"
#     section = models.ForeignKey(Section, on_delete=models.CASCADE)
#     batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.course.title} by {self.teacher.name} in {self.room} on {self.day_of_week}"
    
