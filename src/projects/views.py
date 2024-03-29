from django.db.models import query
from rest_framework.generics import ListCreateAPIView
from projects.models import Project
from projects.serializers import ProjectSerializer


class ProjectListCreateAPIView(ListCreateAPIView):
    queryset = Project.objects.select_related('created_by', 'client')
    serializer_class = ProjectSerializer

    def get_queryset(self):
        '''
        Following query is optimized and we have explicitely mentioned fields
        that we want to retrieve. To understand better, Comment this function
        and check SQL query in debug toolbar with above queryset.
        '''
        logged_in_user = self.request.user
        queryset = Project.objects \
            .select_related('created_by', 'client') \
            .filter(users=logged_in_user) \
            .only('id', 'project_name', 'client_id', 'created_at', 'created_by_id',
                 'client__client_name', 'created_by__first_name', 'created_by__last_name')
        return queryset