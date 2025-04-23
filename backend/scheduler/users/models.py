from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
logger = logging.getLogger(__name__)

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('deo', 'DEO'),
        ('advisor', 'Advisor'),
        ('chairman', 'Chairman'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    staff_id = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15, blank=True, null=True)


class DEO(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department_name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.user.username
    @classmethod
    def create_with_user(cls, username, email, password, first_name, last_name, staff_id, department_name):
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='deo',
            first_name=first_name,
            last_name=last_name,
            staff_id=staff_id
        )
        return cls.objects.create(user=user, department_name=department_name)


# Replace your current Advisor model with the following:
class Advisor(models.Model):
    """
    Advisor profile model.
    This model stores advisor-specific information and links to the CustomUser
    which handles authentication.
    """
    class YearChoices(models.TextChoices):
        FIRST = 'first', 'First'
        SECOND = 'second', 'Second'
        THIRD = 'third', 'Third'
        FOURTH = 'fourth', 'Fourth'

    class SeniorityChoices(models.TextChoices):
        PROFESSOR = 'professor', 'Professor'
        ASSOCIATE_PROFESSOR = 'associate_professor', 'Associate Professor'
        ASSISTANT_PROFESSOR = 'assistant_professor', 'Assistant Professor'
        LECTURER = 'lecturer', 'Lecturer'
        IT_MANAGER_SR = 'it_manager_sr', 'IT Manager (Sr)'
        IT_MANAGER_JR = 'it_manager_jr', 'IT Manager (Jr)'

    # Link to the CustomUser
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='advisor_profile')
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    year = models.CharField(max_length=10, choices=YearChoices.choices, blank=True, null=True)
    faculty = models.CharField(max_length=100, blank=True, null=True)
    seniority = models.CharField(max_length=20, choices=SeniorityChoices.choices, blank=True, null=True)
    deo = models.ForeignKey('DEO', on_delete=models.CASCADE, related_name='advisors', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Advisor ({self.year})"


class Chairman(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)

    @classmethod
    def create_with_user(cls, username, email, password, first_name, last_name, staff_id, department, phone_number):
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='chairman',
            first_name=first_name,
            last_name=last_name,
            staff_id=staff_id,
            phone_number=phone_number
        )
        return cls.objects.create(user=user, department=department)


class Department(models.Model):
    name = models.CharField(max_length=100)
    chairman = models.ForeignKey('Chairman', on_delete=models.SET_NULL, null=True, related_name='head_of_department')

    def __str__(self):
        return self.name


class Year(models.Model):
    academic_year = models.PositiveIntegerField()
    academic_start = models.DateField()
    academic_end = models.DateField()

    def __str__(self):
        return str(self.academic_year)



class Batch(models.Model):
    Batch_ID = models.AutoField(primary_key=True)
    Discipline = models.CharField(max_length=50)
    Batch_name = models.CharField(max_length=100, unique=True)
    Year = models.IntegerField()

    def __str__(self):
        return f"{self.Batch_name} (Year: {self.Year})"


class Section(models.Model):
    Section_ID = models.AutoField(primary_key=True)
    Batch_ID = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='sections')
    Section_name = models.CharField(max_length=50)
    Max_students = models.PositiveIntegerField()
    Max_gaps = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.Section_name} (Batch: {self.Batch_ID.Batch_name})"


class Teacher(models.Model):
    Teacher_ID = models.CharField(primary_key=True)
    Name = models.CharField(max_length=100)
    NIC = models.CharField(max_length=20, unique=True)
    Email = models.EmailField(unique=True)
    Phone = models.CharField(max_length=15, null=True, blank=True)
    Max_classes = models.PositiveIntegerField(null=True, blank=True)
    Health_limitation = models.CharField(max_length=255, null=True, blank=True)
    Seniority = models.CharField(max_length=50, null=True, blank=True)
    Teacher_type = models.CharField(max_length=50)  # e.g. "Permanent", "Visiting", etc.

    def __str__(self):
        return self.Name


class Room(models.Model):
    Room_ID = models.AutoField(primary_key=True)
    Room_no = models.CharField(max_length=50)
    Max_capacity = models.PositiveIntegerField()
    Floor = models.IntegerField()
    Room_type = models.CharField(max_length=100)
    Multimedia = models.BooleanField(default=False)
    Speaker = models.BooleanField(default=False)
    ROOM_STATUS_CHOICES = [
        ('enable', 'Enable'),
        ('disable', 'Disable')
    ]
    Room_status = models.CharField(max_length=7, choices=ROOM_STATUS_CHOICES, default='enable')

    def __str__(self):
        return f"Room {self.Room_no}"


class Course(models.Model):
    Course_ID = models.AutoField(primary_key=True)
    Course_name = models.CharField(max_length=100)
    Course_fullname = models.CharField(max_length=500)
    Course_code = models.CharField(max_length=20)
    Batch_ID = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='courses')
    Max_classes_per_day = models.PositiveIntegerField()
    Credit_hours = models.PositiveIntegerField()
    Course_desc = models.TextField(null=True, blank=True)
    Is_Lab = models.BooleanField(default=False)
    def __str__(self):
        return self.Course_name


class TeacherCourseAssignment(models.Model):
    Assignment_ID = models.AutoField(primary_key=True)
    Teacher_ID = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_assignments')
    Course_ID = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_assignments')
    TEACHER_TYPE_CHOICES = [
        ('lab', 'Lab'),
        ('theory', 'Theory')
    ]
    Teacher_type = models.CharField(max_length=10, choices=TEACHER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.Teacher_ID.Name} -> {self.Course_ID.Course_name}"


class BatchCourseTeacherAssignment(models.Model):
    Assignment_ID = models.AutoField(primary_key=True)
    Batch_ID = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='batch_course_teacher_assignments')
    Course_ID = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batch_course_teacher_assignments')
    Teacher_ID = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='batch_course_teacher_assignments')
    Course_type= models.CharField(max_length=100)
    Section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, related_name='batch_course_teacher_assignments')


    def __str__(self):
        section_name = self.Section.Section_name if self.Section else "No Section"
        return f"Batch={self.Batch_ID.Batch_name}, Course={self.Course_ID.Course_name}, Teacher={self.Teacher_ID.Name}, Section={self.Section}"


@receiver(post_save, sender=CustomUser)
def create_related_profile(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Signal fired for user: {instance.username} with role: {instance.role}")
        # Or temporarily use:
        # print(f"Signal fired for user: {instance.username} with role: {instance.role}")
        if instance.role == 'deo':
            DEO.objects.create(user=instance, department_name='')
        elif instance.role == 'advisor':
            Advisor.objects.create(user=instance, year='', faculty='', seniority='', deo=None)