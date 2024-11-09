from rest_framework import viewsets,status
from .models import  *
from .serializers import  *
from rest_framework import generics,permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken

import logging
logger = logging.getLogger(__name__)




#  """ Only a deo can log in.
#     The deo (data entry operator) login view.
#         """

class DEOLoginView(generics.GenericAPIView):
    serializer_class = DEOLoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']

            # Check if the user's role is 'deo'
            if user.role != 'deo':
                return Response({
                    'error': 'Access denied. Only users with DEO role can log in.'
                }, status=status.HTTP_403_FORBIDDEN)

            # Create tokens
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)

            return Response({
                'refresh': str(refresh),
                'access': access,
                'username': user.username,
                'role': user.role
            }, status=status.HTTP_200_OK)

        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class AdvisorCreateandGetAPI(generics.ListCreateAPIView):
    serializer_class = AdvisorSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only allow authenticated users

    def get_queryset(self):
        # Return all advisors
        return Advisor.objects.all()

    def list(self, request, *args, **kwargs):
        advisors = self.get_queryset()
        serializer = self.get_serializer(advisors, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'message': 'Advisors retrieved successfully.'
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        deo_username = request.data.get('deo_username')
        try:
            deo = DEO.objects.get(user__username=deo_username)
        except DEO.DoesNotExist:
            return Response({
            'status': 'error',
            'message': 'DEO with the provided username does not exist.'
            }, status=status.HTTP_400_BAD_REQUEST)

    # Inject DEO ID
        request.data['deo'] = deo.id

        serializer = AdvisorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({
            'status': 'error',
            'message': 'Invalid data',
            'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
class AdvisorUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            advisor = self.get_object()
            serializer = self.get_serializer(advisor)
            return Response({
                'status': 'success',
                'data': serializer.data,
                'message': 'Advisor retrieved successfully.'
            }, status=status.HTTP_200_OK)
        except Advisor.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Advisor not found.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Failed to retrieve advisor: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        advisor = self.get_object()
        serializer = self.get_serializer(advisor, data=request.data, partial=True)

        if serializer.is_valid():
            try:
                # You can add password handling logic if needed here
                updated_advisor = serializer.save()
                return Response({
                    'status': 'success',
                    'data': AdvisorSerializer(updated_advisor).data,
                    'message': 'Advisor updated successfully.'
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'status': 'error',
                    'message': f'Failed to update advisor: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'status': 'error',
                'errors': serializer.errors,
                'message': 'Validation failed for advisor update.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            advisor = self.get_object()
            advisor.delete()
            return Response({
                'status': 'success',
                'message': 'Advisor deleted successfully.'
            }, status=status.HTTP_204_NO_CONTENT)
        except Advisor.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Advisor not found.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Failed to delete advisor: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class TeacherListCreateView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def list(self, request, *args, **kwargs):
        teachers = self.get_queryset()
        serializer = self.get_serializer(teachers, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'message': 'Teachers retrieved successfully.'
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save()
        return Response({
            'status': 'success',
            'data': TeacherSerializer(teacher).data,
            'message': 'Teacher created successfully.'
        }, status=status.HTTP_201_CREATED)





class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'message': 'Teacher retrieved successfully.'
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save()
        return Response({
            'status': 'success',
            'data': TeacherSerializer(teacher).data,
            'message': 'Teacher updated successfully.'
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': 'success',
            'message': 'Teacher deleted successfully.'
        }, status=status.HTTP_204_NO_CONTENT)


class BaseListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            items = self.get_queryset()
            serializer = self.get_serializer(items, many=True)
            logger.info(f'{self.__class__.__name__}: Retrieved {len(serializer.data)} items.')
            return Response({
                'status': 'success',
                'data': serializer.data,
                'message': f'{self.__class__.__name__.replace("View", "")}s retrieved successfully.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Error retrieving items in {self.__class__.__name__}: {str(e)}')
            return Response({
                'status': 'error',
                'message': 'Failed to retrieve items.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                item = serializer.save()
                logger.info(f'{self.__class__.__name__}: Created {item}.')
                return Response({
                    'status': 'success',
                    'data': serializer.data,
                    'message': f'{self.__class__.__name__.replace("View", "")} created successfully.'
                }, status=status.HTTP_201_CREATED)
            else:
                logger.warning(f'{self.__class__.__name__}: Validation errors: {serializer.errors}.')
                return Response({
                    'status': 'error',
                    'errors': serializer.errors,
                    'message': f'Failed to create {self.__class__.__name__.replace("View", "").lower()}.'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error creating item in {self.__class__.__name__}: {str(e)}')
            return Response({
                'status': 'error',
                'message': 'Failed to create item.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            logger.info(f'{self.__class__.__name__}: Retrieved {instance}.')
            return Response({
                'status': 'success',
                'data': serializer.data,
                'message': f'{self.__class__.__name__.replace("View", "")} retrieved successfully.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Error retrieving item in {self.__class__.__name__}: {str(e)}')
            return Response({
                'status': 'error',
                'message': 'Failed to retrieve item.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                item = serializer.save()
                logger.info(f'{self.__class__.__name__}: Updated {item}.')
                return Response({
                    'status': 'success',
                    'data': serializer.data,
                    'message': f'{self.__class__.__name__.replace("View", "")} updated successfully.'
                }, status=status.HTTP_200_OK)
            else:
                logger.warning(f'{self.__class__.__name__}: Validation errors: {serializer.errors}.')
                return Response({
                    'status': 'error',
                    'errors': serializer.errors,
                    'message': f'Failed to update {self.__class__.__name__.replace("View", "").lower()}.'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error updating item in {self.__class__.__name__}: {str(e)}')
            return Response({
                'status': 'error',
                'message': 'Failed to update item.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            logger.info(f'{self.__class__.__name__}: Deleted {instance}.')
            return Response({
                'status': 'success',
                'message': f'{self.__class__.__name__.replace("View", "")} deleted successfully.'
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f'Error deleting item in {self.__class__.__name__}: {str(e)}')
            return Response({
                'status': 'error',
                'message': 'Failed to delete item.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


# Department Views
class DepartmentListCreateView(BaseListCreateView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class DepartmentRetrieveUpdateDestroyView(BaseRetrieveUpdateDestroyView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


# Year Views
class YearListCreateView(BaseListCreateView):
    queryset = Year.objects.all()
    serializer_class = YearSerializer
    permission_classes = [permissions.IsAuthenticated]


class YearRetrieveUpdateDestroyView(BaseRetrieveUpdateDestroyView):
    queryset = Year.objects.all()
    serializer_class = YearSerializer
    permission_classes = [permissions.IsAuthenticated]


# Batch Views
class BatchListCreateView(BaseListCreateView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]


class BatchRetrieveUpdateDestroyView(BaseRetrieveUpdateDestroyView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]


# Section Views
class SectionListCreateView(BaseListCreateView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]


class SectionRetrieveUpdateDestroyView(BaseRetrieveUpdateDestroyView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]


# Equipment Views
class EquipmentListCreateView(BaseListCreateView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class EquipmentRetrieveUpdateDestroyView(BaseRetrieveUpdateDestroyView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]


# Room Views
class RoomListCreateView(BaseListCreateView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoomRetrieveUpdateDestroyView(BaseRetrieveUpdateDestroyView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChairmanListView(generics.ListAPIView):
    queryset = Chairman.objects.all()
    serializer_class = ChairmanSerializer


# Lab Views
class LabListCreateView(BaseListCreateView):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer
    permission_classes = [permissions.IsAuthenticated]


class LabRetrieveUpdateDestroyView(BaseRetrieveUpdateDestroyView):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer
    permission_classes = [permissions.IsAuthenticated]


# Course Views
class CourseListCreateView(BaseListCreateView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseRetrieveUpdateDestroyView(BaseRetrieveUpdateDestroyView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

class TeacherListCreateView(BaseListCreateView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherRetrieveUpdateDestroyView(BaseRetrieveUpdateDestroyView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

















class DEOLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Extract the refresh token from the request data
            refresh_token = request.data.get('refresh_token')

            if not refresh_token:
                return Response({"error": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the token using the RefreshToken class
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)