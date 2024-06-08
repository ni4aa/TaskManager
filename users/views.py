from rest_framework import viewsets, permissions
from users.models import User
from .serializers import UserSerializer
from tasks.permissions import IsWorker

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post"]

    def get_queryset(self):
        queryset = super(UserViewSet, self).get_queryset()

        if self.request.user.role == "CLIENT":
            return queryset.filter(role="WORKER")
        else:
            return queryset.order_by("role")

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]

        if self.request.method == "POST":
            return [IsWorker()]

