from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, Http404
from .models import Competition, Submission
from .forms import HostCompetitionForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .service import start_jupyter_server

def index(request):
    competition = Competition.objects.all()
    paginator = Paginator(competition, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request, "core/index.html", {"videos": page_obj, "user": request.user}
    )


def competition(request, competition_id):
    return HttpResponse("Check")

def start_competition(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    
    jupyter_url = start_jupyter_server(request.user, competition)
    return HttpResponse(jupyter_url)

@login_required(login_url='login/')
def host_competition(request):
    user = request.user
    if request.method == "POST":
        form = HostCompetitionForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            competition = form.save(commit=False)
            competition.host = user
            competition.save()
            return redirect('/')
        else:
            print(form.errors)
    if request.method == "GET":
        form = HostCompetitionForm()
    return render(request, "core/host_competition.html", {"form": form, "user": user})
