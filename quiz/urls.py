from django.urls import path
from . import views

urlpatterns = [
    path("", views.Quiz.as_view(), name="quiz"),

    path("attempts/", views.Attempts.as_view(), name="attempts"),

]
