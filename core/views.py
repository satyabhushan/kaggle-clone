from django.shortcuts import (
    render,
    HttpResponse,
    redirect,
    get_object_or_404,
)
from django.http import JsonResponse
from .models import Competition, Submission
from .forms import HostCompetitionForm
# from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .service import (
    start_jupyter_server,
    load_competitions,
    tell_about_turing_halt,
    submit_solution,
)
from .handle_jupyter_server import enroll_user


def index(request):
    user = request.user
    # rendered = load_competitions(request, user)

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
    competition_enrolls = competition.submission_set.filter(
        accuracy__isnull=False
    ).order_by("-accuracy")

    user_enroll = None
    user_submit = None
    user_rank = None

    if user.is_authenticated:
        user_enroll = competition.submission_set.filter(competitor=user).first()
        if user_enroll:
            user_submit = user_enroll.accuracy
            if user_submit is not None:
                user_rank = list(competition_enrolls).index(user_enroll) + 1

    return render(
        request,
        "core/leaderboard.html",
        {
            "competition": competition,
            "competition_enrolls": list(competition_enrolls),
            "user": user,
            "user_enroll": user_enroll,
            "user_submit": user_submit,
            "user_rank": user_rank,
        },
    )


@login_required(login_url="/login")
def join_competition(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    user = request.user
    status = enroll_user(user, competition)
    message = None
    if status["task_status"] in ("STARTING", "PENDING"):
        pass
    else:
        message = "You have already joined the competition."
    return render(
        request,
        "core/start_competition.html",
        {
            "competition": competition,
            "user": user,
            "message": message,
            "jupyter_path": status["jupyter_path"],
        },
    )


@login_required(login_url="/login")
def join_status(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    user = request.user
    status = enroll_user(user, competition)
    return JsonResponse(status)


@login_required(login_url="/login")
def submit_prediction(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    user = request.user
    return submit_solution(request, competition, user)


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
