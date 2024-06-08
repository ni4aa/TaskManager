from django.shortcuts import render
from rest_framework import viewsets, permissions, request, status, generics
from .models import Task
from .serializers import CreateTaskSerializer, TakeTaskSerializer, ReadTaskSerializer, CloseTaskSerializer, MyTaskSerializer
from .permissions import IsClient, IsWorker
from django.db.models import Q


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = CreateTaskSerializer
    http_method_names = ['get', 'post', 'put', 'patch']

    def get_queryset(self):
        queryset = super(TaskViewSet, self).get_queryset()

        if self.request.user.is_staff:
            return queryset

        if self.request.user.role == 'CLIENT':
            return queryset.filter(client=self.request.user)
        else:
            if self.request.method == "GET":
                return queryset
            else:
                return queryset.filter(status="ON HOLD")

    def get_permissions(self):
        if self.request.method in ['POST']:
            if self.request.user.is_staff:
                return [permissions.IsAdminUser()]
            else:
                return [IsClient()]

        if self.request.method in ["PUT", "PATCH"]:
            return [IsWorker()]

        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return ReadTaskSerializer

        if self.request.method in ["PUT", "PATCH"]:
            return TakeTaskSerializer

        return CreateTaskSerializer


class MyListTaskAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = MyTaskSerializer
    permission_classes = [IsWorker | IsClient]

    def get_queryset(self):
        queryset = super(MyListTaskAPIView, self).get_queryset()

        if self.request.user.role == 'CLIENT':
            return queryset.filter(client=self.request.user)
        else:
            return queryset.filter(worker=self.request.user)



class MyTaskAPIView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = MyTaskSerializer
    permission_classes = [IsWorker, ]

    def get_queryset(self):
        queryset = super(MyTaskAPIView, self).get_queryset()

        if self.request.method in ["PUT", "PATCH"]:
            return queryset.filter(Q(worker=self.request.user) & Q(status="IN PROCESS"))

        return queryset.filter(worker=self.request.user)


class CloseTaskAPIView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = CloseTaskSerializer
    permission_classes = [IsWorker, ]

    def get_queryset(self):
        queryset = super(CloseTaskAPIView, self).get_queryset()

        return queryset.filter(Q(worker=self.request.user) & Q(status="IN PROCESS"))




