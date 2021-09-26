from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from projects.models import Project
from .serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser


@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)