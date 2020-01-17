import os
import docker
from pathlib import Path
from .models import Competition, Submission
from random import randint


def check_previous_session():
    pass


def start_jupyter_server(user, competition):
    try:
        submission = Submission.objects.get(competitor=user, competition=competition)
        return submission.container_path
    except:

        path = "/home/s8/Videos/competition"
        # Path("/home/s8/Videos/competition/user-{}".format(user.id)).mkdir(parents=True, exist_ok=True)
        # os.mkdir("/home/s8/Videos/competition/user-{}".format(user.id))
        Path(
            "/home/s8/Videos/competition/user-{}/competition-{}".format(
                user.id, competition.id
            )
        ).mkdir(parents=True, exist_ok=True)
        os.system(
            "cp /home/s8/Videos/kaggle_clone/media/{}  /home/s8/Videos/competition/user-{}/competition-{}/".format(
                competition.train_csv, user.id, competition.id
            )
        )
        # os.system(
        #     "cp /home/s8/Videos/kaggle_clone/media/dataset/{}  /home/s8/Videos/competition/user-{}/competition-{}".format(
        #         competition.train_solution_csv, user.id, competition.id
        #     )
        # )
        # os.system(
        #     "cp /home/s8/Videos/kaggle_clone/media/dataset/{}  /home/s8/Videos/competition/user-{}/competition-{}".format(
        #         competition.test_csv, user.id, competition.id
        #     )
        # )
        # os.system(
        #     "cp /home/s8/Videos/kaggle_clone/media/dataset/{}  /home/s8/Videos/competition/user-{}/competition-{}".format(
        #         competition.hidden_test_csv, user.id, competition.id
        #     )
        # )
        
        # os.system(
        #     "docker run -p 8888:8888 --mount type=bind,source=/home/s8/Videos/competition/user-{}/competition-{},target=/usr/src/code -d comp:latest > /home/s8/Videos/kaggle_clone/docker/docker_id.txt".format(
        #         user.id, competition.id
        #     )
        # )

        # f = open('/home/s8/Videos/kaggle_clone/docker/docker_id.txt')
        # docker_id = f.read()
        # f.close()

        client = docker.from_env().api
        volumes = [
            "/home/s8/Videos/competition/user-{}/competition-{}".format(
                user.id, competition.id
            )
        ]
        volume_bindings = {
            "/home/s8/Videos/competition/user-{}/competition-{}".format(
                user.id, competition.id
            ): {"bind": "/usr/src/code", "mode": "rw",},
        }

        port = randint(9999, 65535)
        host_config = client.create_host_config(
            binds=volume_bindings, port_bindings={8888: port}
        )

        container = client.create_container(
            image="comp:latest", volumes=volumes, ports=[8888], host_config=host_config,
        )

        container_id = container.get("Id")
        response = client.start(container=container_id)

        client = docker.from_env()

        submission = Submission(competitor=user, competition=competition)
        submission.container_id = container_id
        submission.port = port
        submission.container_path = '127.0.0.1:'+str(port)
        submission.save()

        return submission.container_path