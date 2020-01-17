from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "competition/<int:competition_id>", views.competition, name="watch.competition",
    ),
    path("host-competition", views.host_competition, name="watch.host_competition",),
    path("start-competition/<int:competition_id>", views.start_competition, name="watch.start_competition",),
]