from rest_framework import serializers
from django.contrib.auth.hashers import check_password

from users.models import Advisor
from .models import (
    Compensatory,
    CoursePreferenceConstraints,
    TeacherRoomPreference,
    TimetableHeader,
    TimetableDetail,
    Generation
)


class AdvisorLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('Must include "username" and "password".')

        try:
            advisor = Advisor.objects.get(username=username)
            if not check_password(password, advisor.password):
                raise serializers.ValidationError("Invalid username or password.")
        except Advisor.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password.")

        attrs['advisor'] = advisor
        return attrs



class CompensatorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Compensatory
        fields = '__all__'


class CoursePreferenceConstraintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursePreferenceConstraints
        fields = '__all__'


class TeacherRoomPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherRoomPreference
        fields = '__all__'


class TimetableHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimetableHeader
        fields = '__all__'


class TimetableDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimetableDetail
        fields = '__all__'
class GenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generation
        fields = '__all__'