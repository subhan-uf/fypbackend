from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import DEOLoginView,AdvisorListCreateView, AdvisorRetrieveUpdateDestroyView,DEOLogoutView
from .views import * 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('login/deo/', DEOLoginView.as_view(), name='deo-login'),
    path('advisors/', AdvisorListCreateView.as_view(), name='advisor-list-create'),
    path('advisors/<int:pk>/', AdvisorRetrieveUpdateDestroyView.as_view(), name='advisor-detail'),
    path('teachers/', TeacherListCreateView.as_view(), name='teacher-list-create'),  
    path('teachers/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),   
    path('logout/deo/', DEOLogoutView.as_view(), name='logout'),
]



# http://127.0.0.1:8000/api/login/deo/
# http://127.0.0.1:8000/api/advisors/
# http://127.0.0.1:8000/api/advisors/
# http://127.0.0.1:8000/api/advisors/2/
# http://127.0.0.1:8000/api/advisors/1/
# http://127.0.0.1:8000/api/logout/deo/