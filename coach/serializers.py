from rest_framework import serializers
from .models import Run, Goal

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = '__all__'
        
class GoalSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'