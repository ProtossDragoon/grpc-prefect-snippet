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
import time
import datetime
import asyncio

from grpclib.server import Server
from gps.proto.gps import Request, Response, EvaluationServiceBase


class EvalServiceFromServerA(EvaluationServiceBase):

    async def eval_from_server_a(self, request: Request) -> Response:
        for k, v in request.to_dict().items():
            print(f"{k}: {v}")

        time.sleep(5)
        return Response(
            latency=5.0,
            accuracy=0.9,
            flops=100.0,
            n_params=1000000,
            timestamp=datetime.datetime.now()
        )


async def main():
    server = Server([EvalServiceFromServerA()])
    await server.start("127.0.0.1", 50051)
    print("Server A started at port 50051")
    await server.wait_closed()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
