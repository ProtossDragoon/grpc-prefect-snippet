"""
# 이 부분은 betterproto 1.x 에서 사용하는 방식입니다.
# 일반적인 상황에서는 betterproto 2.x 을 사용합니다.

import time
import grpc

from gps.proto.gps import Response
from gps.proto.gps_pb2_grpc import (
    EvaluationServiceServicer, add_EvaluationServiceServicer_to_server
)

class EvalServiceFromServerB(EvaluationServiceServicer):

    def EvalFromServerB(self, request: Request, context):
        print(request)

        time.sleep(7)
        return Response(
            latency=5.0,
            accuracy=1,
            flops=False,
            n_params=2000000,
        )


def main(port):
    server = grpc.server(futures.ThreadPoolExecutor())
    server.add_insecure_port(f"[::]:{port}")
    add_EvaluationServiceServicer_to_server(EvalServiceFromServerB(), server)
    server.start()
    print(f"Server A started at port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    main(port=50052)
"""
import time
import asyncio

from grpclib.server import Server
from gps.proto.gps import Request, Response, EvaluationServiceBase


class EvalServiceFromServerB(EvaluationServiceBase):

    async def eval_from_server_b(self, request: Request) -> Response:
        for k, v in request.to_dict().items():
            print(f"{k}: {v}")

        time.sleep(7)
        return Response(
            latency=5.0,
            accuracy=1,
            flops=False,
            n_params=2000000,
        )


async def main():
    server = Server([EvalServiceFromServerB()])
    await server.start("127.0.0.1", 50052)
    print("Server B started at port 50052")
    await server.wait_closed()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
