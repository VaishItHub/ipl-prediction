from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict-match/', views.predict_match, name='predict_match'),
]

    
