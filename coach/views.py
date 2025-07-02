import os
import openai
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Run, Goal
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .serializers import RunSerializer, GoalSerializer
from django.views.decorators.csrf import csrf_exempt


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
    
class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@api_view(['GET'])
def generate_plan(request):
    user = request.user
    goal = Goal.objects.filter(user = user).first()
    runs = Run.objects.filter(user = user).order_by('-date')[:5]
    
    if not goal or not runs:
        return Response({"error" : "Missing goal or runs"}, status = 400)
    
    run_summary = "\n".join([f"{r.date.date()}:{r.distance_km} km @ {r.average_pace} min/km" for r in runs])
    
    prompt = f"""
    I'm training for a {goal.target_race_distance_km}km race on {goal.race_date}, and I recently ran:
    {run_summary}
    Create a weekly running plan that helps me hit my target time of {goal.target_time_minutes} minutes.
    """
    
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role" : "user", "content" : prompt}]
    )
    
    plan = response['choices'][0]['message''content']
    return Response({"plan" : plan})

#Mock Data for now
@api_view(['POST'])
def add_mock_runs(request):
    from django.utils import timezone
    from datetime import timedelta
    import random
    
    user = request.user
    now = timezone.now()
    for i in range(5):
        Run.objects.create(
            user = user,
            date = now - timedelta(days = i),
            distance_km = round(random.uniform(5, 10), 2),
            average_pace = round(random.uniform(5.0, 6.5), 2),
            strava_id = f"mock-{i}-{user.id}"
        )
    return Response({"status" : "Mock runs added!"})

@csrf_exempt
def home(request):
    plan = None
    if request.method == 'POST':
        if 'mock' in request.POST:
            add_mock_runs(request)
        elif 'generate' in request.POST:
            plan_resp = generate_plan(request)
            plan = plan_resp.data.get('plan')
    return render(request, 'coach/home.html', {'plan' : plan})