from django.urls import path
from . import views

app_name = 'manage'

urlpatterns = [
    path('create/', views.create_hand, name='create_hand'),
    path('<int:hand_id>/update/', views.update_hand, name='update_hand'),
    path('<int:hand_id>/delete/', views.delete_hand, name='delete_hand'),
    path('hand_list/', views.hand_list, name='hand_list'),
    path('update-answer/<int:hand_id>/<str:answer>/<str:explanation>/', views.update_answer, name='update_answer'),
]
