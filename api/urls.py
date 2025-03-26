# urls.py
from django.urls import path
from .views import CableTracertViewSet

urlpatterns = [
    path('trace/', CableTracertViewSet.as_view({'get': 'trace'}), name='trace'),
    path('paths/<int:pk>/', CablePathDetailView.as_view(), name='path-detail'),
]