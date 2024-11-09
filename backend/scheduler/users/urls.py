from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import DEOLoginView,AdvisorListCreateView, AdvisorRetrieveUpdateDestroyView,DEOLogoutView
from .views import * 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('login/deo/', DEOLoginView.as_view(), name='deo-login'),
    path('advisors/', AdvisorCreateandGetAPI.as_view(), name='advisor-list-create'),
    path('advisors/<int:pk>/', AdvisorUpdateDestroyAPI.as_view(), name='advisor-detail'),
    path('years/', YearListCreateView.as_view(), name='year-list-create'),
    path('years/<int:pk>/', YearRetrieveUpdateDestroyView.as_view(), name='year-detail-update-delete'),
    path('batches/', BatchListCreateView.as_view(), name='batch-list-create'),
    path('batches/<int:pk>/', BatchRetrieveUpdateDestroyView.as_view(), name='batch-detail-update-delete'),
    path('sections/', SectionListCreateView.as_view(), name='section-list-create'),
    path('sections/<int:pk>/', SectionRetrieveUpdateDestroyView.as_view(), name='section-detail-update-delete'),
    path('equipment/', EquipmentListCreateView.as_view(), name='equipment-list-create'),
    path('equipment/<int:pk>/', EquipmentRetrieveUpdateDestroyView.as_view(), name='equipment-detail'),
    path('rooms/', RoomListCreateView.as_view(), name='room-list-create'),  
    path('rooms/<int:pk>/', RoomRetrieveUpdateDestroyView.as_view(), name='room-detail'), 
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),  
    path('departments/<int:pk>/', DepartmentRetrieveUpdateDestroyView.as_view(), name='department-detail'),  
    path('chairman/', ChairmanListView.as_view(), name='chairman-list'),
    path('labs/', LabListCreateView.as_view(), name='lab-list-create'),
    path('labs/<int:pk>/', LabRetrieveUpdateDestroyView.as_view(), name='lab-retrieve-update-destroy'),
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyView.as_view(), name='course-retrieve-update-destroy'),
    path('teachers/', TeacherListCreateView.as_view(), name='teacher-list-create'),
    path('teachers/<int:pk>/', TeacherRetrieveUpdateDestroyView.as_view(), name='teacher-detail'),
      
    path('logout/deo/', DEOLogoutView.as_view(), name='logout'),
]



# http://127.0.0.1:8000/api/login/deo/
# http://127.0.0.1:8000/api/advisors/
# http://127.0.0.1:8000/api/advisors/
# http://127.0.0.1:8000/api/advisors/2/
# http://127.0.0.1:8000/api/advisors/1/
# http://127.0.0.1:8000/api/logout/deo/