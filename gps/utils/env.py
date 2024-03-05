# 내장
import os
from dataclasses import dataclass, field, fields


@dataclass
class EnvVarManager:
    """ 환경 변수의 적절성을 검사하고 값을 저장합니다.
    """
    FLOW_DEPLOYMENT_IMAGE_NAME: str = field()
    PREFECT_HOST: str = field(init=False)
    PREFECT_HOST_IN_CONTAINERS: str = field(init=False)
    PREFECT_API_URL_IN_CONTAINERS: str = field(init=False)
    PREFECT_API_DATABASE_CONNECTION_URL_IN_CONTAINERS: str = field(init=False)
    PREFECT_LOCAL_STORAGE_HOST_VOLUME_PATH: str = field(init=False)
    PREFECT_LOCAL_STORAGE_CONTAINER_VOLUME_PATH: str = field(init=False)

    def __post_init__(self):
        for field in fields(self):
            # init 파라미터가 True로 설정된 필드는 자동 초기화에서 제외
            if field.init:
                continue

            # 자동 초기화
            value = os.getenv(field.name)
            if 'PATH' in field.name:  # 경로에 대한 처리
                value = os.path.expanduser(value)
            setattr(self, field.name, value)

            # 값 검사
            value = getattr(self, field.name)
            assert value is not None, f"{field.name} must not be None"
            print(f"{field.name}: {value}")

        # 특정 조건 검사
        if self.PREFECT_HOST_IN_CONTAINERS == 'host.docker.internal':
            assert self.PREFECT_HOST in ['0.0.0.0', 'localhost'], (
                "PREFECT_HOST must be '0.0.0.0' or 'localhost' "
                "if PREFECT_HOST_IN_CONTAINERS is 'host.docker.internal'"
            )

        assert self.PREFECT_LOCAL_STORAGE_HOST_VOLUME_PATH == self.PREFECT_LOCAL_STORAGE_CONTAINER_VOLUME_PATH, (
            'prefect는 자동으로 배포된 환경에서 사용한 스토리지 경로를 가져옵니다. '
            '이는 minio나 S3와 같은 오브젝트 스토리지를 사용할 때 매우 편리합니다. '
            '하지만 도커 환경에서 로컬 볼륨을 스토리지로 사용한다면, '
            '동일한 경로(path)를 사용하지 않는 것이 문제가 됩니다.'
        )
