from django.urls import path
from .views import ContentViewSet

urlpatterns = [
    path('list',ContentViewSet.as_view({'get':'get'}),name='list'),
    path('retrive',ContentViewSet.as_view({'get':'retrive'}),name='retrive'),
    path('create',ContentViewSet.as_view({'post':'post'}),name='create'),
    path('update',ContentViewSet.as_view({'put':'put'}),name='update'),
    path('delete',ContentViewSet.as_view({'delete':'delete'}),name='delete'),
]