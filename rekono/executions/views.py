from django.core.exceptions import PermissionDenied
from executions.exceptions import InvalidTaskException
from executions.models import Execution, Task
from executions.serializers import ExecutionSerializer, TaskSerializer
from rest_framework import status
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin, DestroyModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from executions import services
from projects.models import Target

# Create your views here.


class TaskViewSet(
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin
):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_fields = {
        'target': ['exact'],
        'target__project': ['exact'],
        'process': ['exact'],
        'tool': ['exact'],
        'intensity': ['exact'],
        'executor': ['exact'],
        'status': ['exact'],
        'start': ['gte', 'lte', 'exact'],
        'end': ['gte', 'lte', 'exact']
    }
    ordering_fields = (
        'target', 'target__project', 'process', 'tool', 'intensity', 'executor',
        'status', 'start', 'end'
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(target__project__members=self.request.user)

    def perform_create(self, serializer):
        project_check = Target.objects.filter(
            id=serializer.validated_data.get('target').id,
            project__members=self.request.user
        ).exists()
        if not project_check:
            raise PermissionDenied()
        serializer.save(executor=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            services.cancel_task(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvalidTaskException:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class ExecutionViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin
):
    queryset = Execution.objects.all()
    serializer_class = ExecutionSerializer
    filterset_fields = {
        'task': ['exact'],
        'task__target': ['exact'],
        'task__target__project': ['exact'],
        'task__process': ['exact'],
        'task__tool': ['exact'],
        'task__intensity': ['exact'],
        'task__executor': ['exact'],
        'status': ['exact'],
        'step__tool': ['exact'],
        'start': ['gte', 'lte', 'exact'],
        'end': ['gte', 'lte', 'exact']
    }
    ordering_fields = (
        ('target', 'task__target'),
        ('project', 'task__target__project'),
        ('process', 'task__process'),
        ('intensity', 'task__intensity'),
        ('executor', 'task__executor'),
        'task__tool', 'step_tool',
        'status', 'start', 'end'
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(task__target__project__members=self.request.user)
