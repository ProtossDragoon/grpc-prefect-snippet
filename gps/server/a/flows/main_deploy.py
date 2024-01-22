""" python3 -m gps.server.a.flows.main_deploy
"""

# 내장
import os
from pathlib import Path

# 서드파티
import dotenv
from prefect.deployments import DeploymentImage

# 프로젝트
from gps.server.a.flows import main_flow

# NOTE: before running this, you need to create the pool
# named `work_pool_name` it for the first time
# e.g. prefect work-pool create lock-container-pool --type docker
# NOTE: next, you also need to create worker.
# e.g. prefect worker start --pool "lock-container-pool" --work-queue "priority"

if __name__ == "__main__":
    dotenv.load_dotenv(Path("./.env"))  # NOTE: '.': project root
    main_flow.deploy(
        name="PrefectDeployerA",
        work_pool_name="lock-container-pool",
        work_queue_name="priority",
        # NOTE: docker build ... 에 해당하는 부분으로, 이 코드가 실행되는 순간 실행됨.
        image=DeploymentImage(
            name="my-cusetom-image-for-a",
            tag="v1",
            dockerfile="./dockerfiles/server_a_infra.dockerfile",
            buildargs={
                "BASE_IMAGE":
                    # TODO: 동적으로 이미지를 변경할 수 있어야 함
                    "prefecthq/prefect:2.14-python3.11-conda"
            },
        ),
        # NOTE: docker run ... 에 해당하는 부분으로, `deployment run ...` 이 호출될 때 실행됨.
        job_variables={
            "env": # --env ...
                {
                    # FIXME: 포트번호를 환경변수에서 읽어올 수 있어야 함
                    "PREFECT_API_URL": os.getenv("PREFECT_API_URL")
                },
            # NOTE: localhost 에 접근하려면 network 가 `host` 이어야 함.
            "network": "host", # --network ...
        },
        push=False
    )
