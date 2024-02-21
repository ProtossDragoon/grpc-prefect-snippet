# 내장
from pprint import pprint
import asyncio

# 서드파티
from prefect.deployments import run_deployment
from betterproto import Casing

# 프로젝트
from gps.proto.gps import (
    ModelInfo,
    DataInfo,
    Request,
)
from gps.server.common.colorprint import colorprint
from gps.server.common.errors import PrefectException


async def main():
    # Create sample requests
    name = "server-a-flow/running-in-container"
    model_info = ModelInfo(
        model_registry_urls=[
            "http://example.com/model_1",
            "http://example.com/model_2",
        ],
        task="classification"
    )
    data_info = DataInfo(
        object_storage_urls=[
            "http://example.com/data_a",
            "http://example.com/data_b",
            "http://example.com/data_c",
        ],
        dataset="sample"
    )
    request = Request(
        model_info=model_info,
        data_info=data_info,
        author="John Doe",
        device="Device X",
        description="Sample description"
    )
    colorprint("prefect python API 호출을 위해 데이터클래스를 JSON 직렬화합니다.")
    request = request.to_dict(casing=Casing.SNAKE, include_default_values=True)
    parameters = {"request": request}
    pprint(parameters)

    colorprint("prefect python API를 이용해 요청을 시작합니다.")
    colorprint("실행 요청한 플로우가 이미 다른 방법으로 실행 중이라면 스케줄링하고 응답을 대기합니다.")
    response_a = await run_deployment(name=name, parameters=parameters)
    colorprint("응답을 수신했습니다.")
    response_a = response_a.state.result()
    print(repr(response_a))
    colorprint("실질적인 값은 데이터베이스에 저장되어 있습니다. 이 값을 가져옵니다.")
    try:
        response_a = await response_a.get()
    except AttributeError as e:
        raise PrefectException from e
    colorprint("가져온 값은 자동으로 역직렬화됩니다. 가져온 값은 플로우의 리턴 타입을 그대로 따릅니다.")
    print(repr(response_a))
    assert isinstance(response_a, dict)

    return response_a


if __name__ == "__main__":
    print(f"response_a: {asyncio.run(main())}")
