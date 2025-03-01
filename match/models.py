 # models.py

from django.db import models
class Players(models.Model):
    team_name = models.CharField(max_length=100)
    player_name = models.CharField(max_length=100)
    strike_rate = models.FloatField(max_length=10)  # Ensure this is defined
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.team_name} - {self.player_name} - {self.strike_rate} - {self.role}"

class Venues(models.Model):
    stadium=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    def __str__(self):
        return f"{self.stadium} - {self.city}"  
    

# In models.py
from django.db import models

class Prediction(models.Model):
    striker = models.CharField(max_length=255)
    bowler = models.CharField(max_length=255)
    non_striker = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    season = models.CharField(max_length=255)
    batting_team = models.CharField(max_length=255)
    bowling_team = models.CharField(max_length=255)
    balls = models.IntegerField()
    strike_rate = models.FloatField()
    runs_prediction = models.FloatField()
    prediction_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction: {self.batting_team} vs {self.bowling_team} ({self.prediction_time})"
