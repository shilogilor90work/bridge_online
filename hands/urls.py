from django.urls import path
from . import views

app_name = 'hands'

urlpatterns = [
        path('', views.bridge_hand, name='index'),
        path('labels', views.bridge_hand_labels, name='labels'),
        path('play/<str:user_name>/', views.hands_by_user, name='labels'),
        path('update_practice/<int:hand_id>/', views.update_practice, name='update_practice'),
        path('update_done/<int:hand_id>/', views.update_done, name='update_done'),

]