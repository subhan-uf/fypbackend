# users/urls.py
from django.urls import path
from .views import (
    DEOLoginView, DEOLogoutView,
    DepartmentListCreateView, DepartmentRetrieveUpdateDestroyView,
    YearListCreateView, YearRetrieveUpdateDestroyView,
    BatchListCreateView, BatchRetrieveUpdateDestroyView,
    SectionListCreateView, SectionRetrieveUpdateDestroyView,
    TeacherListCreateView, TeacherRetrieveUpdateDestroyView,
    RoomListCreateView, RoomRetrieveUpdateDestroyView,
    CourseListCreateView, CourseRetrieveUpdateDestroyView,
    TeacherCourseAssignmentListCreateView, TeacherCourseAssignmentRetrieveUpdateDestroyView,
    BatchCourseTeacherAssignmentListCreateView, BatchCourseTeacherAssignmentRetrieveUpdateDestroyView
)

urlpatterns = [
    # DEO Auth
    path('deo/login/', DEOLoginView.as_view(), name='deo-login'),
    path('deo/logout/', DEOLogoutView.as_view(), name='deo-logout'),

    # Department
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentRetrieveUpdateDestroyView.as_view(), name='department-detail'),

    # Year
    path('years/', YearListCreateView.as_view(), name='year-list-create'),
    path('years/<int:pk>/', YearRetrieveUpdateDestroyView.as_view(), name='year-detail'),

    # Batch
    path('batches/', BatchListCreateView.as_view(), name='batch-list-create'),
    path('batches/<int:pk>/', BatchRetrieveUpdateDestroyView.as_view(), name='batch-detail'),

    # Section
    path('sections/', SectionListCreateView.as_view(), name='section-list-create'),
    path('sections/<int:pk>/', SectionRetrieveUpdateDestroyView.as_view(), name='section-detail'),

    # Teacher
    path('teachers/', TeacherListCreateView.as_view(), name='teacher-list-create'),
    path('teachers/<int:pk>/', TeacherRetrieveUpdateDestroyView.as_view(), name='teacher-detail'),

    # Room
    path('rooms/', RoomListCreateView.as_view(), name='room-list-create'),
    path('rooms/<int:pk>/', RoomRetrieveUpdateDestroyView.as_view(), name='room-detail'),

    # Course
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyView.as_view(), name='course-detail'),

    # TeacherCourseAssignment
    path('teacher-course-assignments/', TeacherCourseAssignmentListCreateView.as_view(), name='tca-list-create'),
    path('teacher-course-assignments/<int:pk>/', TeacherCourseAssignmentRetrieveUpdateDestroyView.as_view(), name='tca-detail'),

    # BatchCourseTeacherAssignment
    path('batch-course-teacher-assignments/', BatchCourseTeacherAssignmentListCreateView.as_view(), name='bcta-list-create'),
    path('batch-course-teacher-assignments/<int:pk>/', BatchCourseTeacherAssignmentRetrieveUpdateDestroyView.as_view(), name='bcta-detail'),
]
