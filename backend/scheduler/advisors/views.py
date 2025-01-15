from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .serializers import (
    AdvisorLoginSerializer,
    CompensatorySerializer,
    CoursePreferenceConstraintsSerializer,
    TeacherRoomPreferenceSerializer,
    TimetableHeaderSerializer,
    TimetableDetailSerializer
)
from .models import (
    Compensatory,
    CoursePreferenceConstraints,
    TeacherRoomPreference,
    TimetableHeader,
    TimetableDetail
)
from users.models import Advisor


# ----------------------------------------------
#  ADVISOR LOGIN (untouched, except serializer)
# ----------------------------------------------
class AdvisorLoginView(generics.GenericAPIView):
    serializer_class = AdvisorLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            advisor = serializer.validated_data['advisor']

            # Manually create a token
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


# ----------------------------------------------
#  ADVISOR LOGOUT (untouched)
# ----------------------------------------------
class AdvisorLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError:
            return Response({"error": "Token is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "An unexpected error occurred. Please try again later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ----------------------------------------------
#  Base Generic Classes for Advisor
# ----------------------------------------------
class AdvisorBaseListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

class AdvisorBaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]


# ----------------------------------------------
#  Compensatory CRUD
# ----------------------------------------------
class CompensatoryListCreateView(AdvisorBaseListCreateView):
    queryset = Compensatory.objects.all()
    serializer_class = CompensatorySerializer

class CompensatoryRetrieveUpdateDestroyView(AdvisorBaseRetrieveUpdateDestroyView):
    queryset = Compensatory.objects.all()
    serializer_class = CompensatorySerializer


# ----------------------------------------------
#  CoursePreferenceConstraints CRUD
# ----------------------------------------------
class CoursePreferenceConstraintsListCreateView(AdvisorBaseListCreateView):
    queryset = CoursePreferenceConstraints.objects.all()
    serializer_class = CoursePreferenceConstraintsSerializer

class CoursePreferenceConstraintsRetrieveUpdateDestroyView(AdvisorBaseRetrieveUpdateDestroyView):
    queryset = CoursePreferenceConstraints.objects.all()
    serializer_class = CoursePreferenceConstraintsSerializer


# ----------------------------------------------
#  TeacherRoomPreference CRUD
# ----------------------------------------------
class TeacherRoomPreferenceListCreateView(AdvisorBaseListCreateView):
    queryset = TeacherRoomPreference.objects.all()
    serializer_class = TeacherRoomPreferenceSerializer

class TeacherRoomPreferenceRetrieveUpdateDestroyView(AdvisorBaseRetrieveUpdateDestroyView):
    queryset = TeacherRoomPreference.objects.all()
    serializer_class = TeacherRoomPreferenceSerializer


# ----------------------------------------------
#  TimetableHeader CRUD
# ----------------------------------------------
class TimetableHeaderListCreateView(AdvisorBaseListCreateView):
    queryset = TimetableHeader.objects.all()
    serializer_class = TimetableHeaderSerializer

class TimetableHeaderRetrieveUpdateDestroyView(AdvisorBaseRetrieveUpdateDestroyView):
    queryset = TimetableHeader.objects.all()
    serializer_class = TimetableHeaderSerializer


# ----------------------------------------------
#  TimetableDetail CRUD
# ----------------------------------------------
class TimetableDetailListCreateView(AdvisorBaseListCreateView):
    queryset = TimetableDetail.objects.all()
    serializer_class = TimetableDetailSerializer

class TimetableDetailRetrieveUpdateDestroyView(AdvisorBaseRetrieveUpdateDestroyView):
    queryset = TimetableDetail.objects.all()
    serializer_class = TimetableDetailSerializer
