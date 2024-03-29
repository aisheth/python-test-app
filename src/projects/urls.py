from django.urls import path
from projects import views


urlpatterns = [
    path('', views.ProjectListCreateAPIView.as_view(), name='project-list-create-api'),
]
