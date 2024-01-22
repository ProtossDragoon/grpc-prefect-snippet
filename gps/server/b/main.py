""" python3 -m gps.server.b.main
"""

# 내장
import asyncio

# 서드파티
import prefect
from grpclib.server import Server

# 프로젝트
from gps.server.common.dbio import db_write
from gps.server.common.computation import heavy_computation
from gps.server.common.dataset import download_dataset, preprocess
from gps.proto.gps import DataInfo, Request, Response, EvaluationServiceBase


@prefect.flow(log_prints=True)
def server_b_flow(data_info: DataInfo) -> Response:
    """ 서버에서 실질적으로 실행해야 하는 로직
    """
    urls = data_info.object_storage_urls
    for url in urls:
        download_dataset(url)
    db_write("content b")
    heavy_computation()
    db_write("global content")
    futures = []
    futures.append(preprocess.submit())
    futures.append(preprocess.submit())
    futures.append(preprocess.submit())
    futures.append(preprocess.submit())
    futures.append(preprocess.submit())
    for future in futures:
        future.result()

    return Response(
        latency=5.0,
        accuracy=1,
        flops=False,
        n_params=2000000,
    )


class EvalServiceFromServerB(EvaluationServiceBase):
    """ 이 클래스는 grpc 요청 수신과 응답 이외에는 아무 역할도 하지 않도록 유지관리합니다.
    """

    async def eval_from_server_b(self, request: Request) -> Response:
        print("------------------ Recieved request ------------------")
        for k, v in request.to_dict().items():
            print(f"{k}: {v}")
        print("------------------------------------------------------")
        return server_b_flow(request.data_info)


class PrefectDeployerB():
    """ 이 클래스는 prefect 요청 수신과 응답 이외에는 아무 역할도 하지 않도록 유지관리합니다.
    """

    async def deploy(self):
        return await server_b_flow.serve(name=self.__class__.__name__)


async def main():
    """ 이 함수는 grpc 서버와 prefect 서버 둘 모두를 이벤트 루프에 붙입니다.
    덕분에 `server_b_flow` 함수에 접근할 때 `grpc` 와 `prefect` 모두를 이용할 수 있습니다.
    """

    prefect_future = asyncio.create_task(PrefectDeployerB().deploy())
    print("Prefect server started")

    grpc_server = Server([EvalServiceFromServerB()])
    await grpc_server.start("127.0.0.1", 50052)
    print("Server A started at port 50052")

    _ = await asyncio.gather(grpc_server.wait_closed(), prefect_future)


if __name__ == "__main__":
    asyncio.run(main())
