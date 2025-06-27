from rest_framework import viewsets
from .models import Run, Goal
from .serializers import RunSerializer, GoalSerialzer

class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
    
class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerialzer
    