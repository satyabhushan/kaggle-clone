from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, Http404
from .models import Competition, Submission
from .forms import HostCompetitionForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .service import start_jupyter_server, load_competitions, tell_about_turing_halt


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
    user_enroll = user.submission_set.filter(competition=competition).first()
    user_submit = None
    if user_enroll:
        user_submit = user_enroll.accuracy
    return render(
        request,
        "core/competition.html",
        {
            "competition": competition,
            "user": user,
            "user_enroll": user_enroll,
            "user_submit": user_submit,
        },
    )


def leaderboard(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    user = request.user
    return render(
        request, "core/leaderboard.html", {"competition": competition, "user": user}
    )


def join_competition(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    user = request.user
    return render(
        request, "core/leaderboard.html", {"competition": competition, "user": user}
    )


def submit_solution(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    user = request.user
    return render(
        request, "core/leaderboard.html", {"competition": competition, "user": user}
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


@login_required(login_url="login/")
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
