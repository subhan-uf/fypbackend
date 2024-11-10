from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import *
from users.models import *
from django.contrib.auth import authenticate

class AdvisorLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('Must include "username" and "password".')

        # Manually fetch advisor and check password
        try:
            advisor = Advisor.objects.get(username=username)
            if not check_password(password, advisor.password):
                raise serializers.ValidationError("Invalid username or password.")
        except Advisor.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password.")

        # Add the advisor to validated data if authentication is successful
        attrs['advisor'] = advisor
        return attrs
    
    
    
    
    
class TeacherPreferenceSerializer(serializers.ModelSerializer):
        class Meta:
            model = TeacherPreference
            fields = '__all__'  # Or specify individual fields you want to expose, e.g., ['teacher', 'preferred_rooms', 'max_classes_per_day']

        def create(self, validated_data):
            # Custom behavior can be added here if needed
            return TeacherPreference.objects.create(**validated_data)

        def update(self, instance, validated_data):
            # Custom update logic if required
            instance.preferred_rooms.set(validated_data.get('preferred_rooms', instance.preferred_rooms.all()))
            instance.max_classes_per_day = validated_data.get('max_classes_per_day', instance.max_classes_per_day)
            instance.health_limitations = validated_data.get('health_limitations', instance.health_limitations)
            instance.preferred_subjects.set(validated_data.get('preferred_subjects', instance.preferred_subjects.all()))
            instance.locked_schedule_slots = validated_data.get('locked_schedule_slots', instance.locked_schedule_slots)
            instance.unavailable_days = validated_data.get('unavailable_days', instance.unavailable_days)
            instance.save()
            return instance