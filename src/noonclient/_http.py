
import inspect
from types import TracebackType
from typing import Any, Callable, Optional, Type
import typing


import aiohttp
from aiohttp.client import ClientSession, _RequestContextManager
from aiohttp.client_reqrep import ClientResponse
from aiohttp.typedefs import LooseHeaders, StrOrURL

import makefun

from yarl import URL
import noonclient._serialization
import noonclient.alaska.kush


def create_request(method: str, url: StrOrURL):
    def request(self, *args, **kwargs: Any) -> _RequestContextManager:
        return self._session.request(method, URL(self._base_url).join(URL(url)), **kwargs)
    return request


def create_replace(method: str, url: StrOrURL):
    def replace(func):
        type_hints = typing.get_type_hints(func)

        request = create_request(method, url)

        def create_request_with_body(request: Callable[[Any, dict[str, Any]], _RequestContextManager]):
            def request_with_json(self, *args, **kwargs: Any):
                kwargs['json'] = args[0]
                return request(self, *args[1::], **kwargs)
            return request_with_json

        def created_typed_response(request):
            async def request_typed_response(self, *args, **kwargs: Any):
                async with request(self, *args, **kwargs) as response:
                    return await response.json(loads=noonclient._serialization._get_loads(type_hints['return']))
            return request_typed_response

        if type_hints['return'] is not ClientResponse:
            request = created_typed_response(request)

        if len(type_hints) == 2:
            request = create_request_with_body(request)

        return request

    return replace


def add_request_params(func: Callable, d: dict):
    if not hasattr(func, '_request_params'):
        func._request_params = dict()
    func._request_params.update(d)
    return func


def headers(headers: Optional[LooseHeaders]):
    def apply_params(func):
        if hasattr(func, '_request_params') and 'headers' in func._request_params:
            func._request_params.headers.extend(headers)
        else:
            add_request_params(func, {'headers': headers})
        return func
    return apply_params


def get(url: StrOrURL):
    def apply_params(func):
        add_request_params(func, {'method': aiohttp.hdrs.METH_GET, 'url': url})
        return func
    return apply_params


def post(url: StrOrURL):
    def apply_params(func):
        add_request_params(func, {'method': aiohttp.hdrs.hdrs.METH_POST, 'url': url})
        return func
    return apply_params


def put(url: StrOrURL):
    def apply_params(func):
        add_request_params(func, {'method': aiohttp.hdrs.hdrs.METH_PUT, 'url': url})
        return func
    return apply_params


_session = aiohttp.ClientSession(
    raise_for_status=True, json_serialize=_json_seralize)


async def __aenter__(self) -> "ServiceActivator":
    return self

async def __aexit__(
    self,
    exc_type: Optional[Type[BaseException]],
    exc_val: Optional[BaseException],
    exc_tb: Optional[TracebackType],
) -> Optional[bool]:
    await self.close()

async def close(self) -> None:
    return await self._session.close()

class ServiceProvider:

    def __init__(self):
        self._session = aiohttp.ClientSession(
            raise_for_status=True, json_serialize=_json_seralize)

    def activate(self, service: Type, base_url):

        def __init__(self, session: ClientSession):
            self._session = session

        members = {
            "__init__": __init__,
            # "__aenter__": __aenter__,
            # "__aexit__": __aexit__,
            "_base_url": 'https://finn.api.noonhome.com',
            # "close": close
        }
        

        def isabstractrequest(obj):
            return hasattr(obj, '_request_params')

        for funcname, func in inspect.getmembers(service, predicate=isabstractrequest):
            def create_request_func():
                d = dict(func._request_params)
                def request(self, *args, **kwargs):
                    return self._session.request(hdrs.METH_GET, "http://google.com")
                return request

            newfunc = makefun.create_function(inspect.signature(func), create_request_func(),
                                            funcname, doc=func.__doc__, module_name=func.__module__, qualname=func.__qualname__)
    
            members[funcname] = newfunc

        return type("Test1", (service, ), members)(self._session)

    def providefinnService():
