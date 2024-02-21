# 내장
import os
from pathlib import Path

# 서드파티
import dotenv
from prefect.runner.storage import GitRepository

# 프로젝트
from gps.server.a.flow import server_a_flow


def main():
    server_a_flow.from_source(
        source=GitRepository(
            url="https://github.com/ProtossDragoon/grpc-prefect-snippet.git",
            credentials=None,
        ),
        entrypoint="gps/server/a/flows/__init__.py:server_a_flow"
    ).deploy(
        name="running-in-subprocess",
        work_pool_name="lock-pool",
        work_queue_name="priority"
    )


if __name__ == "__main__":
    envfile_path = Path("envs/network.env")
    assert os.path.exists(envfile_path), f"`{envfile_path}` 가 존재하지 않습니다."
    dotenv.load_dotenv(envfile_path)
    main()
