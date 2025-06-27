from django.db import models
from django.contrib.auth.models import User

class Run(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    distance_km = models.FloatField()
    average_pace = models.FloatField()
    strava_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.date.date()}"
    
class Goal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target_race_distance_km = models.FloatField()
    target_time_minutes = models.FloatField()
    race_date = models.DateField()
    
    def __str__(self):
        return f"{self.user.username}'s goal" 