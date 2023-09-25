from django.urls import path
from .views import RoleViewSet,RegisterViewSet,LoginAPIView

urlpatterns = [
    path('roles',RoleViewSet.as_view({'get':'list'}),name='roles'),
    path('create-roles',RoleViewSet.as_view({'post':'create'}),name='create-roles'),
    path('users',RegisterViewSet.as_view({'get':'list'}),name='users'),
    path('register',RegisterViewSet.as_view({'post':'create'}),name='register'),
    path('login',LoginAPIView.as_view(),name='login'),
]