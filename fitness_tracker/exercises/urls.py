from django.urls import path
from . import views

app_name = 'exercises'

urlpatterns = [
    path('', views.get_exercises, name='get_exercises'),
    path('create/', views.create_exercise, name='create_exercise'),
    path('<int:exercise_id>/', views.get_exercise, name='get_exercise'),
]

