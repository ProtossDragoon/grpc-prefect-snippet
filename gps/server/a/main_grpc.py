""" python3 -m gps.server.a.main_grpc
"""

# 내장
import asyncio

# 서드파티
from grpclib.server import Server

# 프로젝트
from gps.server.a.flow import server_a_flow
from gps.proto.gps import Request, Response, EvaluationServiceBase


class EvalServiceFromServerA(EvaluationServiceBase):
    """ 이 클래스는 grpc 요청 수신과 응답 이외에는 아무 역할도 하지 않도록 유지관리합니다.
    """

    async def eval_from_server_a(self, request: Request) -> Response:
        print("------------------ Recieved request ------------------")
        for k, v in request.to_dict().items():
            print(f"{k}: {v}")
        print("------------------------------------------------------")
        return Response(**server_a_flow(request))


async def main():
    grpc_server = Server([EvalServiceFromServerA()])
    await grpc_server.start("127.0.0.1", 50051)
    print("Server A started at port 50051")
    await grpc_server.wait_closed()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
