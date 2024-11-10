
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken



class AdvisorLoginView(generics.GenericAPIView):
    serializer_class = AdvisorLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            advisor = serializer.validated_data['advisor']

            # Manually create a token without linking to Django User or OutstandingToken
            refresh = RefreshToken()
            refresh["advisor_id"] = advisor.id
            refresh["username"] = advisor.username
            refresh["faculty"] = advisor.faculty
            refresh["year"] = advisor.year

            access_token = str(refresh.access_token)

            return Response({
                'refresh': str(refresh),
                'access': access_token,
                'username': advisor.username,
                'faculty': advisor.faculty,
                'year': advisor.year,
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class TeacherPreferenceView(generics.GenericAPIView):
    serializer_class = TeacherPreferenceSerializer
    authentication_classes = [JWTAuthentication]  # Ensure JWT token is used for authentication
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def post(self, request, *args, **kwargs):
        # Retrieve teacher id from request data
        teacher_id = request.data.get('teacher_id')  # Assuming teacher_id is passed in request

        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

        preference, created = TeacherPreference.objects.get_or_create(teacher=teacher)

        # Serialize and validate data
        serializer = self.get_serializer(preference, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AdvisorLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can log out

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")

            # Validate if refresh token is provided
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()  # Adds token to the blacklist

            return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError:
            # If token is already blacklisted or invalid
            return Response({"error": "Token is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "An unexpected error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           