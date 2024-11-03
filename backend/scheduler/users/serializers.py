from rest_framework import serializers
# from .models import CustomUser, Advisor, DEO, Chairman,Teacher,Course
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

        # Check if the user has a role attribute
        if not hasattr(user, 'role'):
            raise serializers.ValidationError('User does not have a role attribute.')

        attrs['user'] = user
        return attrs
    




class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ['id', 'username', 'profile_pic', 'year', 'faculty', 'seniority']

    def create(self, validated_data):
        # We don't need to hash the password here since it's handled in the model
        advisor = Advisor(**validated_data)
        advisor.save()
        return advisor

    def update(self, instance, validated_data):
        # Optionally update the password if provided
        password = validated_data.pop('password', None)
        if password:
            instance.password = password  # Password will be hashed in the model's save method

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    







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
        fields = ['id', 'section_id', 'students_count']

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
    class Meta:
        model = Course
        fields = ['id', 'course_code', 'title', 'theory_hours', 'practical_hours','credit_hours','department','year','batches']
        
    def create(self, validated_data):
        course = Course(**validated_data)
        course.save()
        return course
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance






class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'username', 'profile_pic', 'year', 'faculty', 'position', 'department']
    
    def create(self, validated_data):
        teacher = Teacher(**validated_data)
        teacher.save()
        return teacher
    
    def update(self, instance, validated_data):
    
        password = validated_data.pop('password', None)
        if password:
            instance.password = password 
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    