from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.serializers import UserSerializer
from clients.models import Client
from projects.models import Project


class ProjectInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'project_name'
        ]


class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
    client_id = serializers.IntegerField(write_only=True)
    client = serializers.CharField(read_only=True)
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'project_name',
            'client_id',
            'client',
            'users',
            'created_at',
            'created_by'
        ]
        read_only_fields = ['created_at']

    def get_created_by(self, instance):
        '''
        Deriving SerializerMethodField value from the instance.
        '''
        return f'{instance.created_by.first_name} {instance.created_by.last_name}'

    def validate_client_id(self, value):
        if not Client.objects.filter(id=value).exists():
            raise ValidationError('Client with given ID does not exist.')
        return value

    def create(self, validated_data):
        logged_in_user = self.context['request'].user
        user_ids = validated_data.pop('users')
        project = Project.objects.create(**validated_data,
                                         created_by=logged_in_user)
        users = User.objects.filter(id__in=user_ids)
        project.users.add(*users)
        return project

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            return data
        users = []
        for user in instance.users.all():
            user_data = UserSerializer(user).data
            users.append(user_data)
        data['users'] = users
        return data
