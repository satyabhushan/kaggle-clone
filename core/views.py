from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, Http404
from .models import Competition, Submission
from .forms import HostCompetitionForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .service import (
    start_jupyter_server,
    load_competitions,
    tell_about_turing_halt,
    submit_solution,
)


def index(request):
    user = request.user
    if user.is_authenticated:
        rendered = load_competitions(request, user)
    else:
        rendered = tell_about_turing_halt(request)
    return rendered


def competition(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    user = request.user
    user_enroll = None
    user_submit = None
    jupyter_notebook_url = None

    if user.is_authenticated:
        user_enroll = user.submission_set.filter(competition=competition).first()
        if user_enroll:
            user_submit = user_enroll.accuracy
            jupyter_notebook_url = user_enroll.container_path
            print(jupyter_notebook_url)
    return render(
        request,
        "core/competition.html",
        {
            "competition": competition,
            "user": user,
            "user_enroll": user_enroll,
            "user_submit": user_submit,
            "jupyter_notebook_url": jupyter_notebook_url,
        },
    )


def leaderboard(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    user = request.user
    return render(
        request, "core/leaderboard.html", {"competition": competition, "user": user}
    )


@login_required(login_url="/login")
def join_competition(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    user = request.user
    return render(
        request, "core/leaderboard.html", {"competition": competition, "user": user}
    )


@login_required(login_url="/login")
def submit_prediction(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    user = request.user
    submit_solution(competition, user)

    return render(
        request,
        "core/submit_prediction.html",
        {"competition": competition, "user": user},
    )


def start_competition(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)

    jupyter_url = start_jupyter_server(request.user, competition)
    # return HttpResponse(jupyter_url)
    return render(
        request,
        "core/start_competition.html",
        {"jupyter_url": jupyter_url, "user": request.user},
    )


@login_required
def host_competition(request):
    user = request.user
    if request.method == "POST":
        form = HostCompetitionForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            competition = form.save(commit=False)
            competition.host = user
            competition.save()
            return redirect("/competition/" + str(competition.id))
        else:
            print(form.errors)
    if request.method == "GET":
        form = HostCompetitionForm()
    return render(request, "core/host_competition.html", {"form": form, "user": user})
