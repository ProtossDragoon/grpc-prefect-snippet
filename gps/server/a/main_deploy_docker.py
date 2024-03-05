# 내장
import os
from pathlib import Path

# 서드파티
import docker
import dotenv
from prefect.deployments import DeploymentImage

# 프로젝트
from gps.utils.env import EnvVarManager
from gps.server.a.flow import server_a_flow


def build_base_image(image_name: str):
    client = docker.from_env()
    client.images.build(
        path='.',
        dockerfile='dockerfiles/base.dockerfile',
        tag=f'{image_name}',
        rm=True,
        buildargs={
            'BASE_IMAGE': 'ubuntu:20.04',
            'PY3_VERSION': '3.9'
        }
    )


def main(env: EnvVarManager):
    base_image_name = 'server-base'
    build_base_image(base_image_name)
    server_a_flow.deploy(
        name='running-in-container',
        work_pool_name='lock-container-pool',
        work_queue_name='priority',
        # -------------------------
        # NOTE: docker build 관련
        image=DeploymentImage(
            name=env.FLOW_DEPLOYMENT_IMAGE_NAME,
            dockerfile='dockerfiles/a.dockerfile',
            rm=True,
            pull=False,
            buildargs={'BASE_IMAGE': base_image_name},
        ),
        # -------------------------
        # NOTE: docker run 관련
        job_variables={
            'env':
                {
                    'PREFECT_API_URL':
                        env.PREFECT_API_URL_IN_CONTAINERS,
                    'PREFECT_LOCAL_STORAGE_PATH':
                        env.PREFECT_LOCAL_STORAGE_CONTAINER_VOLUME_PATH,
                    'PREFECT_API_DATABASE_CONNECTION_URL':
                        env.PREFECT_API_DATABASE_CONNECTION_URL_IN_CONTAINERS,
                },
            'network': 'host',  # NOTE: localhost에 접근하려면 network가 `host`이어야 함.
            'volumes':
                [
                    f"{env.PREFECT_LOCAL_STORAGE_HOST_VOLUME_PATH}:{env.PREFECT_LOCAL_STORAGE_CONTAINER_VOLUME_PATH}",
                ],  # NOTE: prefect 플로우 API를 실행하면 파일을 통해 결과를 수신합니다.
            'mem_limit': '10g',
        },
        # -------------------------
        push=False,
    )


if __name__ == '__main__':
    envfile = Path('.env')
    assert os.path.exists(envfile), f'`{envfile}` 가 존재하지 않습니다.'
    dotenv.load_dotenv(envfile)
    env = EnvVarManager(os.getenv('FLOW_A_DEPLOYMENT_IMAGE_NAME'))
    main(env)
