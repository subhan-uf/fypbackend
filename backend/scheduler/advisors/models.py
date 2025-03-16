from django.db import models
from users.models import Teacher, Room, Course, Batch, Section  

class Compensatory(models.Model):
    Compensatory_ID = models.AutoField(primary_key=True)
    Teacher_ID = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    Course_ID = models.ForeignKey(Course, on_delete=models.CASCADE)
    Room_ID = models.ForeignKey(Room, on_delete=models.CASCADE)
    Batch_ID = models.ForeignKey(Batch, on_delete=models.CASCADE)
    Date = models.DateField()
    Start_time = models.TimeField()
    End_time = models.TimeField()
    Status = models.CharField(max_length=50, blank=True, null=True)
    Desc = models.TextField(blank=True, null=True)
    Section_ID = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    # New field to store if the class is lab or theory
    Lab_or_Theory = models.CharField(
        max_length=10, 
        choices=[('lab', 'Lab'), ('theory', 'Theory')],
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"Compensatory: Tchr={self.Teacher_ID.Name}, Course={self.Course_ID.Course_name}, {self.Date}"

class CoursePreferenceConstraints(models.Model):
    Preference_ID = models.AutoField(primary_key=True)
    Course_ID = models.ForeignKey(Course, on_delete=models.CASCADE)

    Start_time = models.TimeField(null=True, blank=True)
    End_time = models.TimeField(null=True, blank=True)
    Status = models.CharField(max_length=50, blank=True, null=True)
    Teacher_ID = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    Section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    DAY_CHOICES = [
         ('Monday', 'Monday'),
         ('Tuesday', 'Tuesday'),
         ('Wednesday', 'Wednesday'),
         ('Thursday', 'Thursday'),
         ('Friday', 'Friday'),
         ('Saturday', 'Saturday'),

    ]
    Day = models.CharField(max_length=10, choices=DAY_CHOICES, null=True, blank=True)
    LAB_OR_THEORY_CHOICES = [
        ('lab', 'Lab'),
        ('theory', 'Theory'),
    ]
    Lab_or_Theory = models.CharField(max_length=10, choices=LAB_OR_THEORY_CHOICES)
    Multimedia_requirement = models.BooleanField(default=False)
    Speaker = models.BooleanField(default=False)
    Hard_constraint = models.BooleanField(default=False)

    def __str__(self):
        return f"Pref: {self.Teacher_ID.Name} - {self.Course_ID.Course_name} on {self.Day}"


class TeacherRoomPreference(models.Model):
    Room_Preference_ID = models.AutoField(primary_key=True)
    Teacher_ID = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    Floor = models.CharField(max_length=10, blank=True, null=True)


    def __str__(self):
        return f"TchrRoomPref: Tchr={self.Teacher_ID.Name}"
class Generation(models.Model):
    Generation_ID = models.AutoField(primary_key=True)
    Description = models.TextField(blank=True, null=True)
    Time_Generated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # For display purposes in admin or debugging.
        return f"Generation {self.Generation_ID}: {self.Description or 'No Description'}"

class TimetableHeader(models.Model):
    Timetable_ID = models.AutoField(primary_key=True)
    Batch_ID = models.ForeignKey(Batch, on_delete=models.CASCADE)
    Section_ID = models.ForeignKey(Section, on_delete=models.CASCADE)
    Generation = models.ForeignKey(Generation, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    disabled_days = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"TimetableHeader: Batch={self.Batch_ID.Batch_name}, Section={self.Section_ID.Section_name}"

class TimetableDetail(models.Model):
    Detail_ID = models.AutoField(primary_key=True)
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
        ('Y', 'Yellow'),
        ('H', 'Blue')
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
