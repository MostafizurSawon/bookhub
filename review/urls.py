from django.urls import path
from . import views
 
urlpatterns = [
    path('reviews/<int:pk>', views.review, name='review'),
]