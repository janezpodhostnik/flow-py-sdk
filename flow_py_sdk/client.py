import asyncio
from types import TracebackType
from typing import Optional, Type

from grpclib.client import Channel
from grpclib.config import Configuration
from grpclib.encoding.base import CodecBase, StatusDetailsCodecBase
from grpclib.metadata import Deadline

from .proto.flow.access import AccessAPIStub


class _AccessAPI(AccessAPIStub):
    def __init__(self, channel: "Channel", *, timeout: Optional[float] = None, deadline: Optional["Deadline"] = None,
                 metadata = None) -> None:
        super().__init__(channel=channel, timeout=timeout, deadline=deadline, metadata=metadata)

    async def __aenter__(self) -> AccessAPIStub:
        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> None:
        self.channel.close()


def flow_client(
        host: Optional[str] = None,
        port: Optional[int] = None,
        *,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        path: Optional[str] = None,
        codec: Optional[CodecBase] = None,
        status_details_codec: Optional[StatusDetailsCodecBase] = None,
        ssl=None,
        config: Optional[Configuration] = None,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None, metadata=None) -> _AccessAPI:
    channel = Channel(host=host, port=port, loop=loop, path=path, codec=codec,
                      status_details_codec=status_details_codec, ssl=ssl, config=config)

    return _AccessAPI(channel=channel, timeout=timeout, deadline=deadline, metadata=metadata)
