"""
# 이 부분은 betterproto 1.x 에서 사용하는 방식입니다.
# 일반적인 상황에서는 betterproto 2.x 을 사용합니다.

import time
import datetime
import grpc

from gps.proto.gps import Response
from gps.proto.gps_pb2_grpc import (
    EvaluationServiceServicer, add_EvaluationServiceServicer_to_server
)

class EvalServiceFromServerA(EvaluationServiceServicer):

    def EvalFromServerA(self, request: Request, context):
        print(request)

        time.sleep(5)
        return Response(
            latency=5.0,
            accuracy=0.9,
            flops=100.0,
            n_params=1000000,
            timestamp=datetime.datetime.now()
        )


def main(port):
    server = grpc.server(futures.ThreadPoolExecutor())
    server.add_insecure_port(f"[::]:{port}")
    add_EvaluationServiceServicer_to_server(EvalServiceFromServerA(), server)
    server.start()
    print(f"Server A started at port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    main(port=50051)
"""
# 내장
import datetime
import asyncio
from pathlib import Path

# 서드파티
import prefect
from prefect.deployments import DeploymentImage
from grpclib.server import Server

# 프로젝트
from gps.server.common.dataset import download_dataset, preprocess
from gps.proto.gps import Request, Response, EvaluationServiceBase


@prefect.flow
def server_a_flow(urls: list[str]) -> Response:
    """ 서버에서 실질적으로 실행해야 하는 로직
    """
    for url in urls:
        download_dataset(url)
    preprocess()
    preprocess()

    return Response(
        latency=5.0,
        accuracy=0.9,
        flops=100.0,
        n_params=1000000,
        timestamp=datetime.datetime.now()
    )


class EvalServiceFromServerA(EvaluationServiceBase):
    """ 이 클래스는 grpc 요청 수신과 응답 이외에는 아무 역할도 하지 않도록 유지관리합니다.
    """

    async def eval_from_server_a(self, request: Request) -> Response:
        print("------------------ Recieved request ------------------")
        for k, v in request.to_dict().items():
            print(f"{k}: {v}")
        print("------------------------------------------------------")
        return server_a_flow(request.data_info.object_storage_urls)


class PrefectDeployerA():
    """ 이 클래스는 prefect 요청 수신과 응답 이외에는 아무 역할도 하지 않도록 유지관리합니다.
    """

    async def deploy(self):
        return await server_a_flow.serve(name=self.__class__.__name__)

    async def deploy_to_workpool(self):
        return await server_a_flow.deploy(
            name=self.__class__.__name__,
            work_pool_name="lock-pool",
            image=DeploymentImage(
                name="my-cusetom-image-for-a",
                tag="v1",
                dockerfile=Path("./dockerfiles/server_a_base.dockerfile"),
                build_kwargs={}
            ),
            push=False
        )


async def main():
    """ 이 함수는 grpc 서버와 prefect 서버 둘 모두를 이벤트 루프에 붙인다.
    덕분에 `server_a_flow` 함수에 접근할 때 `grpc` 와 `prefect` 모두를 이용할 수 있다.
    """

    prefect_future = asyncio.create_task(
        PrefectDeployerA().deploy_to_workpool()
    )
    print("Prefect server started")

    grpc_server = Server([EvalServiceFromServerA()])
    await grpc_server.start("127.0.0.1", 50051)
    print("Server A started at port 50051")

    _ = await asyncio.gather(grpc_server.wait_closed(), prefect_future)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
