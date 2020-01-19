import os
import docker
import json
from django.shortcuts import render
from pathlib import Path
from .models import Competition, Submission
from random import randint
from secrets import token_urlsafe
from .extract_csv_file_data import parse_data


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
            "cp /home/s8/Videos/kaggle_clone/kaggle_clone/Kernel.ipynb \
                /home/s8/Videos/competition/user-{}/competition-{}/Kernel-{}.ipynb".format(
                user.id, competition.id, user.id,
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
        submission.container_path = "127.0.0.1:{}/notebooks/Kernel-{}.ipynb?token={}".format(
            port, user.id, jupyter_access_token
        )

        submission.save()
        print(submission)
        return submission.container_path


def get_user_solution_data(competition_id, user_id):
    try:
        user_solution_file_path = "/home/s8/Videos/compertition/user-{}/competition-{}/solution.csv".format(
            user_id, competition_id
        )
        with open(user_solution_file_path) as csv_file:

            solution_output = parse_data(csv_file.read())
            return solution_output
    except IOError:
        try:
            user_kernel_ipynb_file_path = "/home/s8/Videos/compertition/user-{}/competition-{}/Kernel-{}.ipynb.csv".format(
                user_id, competition_id, user_id
            )
            with open(user_kernel_ipynb_file_path) as ipynb_file:
                data = json.loads(ipynb_file.read())
                solution_output = data["cells"][-1]["outputs"]
                if solution_output.get("text"):
                    try:
                        output = json.loads(solution_output["text"])
                        return output
                    except:
                        return {}
        except IOError:
            return {}


def get_solution_data(competition):
    solution_file_path = competition.test_solution_csv
    with open(
        "/home/s8/Videos/kaggle_clone/kaggle_clone/media/{}".format(solution_file_path)
    ) as solution_file:
        solution_output = solution_file.read()

    return solution_output


def get_accuracy_percentage(solution_output, user_solution_output):

    if solution_output == user_solution_output:
        return 100

    keys_len = len(solution_output.keys())
    correct_ids_len = 0

    for user_solution_output_id in user_solution_output:
        if user_solution_output[user_solution_output_id] == solution_output.get(
            user_solution_output_id
        ):
            correct_ids_len += 1

    accuracy_percentage = correct_ids_len*100/keys_len
    return accuracy_percentage


def submit_solution(competition, user):
    user_solution_output = get_user_solution_data(competition.id, user.id)
    solution_data = get_solution_data(competition)
    accuracy = get_accuracy_percentage(solution_data, user_solution_output)
    Submission.filter(competition=competition, competitor=user).update(accuracy=accuracy)
    return accuracy

