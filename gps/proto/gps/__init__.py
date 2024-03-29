# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: gps/proto/gps.proto
# plugin: python-betterproto
# This file has been @generated

from dataclasses import dataclass
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
)

import betterproto
import grpclib
from betterproto.grpc.grpclib_server import ServiceBase


if TYPE_CHECKING:
    import grpclib.server
    from betterproto.grpc.grpclib_client import MetadataLike
    from grpclib.metadata import Deadline


@dataclass(eq=False, repr=False)
class ModelInfo(betterproto.Message):
    model_registry_urls: List[str] = betterproto.string_field(1)
    task: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class DataInfo(betterproto.Message):
    object_storage_urls: List[str] = betterproto.string_field(1)
    dataset: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class Request(betterproto.Message):
    model_info: "ModelInfo" = betterproto.message_field(1)
    data_info: "DataInfo" = betterproto.message_field(2)
    author: str = betterproto.string_field(3)
    device: str = betterproto.string_field(4)
    description: str = betterproto.string_field(5)


@dataclass(eq=False, repr=False)
class Response(betterproto.Message):
    latency: float = betterproto.float_field(1)
    accuracy: float = betterproto.float_field(2)
    flops: float = betterproto.float_field(3)
    n_params: int = betterproto.int32_field(4)
    timestamp: datetime = betterproto.message_field(5)


class EvaluationServiceStub(betterproto.ServiceStub):
    async def eval_from_server_a(
        self,
        request: "Request",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "Response":
        return await self._unary_unary(
            "/gps.EvaluationService/EvalFromServerA",
            request,
            Response,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def eval_from_server_b(
        self,
        request: "Request",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "Response":
        return await self._unary_unary(
            "/gps.EvaluationService/EvalFromServerB",
            request,
            Response,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class EvaluationServiceBase(ServiceBase):
    async def eval_from_server_a(self, request: "Request") -> "Response":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def eval_from_server_b(self, request: "Request") -> "Response":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_eval_from_server_a(
        self, stream: "grpclib.server.Stream[Request, Response]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.eval_from_server_a(request)
        await stream.send_message(response)

    async def __rpc_eval_from_server_b(
        self, stream: "grpclib.server.Stream[Request, Response]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.eval_from_server_b(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/gps.EvaluationService/EvalFromServerA": grpclib.const.Handler(
                self.__rpc_eval_from_server_a,
                grpclib.const.Cardinality.UNARY_UNARY,
                Request,
                Response,
            ),
            "/gps.EvaluationService/EvalFromServerB": grpclib.const.Handler(
                self.__rpc_eval_from_server_b,
                grpclib.const.Cardinality.UNARY_UNARY,
                Request,
                Response,
            ),
        }
