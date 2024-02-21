# 내장
import asyncio

# 서드파티
from grpclib.client import Channel

# 프로젝트
from gps.proto.gps import (
    ModelInfo,
    DataInfo,
    Request,
    EvaluationServiceStub,
)


async def main():
    # Create sample requests
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

    channel_a = Channel("localhost", 50051)
    stub_a = EvaluationServiceStub(channel_a)

    print("요청을 시작합니다.")
    response_a = asyncio.create_task(
        stub_a.eval_from_server_a(
            Request(
                model_info=model_info,
                data_info=data_info,
                author="John Doe",
                device="Device X",
                description="Sample description"
            )
        )
    )
    print("비동기적 요청이 끝났습니다. 응답을 대기합니다.")
    response_a = await response_a

    channel_a.close()
    print("통신이 끝났습니다. grpc 채널을 닫습니다.")
    return response_a


if __name__ == "__main__":
    print(f"response_a: {asyncio.run(main())}")
