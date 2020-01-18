import os
import docker
from django.shortcuts import render
from pathlib import Path
from .models import Competition, Submission
from random import randint
from secrets import token_urlsafe


def load_competitions(request, user):

    entered_competitions = user.submission_set.all()
    active_competitions = Competition.objects.exclude(
        submission__in=entered_competitions
    )
    # paginator = Paginator(competition, 2)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)
    return render(
        request,
        "core/index.html",
        {
            "active_competitions": active_competitions,
            "entered_competitions": entered_competitions,
            "user": request.user,
        },
    )


def tell_about_turing_halt(request):
    pass


def start_jupyter_server(user, competition):
    try:
        print(12)
        submission = Submission.objects.get(competitor=user, competition=competition)
        print(13)
        return submission.container_path
    except:
        # print(ValueError)
        Path(
            "/home/s8/Videos/competition/user-{}/competition-{}".format(
                user.id, competition.id
            )
        ).mkdir(parents=True, exist_ok=True)

        error = os.system(
            "cp /home/s8/Videos/kaggle_clone/kaggle_clone/media/{} \
                /home/s8/Videos/competition/user-{}/competition-{}/".format(
                competition.train_csv, user.id, competition.id
            )
        )

        error = os.system(
            "cp /home/s8/Videos/kaggle_clone/kaggle_clone/media/{} \
                /home/s8/Videos/competition/user-{}/competition-{}/".format(
                competition.train_solution_csv, user.id, competition.id
            )
        )

        error = os.system(
            "cp /home/s8/Videos/kaggle_clone/kaggle_clone/media/{} \
                /home/s8/Videos/competition/user-{}/competition-{}/".format(
                competition.test_csv, user.id, competition.id
            )
        )

        error = os.system(
            "cp /home/s8/Videos/kaggle_clone/kaggle_clone/media/{} \
                /home/s8/Videos/competition/user-{}/competition-{}/".format(
                competition.test_solution_csv, user.id, competition.id
            )
        )

        client = docker.from_env().api
        volumes = [
            "/home/s8/Videos/competition/user-{}/competition-{}".format(
                user.id, competition.id
            )
        ]
        volume_bindings = {
            "/home/s8/Videos/competition/user-{}/competition-{}".format(
                user.id, competition.id
            ): {"bind": "/usr/src/code", "mode": "rw"},
        }

        port = randint(9999, 65535)
        host_config = client.create_host_config(
            binds=volume_bindings, port_bindings={8888: port}
        )

        jupyter_access_token = token_urlsafe(16)

        command = "jupyter notebook --ip 0.0.0.0 --port 8888 --allow-root --NotebookApp.token='{}'".format(
            jupyter_access_token
        )

        container = client.create_container(
            image="comp:latest",
            volumes=volumes,
            ports=[8888],
            host_config=host_config,
            command=command,
        )

        container_id = container.get("Id")
        client.start(container=container_id)

        client = docker.from_env()

        submission = Submission(competitor=user, competition=competition)
        submission.container_id = container_id
        submission.port = port
        submission.container_path = "127.0.0.1:{}/?token={}".format(
            port, jupyter_access_token
        )
        submission.save()
        print(submission)
        return submission.container_path
