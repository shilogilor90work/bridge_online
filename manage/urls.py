from django.urls import path
from . import views

app_name = 'manage'

urlpatterns = [
    path('create/', views.create_hand, name='create_hand'),
    path('<int:hand_id>/update/', views.update_hand, name='update_hand'),
    path('<int:hand_id>/delete/', views.delete_hand, name='delete_hand'),
    path('hand_list/', views.hand_list, name='hand_list'),
    path('hand_list_no_shuffle/', views.hand_list_no_shuffle, name='hand_list'),
    path('<int:hand_id>/', views.display_hand, name='display_hand'),  # New path for displaying one hand
    path('update-answer/<int:hand_id>/<str:answer>/<str:explanation>/', views.update_answer, name='update_answer'),
    path('upload-json/', views.upload_json_view, name='upload_json'),
]
