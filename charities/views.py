from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from .models import Task, Benefactor
from .serializers import BenefactorSerializer, CharitySerializer, TaskSerializer
from accounts.permissions import IsBenefactor, IsCharityOwner


class BenefactorRegistration(CreateAPIView):
    serializer_class = BenefactorSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = BenefactorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=request.data, status=HTTP_201_CREATED)
        return Response(data='Invalid Request', status=HTTP_400_BAD_REQUEST)


class CharityRegistration(CreateAPIView):
    serializer_class = CharitySerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = CharitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=request.data, status=HTTP_201_CREATED)
        return Response(data='Invalid Request', status=HTTP_400_BAD_REQUEST)


class TaskRequest(APIView):
    permission_classes = [IsAuthenticated, IsBenefactor]

    def get(self, request, task_id):

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            task = None

        if task is None:
            return Response(data='Task not found', status=HTTP_404_NOT_FOUND)

        if task.state != 'P':
            return Response(data={'detail': 'This task is not pending.'},
                            status=HTTP_404_NOT_FOUND)

        task.state = 'W'
        task.assigned_benefactor = Benefactor.objects.get(user=request.user)
        task.save()
        return Response(data={'detail': 'Request sent.'}, status=HTTP_200_OK)


class TaskResponse(APIView):
    permission_classes = (IsAuthenticated, IsCharityOwner)

    def post(self, request, task_id):

        response = request.data.get('response')
        if response not in ('A', 'R'):
            return Response(data={'detail': 'Required field ("A" for accepted / "R" for rejected)'},
                            status=HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            task = None

        if task.state != 'W':
            return Response(data={'detail': 'This task is not waiting.'}, status=HTTP_404_NOT_FOUND)

        if response == 'A':
            task.state = 'A'
            task.save()
            return Response(data={'detail': 'Response sent.'}, status=HTTP_200_OK)

        if response == 'R':
            task.state = 'P'
            task.assigned_benefactor = None
            task.save()
            return Response(data={'detail': 'Response sent.'}, status=HTTP_200_OK)


class DoneTask(APIView):
    permission_classes = (IsAuthenticated, IsCharityOwner)

    def post(self, request, task_id):

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        if task.state != 'A':
            return Response(data={'detail': 'Task is not assigned yet.'}, status=HTTP_404_NOT_FOUND)

        task.state = 'D'
        task.save()
        return Response(data={'detail': 'Task has been done successfully.'}, status=HTTP_200_OK)


class Tasks(ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all_related_tasks_to_user(self.request.user)

    def post(self, request, *args, **kwargs):
        data = {
            **request.data,
            "charity_id": request.user.charity.id
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsCharityOwner, ]

        return [permission() for permission in self.permission_classes]

    def filter_queryset(self, queryset):
        filter_lookups = {}
        for name, value in Task.filtering_lookups:
            param = self.request.GET.get(value)
            if param:
                filter_lookups[name] = param
        exclude_lookups = {}
        for name, value in Task.excluding_lookups:
            param = self.request.GET.get(value)
            if param:
                exclude_lookups[name] = param

        return queryset.filter(**filter_lookups).exclude(**exclude_lookups)
