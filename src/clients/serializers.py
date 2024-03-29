from rest_framework import serializers
from clients.models import Client
from projects.serializers import ProjectInfoSerializer



class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(read_only=True)

    class Meta:
        model = Client
        fields = [
            'id',
            'client_name',
            'created_at',
            'updated_at',
            'created_by'
        ]
        read_only_fields = ['created_at'] 

    def create(self, validated_data):
        logged_in_user = self.context['request'].user
        client = Client.objects.create(created_by=logged_in_user,
                                    **validated_data)
        return client


class ClientDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(read_only=True)
    projects = ProjectInfoSerializer(many=True)

    class Meta:
        model = Client
        fields = [
            'id',
            'client_name',
            'projects',
            'created_at',
            'updated_at',
            'created_by'
        ]