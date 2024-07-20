from django.urls import path
from . import views

urlpatterns = [
    path("", views.Controls.as_view(), name="controls"),
    path("results/", views.Results.as_view(), name="results"),
    path("scoresheet/", views.Scoresheet.as_view(), name="scoresheet"),
    path("verify_questions/", views.VerifyQuestion.as_view(), name="verify_question"),
    path("setting/", views.Setting.as_view(), name="setting"),
    path("add_question/", views.AddQuestion.as_view(), name="add_question"),
]
