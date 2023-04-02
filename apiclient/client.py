from abc import ABC
from dataclasses import dataclass
from typing import Generic, Literal, Type, TypeVar

import aiohttp
import vcr
from vcr.record_mode import RecordMode


@dataclass
class ClientConfig:
    base_url: str
    league: str
    language: str
    verbose: bool
    timeout_seconds: int = 300
    use_vcr: bool = False
    vcr_outpath: str = "out/apiclient.vcr"
    raise_errors: bool = False


_TData = TypeVar("_TData")


@dataclass
class RequestConfig(Generic[_TData]):
    method: Literal["GET", "POST"]
    url: str
    path: str
    params: dict[str, str]
    response_type: Type[_TData]


@dataclass
class SuccessResponse(Generic[_TData]):
    data: _TData


@dataclass
class ErrorResponse:
    msg: str


_TModel = TypeVar("_TModel")
_TConfig = TypeVar("_TConfig", bound=ClientConfig)


class Client(ABC, Generic[_TConfig]):
    __session: aiohttp.ClientSession | None = None
    _config: _TConfig

    def __init__(self, cfg: _TConfig) -> None:
        self._config = cfg
        print(f"Init with config: {self._config}")

    @property
    def config(self):
        return self._config

    def build_get_config(
        self,
        path: str,
        model: Type[_TModel],
        params: dict[str, str],
    ) -> RequestConfig[_TModel]:
        return RequestConfig("GET", self._config.base_url, path, params, model)

    async def request(
        self, cfg: RequestConfig[_TModel]
    ) -> SuccessResponse[_TModel] | ErrorResponse:
        async def do_request():
            if not self.__session:
                self.__session = aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=self._config.timeout_seconds),
                )

            try:
                async with self.__session.request(
                    method=cfg.method, url=cfg.url + cfg.path, params=cfg.params
                ) as res:
                    if self._config.verbose:
                        print("Response Details")
                        print("---------------")
                        print(f"Code = {res.status}")
                        print(f"Reason = {res.reason}")
                        print(f"Text = {await res.text()}")
                        print(f"Request = {res.request_info}")

                    if not str(res.status).startswith("2"):
                        raise Exception(f"Request error: {res}", res.request_info)

                    return SuccessResponse(cfg.response_type(await res.json()))
            except Exception as e:
                if self._config.raise_errors:
                    raise e

                if self._config.verbose:
                    print(e)
                return ErrorResponse(str(e))

        if self._config.use_vcr:
            with vcr.use_cassette(
                self._config.vcr_outpath, record_mode=RecordMode.NEW_EPISODES
            ):
                return await do_request()
        return await do_request()
