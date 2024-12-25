from django.urls import path
from . import views

app_name = 'hands'

urlpatterns = [
    path('', views.HandsView.as_view(), name='index'),
    # path('<int:hand_id>/delete', views.delete, name='delete'),
    # path('<int:hand_id>/update', views.update, name='update'),
    # path('add/', views.add, name='add')
]