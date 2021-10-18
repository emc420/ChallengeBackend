from django.urls import path
from groover_api import views 


urlpatterns = [
    path('artists/', views.getArtists)
]