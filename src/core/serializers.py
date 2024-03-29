from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'name'
        ]

    def get_name(self, instance):
        return f'{instance.first_name} {instance.last_name}'