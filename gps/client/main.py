# 내장
import asyncio

# 서드파티
from grpclib.client import Channel

# 프로젝트
from gps.proto.gps import ModelInfo, DataInfo, Request, EvaluationServiceStub


async def main():
    # Create sample requests
    model_info = ModelInfo(
        model_registry_urls=["http://example.com/model"], task="classification"
    )
    data_info = DataInfo(
        object_storage_urls=["http://example.com/data"], dataset="sample"
    )

    # Create a gRPC channel and a stub for each server
    channel_a = Channel("localhost", 50051)
    stub_a = EvaluationServiceStub(channel_a)
    response_a = await stub_a.eval_from_server_a(
        Request(
            model_info=model_info,
            data_info=data_info,
            author="John Doe",
            device="Device X",
            description="Sample description"
        )
    )
    print(f"Response from Server A: {response_a.to_dict()}")

    channel_b = Channel("localhost", 50052)
    stub_b = EvaluationServiceStub(channel_b)
    response_b = await stub_b.eval_from_server_b(
        Request(
            model_info=model_info,
            data_info=data_info,
            author="John Doe",
            device="Device X",
            description="Sample description"
        )
    )
    print(f"Response from Server B: {response_b.to_dict()}")

    channel_a.close()
    channel_b.close()


if __name__ == "__main__":
    asyncio.run(main())
