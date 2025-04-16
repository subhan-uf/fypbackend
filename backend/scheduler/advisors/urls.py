# advisor/urls.py
from django.urls import path
from .views import (
    AdvisorLoginView, AdvisorLogoutView,
    CompensatoryListCreateView, CompensatoryRetrieveUpdateDestroyView,
    CoursePreferenceConstraintsListCreateView, CoursePreferenceConstraintsRetrieveUpdateDestroyView,
    TeacherRoomPreferenceListCreateView, TeacherRoomPreferenceRetrieveUpdateDestroyView,
    TimetableHeaderListCreateView, TimetableHeaderRetrieveUpdateDestroyView,
    TimetableDetailListCreateView, TimetableDetailRetrieveUpdateDestroyView,
    GenerationListCreateView, GenerationRetrieveUpdateDestroyView,
    DisciplineListCreateView, DisciplineRetrieveUpdateDestroyView
)

urlpatterns = [
    # Advisor Auth
    path('advisor/login/', AdvisorLoginView.as_view(), name='advisor-login'),
    path('logout/advisor/', AdvisorLogoutView.as_view(), name='advisor-logout'),

    # Compensatory
    path('compensatory/', CompensatoryListCreateView.as_view(), name='compensatory-list-create'),
    path('compensatory/<int:pk>/', CompensatoryRetrieveUpdateDestroyView.as_view(), name='compensatory-detail'),
     path('disciplines/', DisciplineListCreateView.as_view(), name='discipline-list-create'),
    path('disciplines/<str:pk>/', DisciplineRetrieveUpdateDestroyView.as_view(), name='discipline-detail'),
    # CoursePreferenceConstraints
    path('course-preference-constraints/', CoursePreferenceConstraintsListCreateView.as_view(), name='cpc-list-create'),
    path('course-preference-constraints/<int:pk>/', CoursePreferenceConstraintsRetrieveUpdateDestroyView.as_view(), name='cpc-detail'),

    # TeacherRoomPreference
    path('teacher-room-preference/', TeacherRoomPreferenceListCreateView.as_view(), name='trp-list-create'),
    path('teacher-room-preference/<int:pk>/', TeacherRoomPreferenceRetrieveUpdateDestroyView.as_view(), name='trp-detail'),

    # TimetableHeader
    path('timetable-header/', TimetableHeaderListCreateView.as_view(), name='tth-list-create'),
    path('timetable-header/<int:pk>/', TimetableHeaderRetrieveUpdateDestroyView.as_view(), name='tth-detail'),

    # TimetableDetail
    path('timetable-detail/', TimetableDetailListCreateView.as_view(), name='ttd-list-create'),
    path('timetable-detail/<int:pk>/', TimetableDetailRetrieveUpdateDestroyView.as_view(), name='ttd-detail'),

    path('generation/', GenerationListCreateView.as_view(), name='generation-list-create'),
    path('generation/<int:pk>/', GenerationRetrieveUpdateDestroyView.as_view(), name='generation-detail'),
]
