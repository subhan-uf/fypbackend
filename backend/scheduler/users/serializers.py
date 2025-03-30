from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

from .models import (
    CustomUser, DEO, Advisor, Chairman, Department, Year,
    Batch, Section, Teacher, Room, Course,
    TeacherCourseAssignment, BatchCourseTeacherAssignment
)

class AdvisorCreateSerializer(serializers.ModelSerializer):
    # Include user fields from the CustomUser model via the related 'user' field
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    password = serializers.CharField(source='user.password', write_only=True)
    phone_number = serializers.CharField(source='user.phone_number')
    staff_id = serializers.CharField(source='user.staff_id')
    
    # Advisor-specific fields
    year = serializers.ChoiceField(choices=Advisor.YearChoices.choices, allow_blank=True, allow_null=True)
    faculty = serializers.CharField(allow_blank=True, allow_null=True)
    seniority = serializers.ChoiceField(choices=Advisor.SeniorityChoices.choices, allow_blank=True, allow_null=True)
    profile_pic = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Advisor
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password',
            'phone_number', 'staff_id', 'year', 'faculty', 'seniority', 'profile_pic'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        # Create the CustomUser with role 'advisor'
        user = CustomUser.objects.create(**user_data, role='advisor')
        user.set_password(password)
        user.save()
        # Check if an advisor already exists (it might have been auto-created by the signal)
        if hasattr(user, 'advisor_profile'):
            # Update existing advisor if needed
            advisor = user.advisor_profile
            for attr, value in validated_data.items():
                setattr(advisor, attr, value)
            advisor.save()
        else:
            advisor = Advisor.objects.create(user=user, **validated_data)
        return advisor


    def update(self, instance, validated_data):
        # Update nested user fields
        user_data = validated_data.pop('user', {})
        user = instance.user
        for attr, value in user_data.items():
            if attr == 'password':
                user.set_password(value)
            else:
                setattr(user, attr, value)
        user.save()
        # Update Advisor fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class AdvisorLoginSerializer(serializers.Serializer):
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
        if getattr(user, 'role', None) != 'advisor':
            raise serializers.ValidationError('Access denied. Only users with Advisor role can log in.')
        attrs['user'] = user
        return attrs
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



class AdvisorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    phone_number = serializers.CharField(source='user.phone_number')
    staff_id = serializers.CharField(source='user.staff_id')

    class Meta:
        model = Advisor
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'staff_id',
            'profile_pic',
            'year',
            'faculty',
            'seniority',
            'deo'
        ]


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
        fields = ['Batch_ID', 'Discipline', 'Batch_name', 'Year']


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
             'Course_ID', 'Course_name','Course_fullname' ,'Course_code', 'Batch_ID',
            'Max_classes_per_day', 'Credit_hours', 'Course_desc', 'Is_Lab'
        ]


class TeacherCourseAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherCourseAssignment
        fields = ['Assignment_ID', 'Teacher_ID', 'Course_ID', 'Teacher_type']


class BatchCourseTeacherAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchCourseTeacherAssignment
        fields = ['Assignment_ID', 'Batch_ID', 'Course_ID', 'Teacher_ID', 'Course_type', 'Section']
