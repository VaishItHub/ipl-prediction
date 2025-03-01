

#3--------------
# In your views.py


from django.shortcuts import render
from django.http import JsonResponse
import os
import json
import time
from django.conf import settings
from .models import Players, Venues, Prediction
from django.core.serializers.json import DjangoJSONEncoder
from .models import Prediction
import pickle
import pandas as pd

# Function to load all pickle files from the 'pickl' directory
def load_pickles_from_directory(directory):
    pickle_data = {}
    if os.path.exists(directory):
        for file_name in os.listdir(directory):
            if file_name.endswith('.pkl'):
                file_path = os.path.join(directory, file_name)
                with open(file_path, 'rb') as file:
                    pickle_data[os.path.splitext(file_name)[0]] = pickle.load(file)
    else:
        raise FileNotFoundError(f"Pickle directory does not exist: {directory}")
    return pickle_data

# Function to read prediction text files and return the contents
def read_prediction_files(directory):
    prediction_data = []
    if os.path.exists(directory):
        for file_name in os.listdir(directory):
            if file_name.endswith('.txt'):
                file_path = os.path.join(directory, file_name)
                with open(file_path, 'r') as file:
                    content = file.readlines()
                    prediction = {}
                    for line in content:
                        key, value = line.strip().split(": ", 1)
                        prediction[key] = value
                    prediction_data.append(prediction)
    return prediction_data

def home(request):
    teams = Players.objects.values_list('team_name', flat=True).distinct()
    players = list(Players.objects.values('team_name', 'player_name'))  # Serialize players
    venues = Venues.objects.all()

    # Fetch predictions from the database
    predictions = Prediction.objects.all()

    # Read predictions from text files
    predictions_folder = os.path.join(settings.BASE_DIR, 'predictions')
    prediction_files = read_prediction_files(predictions_folder)

    context = {
        'teams': teams,
        'players': json.dumps(players, cls=DjangoJSONEncoder),  # Pass serialized players
        'venues': venues,
        'predictions': prediction_files,  # Pass the predictions read from text files
    }
    return render(request, 'import_csv.html', context)


def predict_match(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            batting_team = data.get('batting_team')
            bowling_team = data.get('bowling_team')
            striker = data.get('striker')
            non_striker = data.get('non_striker')
            venue = data.get('venue')
            balls = int(data.get('balls'))
            season = data.get('season')

            striker_data = Players.objects.filter(team_name=batting_team, player_name=striker).first()
            non_striker_data = Players.objects.filter(team_name=batting_team, player_name=non_striker).first()
            bowler_data = Players.objects.filter(team_name=bowling_team, player_name=data.get('bowler')).first()

            striker_sr = striker_data.strike_rate if striker_data else 0

            prediction_data = {
                'batter': striker,
                'bowler': bowler_data.player_name if bowler_data else None,
                'non_striker': non_striker,
                'venue': venue,
                'season': season,
                'team1': batting_team,
                'team2': bowling_team,
                'balls_count': balls,
                'strike_rate': striker_sr,
                'total_runs' : 0,
            }

            # Load pickle models
            pickles_directory = os.path.join(settings.BASE_DIR, 'pickl')
            models = load_pickles_from_directory(pickles_directory)

            if 'batter' not in models or 'Bowler' not in models:
                return JsonResponse({'error': 'Required model "batter.pkl" or "Bowler.pkl" not found'}, status=500)

            batter_model = models['batter']
            bowler_model = models['Bowler']

            batter_input = pd.DataFrame(
                data=[[elem for elem in prediction_data.values()]],
                columns=['batter', 'bowler', 'non_striker', 'venue', 'season', 'team1', 'team2', 'balls_count', 'strike_rate', 'total_runs']
            )
            runs_prediction = batter_model.predict(batter_input)
            wicket_prediction = bowler_model.predict(batter_input)

# Ensure runs_prediction is in integer form
            if isinstance(runs_prediction, (int, float)):
             prediction_data['runs_prediction'] = int(runs_prediction)  
            else:
             prediction_data['runs_prediction'] = int(runs_prediction[0])  # Handle array-like output



# Update prediction data
            prediction_data['wicket_chance'] = f"{int(wicket_prediction[0])}%"
            # prediction_data['runs_prediction'] = runs_prediction[0]

            # Save prediction in the list
            # predictions_list.append(prediction_data)

            # Save the prediction to a file
            predictions_folder = os.path.join(settings.BASE_DIR, 'predictions')
            os.makedirs(predictions_folder, exist_ok=True)
            prediction_file = os.path.join(predictions_folder, f"prediction_{str(round(time.time() * 1000))}.txt")

            with open(prediction_file, 'w') as file:
                for key, value in prediction_data.items():
                    file.write(f"{key}: {value}\n")

            return JsonResponse({'prediction_data': prediction_data, 'message': 'Prediction saved successfully', 'file_path': prediction_file})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
