from django.urls import path
from clients import views


urlpatterns = [
    path('', views.ClientListCreateAPIView.as_view(), name='client-list-create-api'),
    path('<int:pk>/', views.ClientRetrieveUpdateAPIView.as_view(), name='client-retrieve-update-api')
]
