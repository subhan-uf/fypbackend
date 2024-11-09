from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('deo', 'DEO'),
        ('advisor', 'Advisor'),
        ('chairman', 'Chairman'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    staff_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    





class DEO(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department_name = models.CharField(max_length=100)

    @classmethod
    def create_with_user(cls, username, email, password, first_name, last_name, staff_id, department_name):
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='deo',
            first_name=first_name,
            last_name=last_name,
            staff_id=staff_id,
            department_name=department_name
        )
        return cls.objects.create(user=user, department_name=department_name)
    




class Advisor(models.Model):
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

    username = models.CharField(max_length=150, unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    password = models.CharField(max_length=128)  # Store the hashed password
    year = models.CharField(max_length=10, choices=YearChoices.choices)
    faculty = models.CharField(max_length=100)
    seniority = models.CharField(max_length=20, choices=SeniorityChoices.choices)
    deo = models.ForeignKey('DEO', on_delete=models.CASCADE, related_name='advisors')  # Link to the DEO

    def save(self, *args, **kwargs):
        # Automatically hash the password before saving if it's a new instance
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.faculty} Advisor ({self.year})"







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






# Department model for managing different departments in the institution
class Department(models.Model):
    name = models.CharField(max_length=100)  # Department name
    chairman = models.ForeignKey('Chairman', on_delete=models.SET_NULL, null=True, related_name='head_of_department')  # Department chairman

    def __str__(self):
        return self.name






# Academic year model to represent different academic years
class Year(models.Model):
    academic_year = models.PositiveIntegerField()  # Academic year number
    academic_start = models.DateField()  # Start date of the academic year
    academic_end = models.DateField()  # End date of the academic year

    def __str__(self):
        return str(self.academic_year)



# Batch model to represent different batches in an academic year
class Batch(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)  # Linking to the Year model
    batch_id = models.CharField(max_length=10)  # Unique batch identifier

    def __str__(self):
        return f"{self.year} - {self.batch_id}"





# Section model to represent sections within batches
class Section(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)  # Linking to the Batch model
    section_id = models.CharField(max_length=1)  # Section identifier (e.g., A, B, C)
    students_count = models.PositiveIntegerField()  # Number of students in the section

    def __str__(self):
        return f"{self.batch} - Section {self.section_id}"






# Equipment model to represent various equipment available
class Equipment(models.Model):
    projector = models.BooleanField(default=False)  # Projector availability
    speaker = models.BooleanField(default=False)  # Speaker availability
    pc_connection = models.BooleanField(default=False)  # PC connection availability
    wifi = models.BooleanField(default=False)  # Wi-Fi availability

    def __str__(self):
        return f"Equipment: Projector={self.projector}, Speaker={self.speaker}, PC Connection={self.pc_connection}, WiFi={self.wifi}"






# Room model representing classrooms with associated equipment
class Room(models.Model):
    floor = models.PositiveIntegerField()  # Floor number
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # Linked department
    max_std_limit = models.PositiveIntegerField()  # Maximum student capacity
    room_no = models.CharField(max_length=10)  # Room number
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True)  # Linked equipment
    room_type = models.CharField(max_length=20)# room type 
    def __str__(self):
        return f"Room {self.room_no} on Floor {self.floor}"







# Lab model representing specialized labs with associated equipment
class Lab(models.Model):
    floor = models.PositiveIntegerField()  # Floor number
    lab_no = models.CharField(max_length=10)  # Lab number
    max_capacity = models.PositiveIntegerField()  # Maximum capacity
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # Linked department
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True)  # Linked equipment

    def __str__(self):
        return f"Lab {self.lab_no} on Floor {self.floor}"









# Course model representing different courses offered
class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)  # Unique course code
    title = models.CharField(max_length=100)  # Course title
    theory_hours = models.PositiveIntegerField()  # Number of theory hours
    practical_hours = models.PositiveIntegerField()  # Number of practical hours
    credit_hours = models.PositiveIntegerField()  # Total credit hours
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # Linked department
    year = models.ForeignKey(Year, on_delete=models.CASCADE)  # Linked academic year
    batches = models.ManyToManyField(Batch, related_name='courses')  # Batches associated with the course

    def save(self, *args, **kwargs):
        # Automatically calculate credit hours before saving
        self.credit_hours = self.theory_hours + self.practical_hours
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.course_code})"








# Teacher model representing faculty members
class Teacher(models.Model):
    name = models.CharField(max_length=100)  # Teacher's name
    email = models.EmailField(unique=True)  # Unique email address
    nic = models.CharField(max_length=20, unique=True)  # Unique NIC (National ID)
    faculty = models.CharField(max_length=100)  # Faculty name
    courses = models.ManyToManyField(Course, related_name='teachers')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # Linked department
    designation = models.CharField(max_length=50, choices=[
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('lecturer', 'Lecturer'),
        ('chairman', 'Chairman'),
    ])
    
  
    def __str__(self):
        return f"{self.name} ({self.designation})"
    










    