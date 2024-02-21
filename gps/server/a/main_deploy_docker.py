# 내장
import os
from pathlib import Path

# 서드파티
import docker
import dotenv
from prefect.deployments import DeploymentImage

# 프로젝트
from gps.server.a.flow import server_a_flow


def build_base_image(image_name: str):
    client = docker.from_env()
    client.images.build(
        path=".",
        dockerfile="dockerfiles/base.dockerfile",
        tag=f"{image_name}",
        rm=True,
        buildargs={
            "BASE_IMAGE": "ubuntu:20.04",
            "PY3_VERSION": "3.9"
        }
    )


def main():
    # 환경변수 값 검사
    FLOW_A_DEPLOYMENT_IMAGE_NAME = os.getenv("FLOW_A_DEPLOYMENT_IMAGE_NAME")
    PREFECT_API_URL_IN_CONTAINERS = os.getenv("PREFECT_API_URL_IN_CONTAINERS")
    PREFECT_LOCAL_STORAGE_PATH = os.getenv("PREFECT_LOCAL_STORAGE_PATH")
    PREFECT_LOCAL_STORAGE_SRC_VOLUME_PATH = os.path.expanduser(
        os.getenv("PREFECT_LOCAL_STORAGE_SRC_VOLUME_PATH")
    )  # 마운팅되는 경로는 반드시 절대경로여야 함.
    PREFECT_LOCAL_STORAGE_DST_VOLUME_PATH = os.path.expanduser(
        os.getenv("PREFECT_LOCAL_STORAGE_DST_VOLUME_PATH")
    )  # 마운팅되는 경로는 반드시 절대경로여야 함.
    assert FLOW_A_DEPLOYMENT_IMAGE_NAME is not None
    assert PREFECT_API_URL_IN_CONTAINERS is not None
    assert PREFECT_LOCAL_STORAGE_PATH is not None
    assert PREFECT_LOCAL_STORAGE_SRC_VOLUME_PATH is not None
    assert PREFECT_LOCAL_STORAGE_DST_VOLUME_PATH is not None
    assert (
        PREFECT_LOCAL_STORAGE_SRC_VOLUME_PATH ==
        PREFECT_LOCAL_STORAGE_DST_VOLUME_PATH
    ), (
        "prefect는 자동으로 배포된 환경에서 사용한 스토리지 경로를 가져옵니다. "
        "이는 minio나 S3와 같은 오브젝트 스토리지를 사용할 때 매우 편리합니다. "
        "하지만 도커 환경에서 로컬 볼륨을 스토리지로 사용한다면, "
        "동일한 경로(path)를 사용하지 않는 것이 문제가 됩니다."
    )

    base_image_name = "server-base"
    build_base_image(base_image_name)
    server_a_flow.deploy(
        name="running-in-container",
        work_pool_name="lock-container-pool",
        work_queue_name="priority",
        # -------------------------
        # NOTE: docker build 과 관련
        image=DeploymentImage(
            name=FLOW_A_DEPLOYMENT_IMAGE_NAME,
            dockerfile="dockerfiles/a.dockerfile",
            rm=True,
            pull=False,
            buildargs={"BASE_IMAGE": base_image_name},
        ),
        # -------------------------
        # NOTE: docker run 과 관련
        job_variables={
            "env":
                {
                    "PREFECT_API_URL":
                        PREFECT_API_URL_IN_CONTAINERS,
                    "PREFECT_LOCAL_STORAGE_PATH":
                        PREFECT_LOCAL_STORAGE_DST_VOLUME_PATH,
                },
            "network":
                "host",  ## NOTE: localhost 에 접근하려면 network 가 `host` 이어야 함.
            "volumes":
                [
                    f"{PREFECT_LOCAL_STORAGE_SRC_VOLUME_PATH}:{PREFECT_LOCAL_STORAGE_DST_VOLUME_PATH}",
                ],  # NOTE: prefect 플로우 API 를 실행하면 파일을 통해 결과를 수신합니다.
            "remove": True,
            "auto_remove": True,
            "mem_limit": "10g",
        },
        # -------------------------
        push=False,
    )


if __name__ == "__main__":
    network_envfile_path = Path("envs/network.env")
    assert os.path.exists(
        network_envfile_path
    ), f"`{network_envfile_path}` 가 존재하지 않습니다."
    docker_envfile_path = Path("envs/docker.env")
    assert os.path.exists(
        docker_envfile_path
    ), f"`{docker_envfile_path}` 가 존재하지 않습니다."
    dotenv.load_dotenv(network_envfile_path)
    dotenv.load_dotenv(docker_envfile_path)
    main()
