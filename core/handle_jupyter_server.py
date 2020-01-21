# from __future__ import absolute_import, unicode_literals
import os
import docker
import time
from pathlib import Path
from random import randint
from secrets import token_urlsafe

# from django.shortcuts import render
from celery import shared_task
from core.models import Submission


def enroll_user(user, competition):
    print(1)
    submission = user.submission_set.filter(competition=competition).first()
    print(2)
    if not submission:
        # task_id = start_jupyter_server.delay({"user":user, "competition": competition})
        task_id = start_jupyter_server.delay(
            user.id,
            {
                "id": competition.id,
                "train_csv": competition.train_csv.name,
                "train_solution_csv": competition.train_solution_csv.name,
                "test_csv": competition.test_csv.name,
            },
        )
        print(11)
        submission = Submission(competitor=user, competition=competition)
        print(12)
        submission.container_path = "task_id=" + str(task_id)
        print(13)
        submission.save()
        print(14)
        return {"jupyter_path": None, "task_status": "STARTING"}

    if submission.container_path:
        jupyter_path = submission.container_path
        if jupyter_path[:7] == "task_id":
            pass  # check task status
            return {"jupyter_path": None, "task_status": "PENDING"}
        else:
            return {"jupyter_path": jupyter_path, "task_status": "SUCCESS"}


@shared_task
def start_jupyter_server(user_id, competition):
    print("hello")
    Path(
        "/home/s8/Videos/competition/user-{}/competition-{}".format(
            user_id, competition["id"]
        )
    ).mkdir(parents=True, exist_ok=True)

    _ = os.system(
        "cp /home/s8/Videos/kaggle_clone/kaggle_clone/media/{} \
            /home/s8/Videos/competition/user-{}/competition-{}/".format(
            competition["train_csv"], user_id, competition["id"]
        )
    )

    _ = os.system(
        "cp /home/s8/Videos/kaggle_clone/kaggle_clone/media/{} \
            /home/s8/Videos/competition/user-{}/competition-{}/".format(
            competition["train_solution_csv"], user_id, competition["id"]
        )
    )

    _ = os.system(
        "cp /home/s8/Videos/kaggle_clone/kaggle_clone/media/{} \
            /home/s8/Videos/competition/user-{}/competition-{}/".format(
            competition["test_csv"], user_id, competition["id"]
        )
    )

    _ = os.system(
        "cp /home/s8/Videos/kaggle_clone/kaggle_clone/Kernel.ipynb \
            /home/s8/Videos/competition/user-{}/competition-{}/Kernel-{}.ipynb".format(
            user_id, competition["id"], user_id,
        )
    )

    print("t1", time)

    client = docker.from_env().api
    volumes = [
        "/home/s8/Videos/competition/user-{}/competition-{}".format(
            user_id, competition["id"]
        )
    ]
    volume_bindings = {
        "/home/s8/Videos/competition/user-{}/competition-{}".format(
            user_id, competition["id"]
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
        image="comp:1.0",
        volumes=volumes,
        ports=[8888],
        host_config=host_config,
        command=command,
    )

    print("t2", time)

    container_id = container.get("Id")
    client.start(container=container_id)

    client = docker.from_env()

    submission = Submission.objects.get(
        competition__id=competition["id"], competitor__id=user_id
    )
    submission.container_id = container_id
    submission.port = port
    submission.container_path = "127.0.0.1:{}/notebooks/Kernel-{}.ipynb?token={}".format(
        port, user_id, jupyter_access_token
    )
    print("t3", time)

    time.sleep(5)
    submission.save()
    print(submission)
    print("t4", time)

    return submission.container_path
