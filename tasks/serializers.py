import datetime

from rest_framework import serializers
from django.shortcuts import render
from .models import Task
from users.models import User


class CreateTaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    client = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ('id', 'title', 'client', 'worker', 'status')
        extra_kwargs = {'title': {'read_only': True},
                        'status': {'read_only': True},
                        'worker': {'read_only': True}
                        }

    def __init__(self, *args, **kwargs):
        super(CreateTaskSerializer, self).__init__(*args, **kwargs)
        user = kwargs['context']['request'].user
        if user.role == "WORKER":
            self.fields['client'].queryset = User.objects.all().filter(role="CLIENT")
        else:

            self.fields['client'] = serializers.HiddenField(default=serializers.CurrentUserDefault())


class ReadTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TakeTaskSerializer(serializers.ModelSerializer):
    worker = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = ("id", "title", "client", "worker", "status")
        extra_kwargs = {'title': {'read_only': True},
                        'client': {'read_only': True},
                        'status': {'read_only': True}
                        }

    def update(self, instance, validated_data):
        validated_data["status"] = "IN PROCESS"
        return super(TakeTaskSerializer, self).update(instance, validated_data)


class MyTaskSerializer(serializers.ModelSerializer):
    report = serializers.CharField()

    class Meta:
        model = Task
        fields = ("id", "title", "report", "client", "status", "created_at", "updated_at")
        extra_kwargs = {'title': {'read_only': True},
                        'client': {'read_only': True},
                        'status': {'read_only': True},
                        'created_at': {'read_only': True},
                        'updated_at': {'read_only': True},
                        }


class CloseTaskSerializer(serializers.ModelSerializer):
    report = serializers.CharField()

    class Meta:
        model = Task
        fields = ("title", "report", "client", "status", "created_at", "updated_at", "closed_at")
        extra_kwargs = {'title': {'read_only': True},
                        'client': {'read_only': True},
                        'status': {'read_only': True},
                        'created_at': {'read_only': True},
                        'updated_at': {'read_only': True},
                        'closed_at': {'read_only': True},
                        }

    def update(self, instance, validated_data):
        instance.closed_at = datetime.datetime.now()
        validated_data["status"] = "COMPLETED"
        return super(CloseTaskSerializer, self).update(instance, validated_data)