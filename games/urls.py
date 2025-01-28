from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
        path('', views.GameListView.as_view(), name='game-list'),
        path('create/', views.game_create, name='game-create'),
        path('<int:pk>/update/', views.GameUpdateView.as_view(), name='game-update'),
        path('<int:pk>/delete/', views.GameDeleteView.as_view(), name='game-delete'),
]