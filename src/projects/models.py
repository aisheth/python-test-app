from django.db import models
from django.contrib.auth.models import User
from clients.models import Client


class Project(models.Model):
    '''
    Data model for Project. To store information about projects.
    '''
    project_name = models.CharField(max_length=100, blank=False, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    users = models.ManyToManyField(User, through='ProjectUser')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, 
                                    related_name='project_created_by')

    class Meta:
        db_table = 'projects'
        default_permissions = ()

    def __str__(self):
        return self.project_name


class ProjectUser(models.Model):
    '''
    Data model for ProjectUser. To store many to many mapping of projects and users.
    Seperate Model is created to add contraint and have more control over this table.
    We have user user ManyToMany field with through attribute in Project model.
    '''
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'project_users'
        default_permissions = ()
        unique_together = ('project', 'user')

    def __str__(self):
        return f'{self.project.project_name} - {self.user.username}'