from rest_framework.permissions import BasePermission


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "CLIENT"


class IsWorker(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "WORKER"

