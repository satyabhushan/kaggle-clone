from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("competition/<int:competition_id>", views.competition, name="competition",),
    path(
        "competition/<int:competition_id>/leaderboard",
        views.leaderboard,
        name="leaderboard",
    ),
    path(
        "competition/<int:competition_id>/join-competition",
        views.join_competition,
        name="join_competition",
    ),
    path(
        "competition/<int:competition_id>/submit-prediction",
        views.submit_solution,
        name="submit_solution",
    ),
    path("host-competition", views.host_competition, name="host_competition",),
    path(
        "start-competition/<int:competition_id>",
        views.start_competition,
        name="start_competition",
    ),
]
