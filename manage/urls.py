from django.urls import path
from . import views

app_name = 'manage'

urlpatterns = [
    path('create/', views.create_hand, name='create_hand'),
    path('<int:hand_id>/update/', views.update_hand, name='update_hand'),
    path('<int:hand_id>/delete/', views.delete_hand, name='delete_hand'),
    path('hand_list/', views.hand_list, name='hand_list'),
    path('hand_list/<int:limit>/', views.hand_list_limit, name='hand_list_limit'),
    path('hand_list_no_shuffle/', views.hand_list_no_shuffle, name='hand_list_no_shuffle'),
    path('hand_list_no_answer_only/', views.hand_list_no_answer_only, name='hand_list_no_answer_only'),
    path('hand_list_no_shuffle/<int:limit>/', views.hand_list_no_shuffle_limit, name='hand_list_no_shuffle_limit'),
    path('hand_list_no_shuffle/<int:start_point>/<int:end_point>/', views.hand_list_no_shuffle_limit_and_start, name='hand_list_no_shuffle_limit_and_start'),
    path('<int:hand_id>/', views.display_hand, name='display_hand'),  # New path for displaying one hand
    path('update-explanation/<int:hand_id>/', views.update_explanation, name='update_explanation'),
    path('upload-json/', views.upload_json_view, name='upload_json'),
]
