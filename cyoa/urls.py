from django.urls import path

from . import views

urlpatterns = [
    path('data/', views.get_game, name='get game'),
    path('view/', views.view_game, name='view game'),
    path('check/', views.check_game, name='check game'),
]