from django.db import models
from users.models import Teacher, Room, Course, Batch, Section  # or from users.models import *

class Compensatory(models.Model):
    # Django's default 'id' is real PK
    Compensatory_ID = models.IntegerField(unique=True)
    Teacher_ID = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    Course_ID = models.ForeignKey(Course, on_delete=models.CASCADE)
    Room_ID = models.ForeignKey(Room, on_delete=models.CASCADE)
    Date = models.DateField()
    Start_time = models.TimeField()
    End_time = models.TimeField()
    Status = models.CharField(max_length=50, blank=True, null=True)
    Desc = models.TextField(blank=True, null=True)
    Section = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Compensatory: Tchr={self.Teacher_ID.Name}, Course={self.Course_ID.Course_name}, {self.Date}"


class CoursePreferenceConstraints(models.Model):
    Preference_ID = models.AutoField(primary_key=True)
    Course_ID = models.ForeignKey(Course, on_delete=models.CASCADE)
    Date = models.DateField()
    Start_time = models.TimeField(null=True, blank=True)
    End_time = models.TimeField(null=True, blank=True)
    Status = models.CharField(max_length=50, blank=True, null=True)
    Teacher_ID = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    LAB_OR_THEORY_CHOICES = [
        ('lab', 'Lab'),
        ('theory', 'Theory'),
    ]
    Lab_or_Theory = models.CharField(max_length=10, choices=LAB_OR_THEORY_CHOICES)
    Multimedia_requirement = models.BooleanField(default=False)
    Speaker = models.BooleanField(default=False)
    Hard_constraint = models.BooleanField(default=False)

    def __str__(self):
        return f"PrefConstraint: Course={self.Course_ID.Course_name}, Tchr={self.Teacher_ID.Name}"


class TeacherRoomPreference(models.Model):
    Room_Preference_ID = models.AutoField(primary_key=True)
    Teacher_ID = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    Floor = models.CharField(max_length=10, blank=True, null=True)


    def __str__(self):
        return f"TchrRoomPref: Tchr={self.Teacher_ID.Name}"


class TimetableHeader(models.Model):
    Timetable_ID = models.IntegerField(unique=True)
    Batch_ID = models.ForeignKey(Batch, on_delete=models.CASCADE)
    Section_ID = models.ForeignKey(Section, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return f"TimetableHeader: Batch={self.Batch_ID.Batch_name}, Section={self.Section_ID.Section_name}"


class TimetableDetail(models.Model):
    Detail_ID = models.IntegerField(unique=True)
    Timetable_ID = models.ForeignKey(TimetableHeader, on_delete=models.CASCADE)
    Course_ID = models.ForeignKey(Course, on_delete=models.CASCADE)
    Teacher_ID = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    Room_ID = models.ForeignKey(Room, on_delete=models.CASCADE)
    Day = models.CharField(max_length=10, blank=True, null=True)
    Start_time = models.TimeField(null=True, blank=True)
    End_time = models.TimeField(null=True, blank=True)
    Locked = models.BooleanField(default=False)
    TEACHER_PREF_STATUS_CHOICES = [
        ('R', 'Red'),
        ('G', 'Green'),
        ('Y', 'Yellow')
    ]
    Teacher_pref_status = models.CharField(max_length=1, choices=TEACHER_PREF_STATUS_CHOICES, blank=True, null=True)
    THEORY_OR_LAB_CHOICES = [
        ('lab', 'Lab'),
        ('theory', 'Theory')
    ]
    Theory_or_Lab = models.CharField(max_length=10, choices=THEORY_OR_LAB_CHOICES, blank=True, null=True)
    Hard_slot = models.BooleanField(default=False)

    def __str__(self):
        return f"TimetableDetail: Course={self.Course_ID.Course_name}, Tchr={self.Teacher_ID.Name}, Day={self.Day}"
