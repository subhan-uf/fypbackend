from rest_framework import serializers
from .models import * 
from django.contrib.auth import authenticate

from django.contrib.auth.hashers import check_password


#

# serializer to vaildate data in json form 
#

class DEOLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('Must include "username" and "password".')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid username or password.')

        # Check if the user has a role attribute and if it's 'deo'
        if not hasattr(user, 'role') or user.role != 'deo':
            raise serializers.ValidationError('Access denied. Only DEO users can log in.')

        attrs['user'] = user
        return attrs
    




class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ['id', 'username', 'profile_pic', 'year', 'faculty', 'seniority', 'deo']
      

    def validate_username(self, value):
        if Advisor.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def create(self, validated_data):
        try:
            advisor = Advisor.objects.create(**validated_data)
            return advisor
        except Exception as e:
            raise serializers.ValidationError(f'Failed to create advisor: {str(e)}')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = password  # Assume hashing is handled in the model's save method

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        try:
            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError(f'Failed to update advisor: {str(e)}')
    







class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'chairman']
    
    def create(self, validated_data):
        department = Department(**validated_data)
        department.save()
        return department
        
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
        



class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ['id', 'academic_year', 'academic_start','academic_end']
    
    def create(self, validated_data):
        year = Year(**validated_data)
        year.save()
        return year
        
    def  update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
        




class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id', 'year', 'batch_id']

    def create(self, validated_data):
        batch = Batch(**validated_data)
        batch.save()
        return batch
        
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
     


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id','batch', 'section_id', 'students_count']

    def create(self, validated_data):
        section = Section(**validated_data)
        section.save()
        return section
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
        
    




class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'projector', 'speaker', 'pc_connection', 'wifi']

    def create(self, validated_data):
        equipment = Equipment(**validated_data)
        equipment.save()
        return equipment
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
        

class ChairmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chairman
        fields = ['id', 'department']  



class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_no', 'room_type', 'floor', 'department','max_std_limit','equipment']
    def create(self, validated_data):
        room = Room(**validated_data)
        room.save()
        return room
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ['id', 'floor', 'lab_no', 'max_capacity', 'department','equipment']

    def create(self, validated_data):
        lab = Lab(**validated_data)
        lab.save()
        return lab
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
        

    


class CourseSerializer(serializers.ModelSerializer):
    credit_hours = serializers.IntegerField(read_only=True)  # Make credit_hours read-only

    class Meta:
        model = Course
        fields = ['id', 'course_code', 'title', 'theory_hours', 'practical_hours', 'credit_hours', 'department', 'year', 'batches']
        
    def create(self, validated_data):
        # Pop batches from validated_data because we need to set it after saving the course
        batches_data = validated_data.pop('batches', [])
        
        # Create the Course instance
        course = Course.objects.create(**validated_data)
        
        # Assign the many-to-many batches relationship
        course.batches.set(batches_data)
        
        return course

    def update(self, instance, validated_data):
        # Pop batches from validated_data so it can be handled separately
        batches_data = validated_data.pop('batches', None)
        
        # Update the remaining fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()

        # Update batches if provided
        if batches_data is not None:
            instance.batches.set(batches_data)
        
        return instance


class TeacherSerializer(serializers.ModelSerializer):
    # Define the courses field, so it can be serialized
    courses = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True)
    
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'email', 'nic', 'faculty', 'department', 'designation', 'courses']
    
    def create(self, validated_data):
        # Handling the many-to-many relationship during creation
        courses_data = validated_data.pop('courses', [])
        teacher = Teacher(**validated_data)
        teacher.save()
        
        # Add courses to the teacher after saving
        teacher.courses.set(courses_data)
        return teacher
    
    def update(self, instance, validated_data):
        courses_data = validated_data.pop('courses', None)
        
        # Update teacher fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # If courses data exists, update it
        if courses_data is not None:
            instance.courses.set(courses_data)  # Using set() to properly update many-to-many relationships
        
        instance.save()
        return instance