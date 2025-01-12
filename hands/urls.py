from django.urls import path
from . import views

app_name = 'hands'

urlpatterns = [
        path('', views.bridge_hand, name='index'),
        path('labels', views.bridge_hand_labels, name='labels'),
        path('play/<str:user_name>/', views.hands_by_user, name='hands_by_user'),
        path('needs_validation/', views.hands_that_need_validation, name='needs_validation'),
        path('update_practice/<int:hand_id>/', views.update_practice, name='update_practice'),
        path('update_done/<int:hand_id>/', views.update_done, name='update_done'),
        path('needs_validation/<int:hand_id>/', views.needs_validation, name='needs_validation'),
        path('remove_needs_validation/<int:hand_id>/', views.remove_needs_validation, name='remove_needs_validation'),
        path('compete/<int:competition_id>/', views.compete, name='compete'),
        path('compete/<int:competition_id>/submit', views.compete_submit, name='compete_submit'),
]