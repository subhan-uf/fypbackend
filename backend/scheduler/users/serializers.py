from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

from .models import (
    CustomUser, DEO, Advisor, Chairman, Department, Year,
    Batch, Section, Teacher, Room, Course,
    TeacherCourseAssignment, BatchCourseTeacherAssignment
)


# -----------------------------------------------------------------------------
#  DEO LOGIN SERIALIZER (unchanged)
# -----------------------------------------------------------------------------
class DEOLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('Must include "username" and "password".')

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid username or password.')

        if getattr(user, 'role', None) != 'deo':
            raise serializers.ValidationError('Access denied. Only DEO users can log in.')

        attrs['user'] = user
        return attrs


# -----------------------------------------------------------------------------
#  ADVISOR SERIALIZER (kept if needed by other code)
# -----------------------------------------------------------------------------
class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ['id', 'username', 'profile_pic', 'year', 'faculty', 'seniority', 'deo']


# -----------------------------------------------------------------------------
#  DEPARTMENT, YEAR, ETC. SERIALIZERS
# -----------------------------------------------------------------------------
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'chairman']


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ['id', 'academic_year', 'academic_start','academic_end']


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['Batch_ID', 'Batch_name', 'Year']


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['Section_ID', 'Batch_ID', 'Section_name', 'Max_students', 'Max_gaps']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
          'Teacher_ID', 'Name', 'NIC', 'Email', 'Phone',
            'Max_classes', 'Health_limitation', 'Seniority', 'Teacher_type'
        ]


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'Room_ID', 'Room_no', 'Max_capacity', 'Floor',
            'Room_type', 'Multimedia', 'Speaker', 'Room_status'
        ]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
             'Course_ID', 'Course_name', 'Course_code', 'Batch_ID',
            'Max_classes_per_day', 'Credit_hours', 'Course_desc', 'Is_Lab'
        ]


class TeacherCourseAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherCourseAssignment
        fields = ['Assignment_ID', 'Teacher_ID', 'Course_ID', 'Teacher_type']


class BatchCourseTeacherAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchCourseTeacherAssignment
        fields = ['Assignment_ID', 'Batch_ID', 'Course_ID', 'Teacher_ID', 'Course_type']
