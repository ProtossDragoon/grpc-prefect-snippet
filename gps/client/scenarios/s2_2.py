# 내장
import json
import asyncio
import subprocess

# 서드파티
from prefect.deployments import run_deployment

# 프로젝트
from gps.proto.gps import Response
from gps.server.common.colorprint import colorprint


async def main():
    # Create sample requests
    name = "server-b-flow/PrefectDeployerB"
    parameters = {
        "data_info": {
            "object_storage_urls": ["a"],
            "dataset": "b"
        },
    }

    colorprint("prefect python API를 이용해 요청을 시작합니다.")
    colorprint("실행 요청한 플로우가 이미 다른 방법으로 실행 중이라면 스케줄링하고 응답을 대기합니다.")
    response_b = await run_deployment(name=name, parameters=parameters)
    colorprint("응답을 수신했습니다.")
    response_b = response_b.state.result()
    print(repr(response_b))
    colorprint("실질적인 값은 데이터베이스에 저장되어 있습니다. 이 값을 가져옵니다.")
    response_b = await response_b.get()
    print(repr(response_b))
    colorprint("가져온 값은 자동으로 역직렬화됩니다. 가져온 값은 grpc 리턴타입을 가집니다.")
    assert isinstance(response_b, Response)
    # NOTE: 더 궁금하면 https://docs.prefect.io/latest/concepts/results/ 을 참고하세요.

    colorprint("이번에는 prefect CLI를 이용해 요청을 시작합니다.")
    colorprint("`--params` 옵션에 전달될 값을 스트링으로 바꿉니다.")
    json_string = json.dumps(parameters)
    print(repr(json_string))
    args = [
        "prefect",
        "deployment",
        "run",
        f"{name}",
        "--params",
        f"{json_string}",
    ]
    colorprint("최종적으로 실행되는 커맨드는 다음과 같은 형태입니다.")
    print(" ".join(args))
    colorprint("CLI 를 실행하고 stdout 을 출력합니다.")
    response_b = subprocess.run(args, check=False)
    colorprint("비동기적 실행을 완료했습니다. 반환받은 값은 다음과 같습니다.")
    print(response_b)

    return True


if __name__ == "__main__":
    print(f"response_b: {asyncio.run(main())}")
