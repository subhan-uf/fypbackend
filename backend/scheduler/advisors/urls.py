 # advisors/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('advisor/login/', AdvisorLoginView.as_view(), name='advisor-login'),
    path('teacher-preferences/', TeacherPreferenceView.as_view(), name='teacher-preferences'),

    path('logout/advisor/', AdvisorLogoutView.as_view(), name='logout'),
]
