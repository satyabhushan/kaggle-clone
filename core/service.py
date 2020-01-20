import os
import docker
import json
from django.shortcuts import render
from pathlib import Path
from .models import Competition, Submission
from random import randint
from secrets import token_urlsafe
from .extract_csv_file_data import parse_data, get_dict_from_str_list


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
        user_solution_file_path = "/home/s8/Videos/competition/user-{}/competition-{}/solution.csv".format(
            user_id, competition_id
        )
        with open(user_solution_file_path) as _:

            solution_output = parse_data(user_solution_file_path)
            return solution_output
    except IOError:
        print(1)
        try:
            user_kernel_ipynb_file_path = "/home/s8/Videos/competition/user-{}/competition-{}/Kernel-{}.ipynb".format(
                user_id, competition_id, user_id
            )
            print(user_kernel_ipynb_file_path)
            with open(user_kernel_ipynb_file_path) as ipynb_file:
                data = json.loads(ipynb_file.read())
                try:
                    outputs = data["cells"][-1]["outputs"][0]["text"]
                    solution_output = get_dict_from_str_list(outputs, delemiter=",")
                    print(solution_output)
                    if len(solution_output.keys()) == 0:
                        raise Exception

                    return solution_output
                except Exception:
                    if not data.get("cells"):
                        raise Exception(42, "some other details")
                        # raise "Something failed", (
                        #     "There is some error in <code>Kernel-{}.ipynb</code> file. Please print output in proper format.".format(
                        #         user_id
                        #     ),
                        #     "No output",
                        # )
                    if len(data["cells"]) == 0:
                        raise Exception(
                            "There is no code cell output in <code>Kernel-{}.ipynb</code>. Please check again then submit.".format(
                                user_id
                            ),
                            "No output",
                        )
                    if len(data["cells"][-1].get("outputs")) == 0:
                        raise Exception(
                            "There is no code cell output in <code>Kernel-{}.ipynb</code>. Please check again then submit.".format(
                                user_id
                            ),
                            "No output",
                        )
                    else:
                        raise Exception(
                            "Please print output in proper format.",
                            outputs,
                        )
        except IOError:
            raise Exception(
                "Neither <code>solution.csv</code> or <code>Kernel-{}.ipynb</code> file found.".format(
                    user_id
                ),
                None,
            )
    except Exception:
        with open(user_solution_file_path) as _:
            solution_output = _.read()
            raise Exception(
                "There is some error in <code>solution.csv</code> file. Please upload in proper format.",
                solution_output,
            )


def get_solution_data(competition):
    solution_file_path = "/home/s8/Videos/kaggle_clone/kaggle_clone/media/{}".format(
        competition.test_solution_csv
    )
    with open(solution_file_path) as _:
        solution_output = parse_data(solution_file_path)

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

    accuracy_percentage = correct_ids_len * 100 / keys_len
    return accuracy_percentage


def submit_solution(request, competition, user):

    try:
        user_solution_output = get_user_solution_data(competition.id, user.id)
    except Exception as e:
        print("error", e)
        error = e
        return render(
            request,
            "core/submit_prediction.html",
            {"user": user, "competition": competition, "error": error},
        )

    solution_data = get_solution_data(competition)
    print(user_solution_output, solution_data)
    accuracy = get_accuracy_percentage(solution_data, user_solution_output)
    Submission.objects.filter(competition=competition, competitor=user).update(
        accuracy=accuracy
    )
    print(accuracy)
    return render(
        request,
        "core/submit_prediction.html",
        {
            "user": user,
            "competition": competition,
            "user_solution_output": user_solution_output,
        },
    )

