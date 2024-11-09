from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import Advisor
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