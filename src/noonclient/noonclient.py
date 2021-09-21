from types import TracebackType
from typing import Optional, Type, Union
import random
import aiohttp
from aiohttp import hdrs
from aiohttp.client_exceptions import ClientResponseError
from noonclient.alaska.model import NoonDexResponse, NoonEndpoints, \
    NoonLoginRequest, \
    NoonLoginResponse, NoonModel, \
    NoonSetLineLightLevelRequest, \
    NoonSetLineLightsOnRequest, \
    NoonViper
from noonclient.alaska.model import NoonLoginResponse
from noonclient._serialization import _json_seralize, _get_loads
from noonclient.alaska.kush import GraphQLGenerator


class NoonClient:
    _PING = "{\"ping\":\"milk shake\"}"

    _NOON_MODEL_GRAPHQL_STRING = GraphQLGenerator.generate(NoonModel)

    def __init__(self):
        self.__token: str = None
        self.__session = aiohttp.ClientSession(
            raise_for_status=True, json_serialize=_json_seralize)
        self.__endpoints: NoonEndpoints = None
        self.__transactionid: int = random.randrange(1073741823) + 1000

    async def __aenter__(self) -> "NoonClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        await self.close()

    async def close(self) -> None:
        return await self.__session.close()

    async def __authrequest(self, method, url, **kwargs):
        raise_for_status: Union[bool,
                                None] = kwargs['raise_for_status'] if 'raise_for_status' in kwargs else None

        kwargs = dict(kwargs)
        if 'headers' not in kwargs:
            kwargs['headers'] = dict()

        kwargs['headers']['Authorization'] = 'Token ' + self.__token
        kwargs['raise_for_status'] = True

        try:
            return await self.__session.request(method, url, **kwargs)
        except ClientResponseError as err:
            if err.status != 401:
                raise err

            await self._renew_token_sync()

            kwargs['headers']['Authorization'] = 'Token ' + self.__token
            del kwargs['raise_for_status']
            if raise_for_status is not None:
                kwargs['raise_for_status'] = raise_for_status

            return await self.__session.request(method, url, **kwargs)

    async def login(self, email: str, password: str) -> NoonLoginResponse:
        async with self.__session.post('https://finn.api.noonhome.com/api/login', json=NoonLoginRequest(email, password)) as response:
            loginresponse: NoonLoginResponse = await response.json(loads=_get_loads(NoonLoginResponse))
            self.__token = loginresponse.token
            async with await self.__authrequest(hdrs.METH_GET, 'https://dex.api.noonhome.com/api/endpoints') as response:
                self.__endpoints = (await response.json(loads=_get_loads(NoonDexResponse))).endpoints

            return loginresponse

    async def _renew_token_sync(self) -> None:
        if self.__token is not None:
            async with self.__session.post('https://finn.api.noonhome.com/api/token/renew', json=NoonLoginResponse(self.__token)) as response:
                self.__token = await response.json(
                    loads=_get_loads(NoonLoginResponse)).token

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, token: str):
        self.__token = token

    @property
    def endpoints(self):
        return self.__endpoints

    @endpoints.setter
    def endpoints(self, endpoints: NoonEndpoints):
        self.__.endpoints = endpoints

    async def fetch_model(self) -> NoonModel:
        headers = {'Content-Type': 'application/graphql'}
        async with await self.__authrequest(hdrs.METH_POST, self.__endpoints.query + '/api/query', data=self._NOON_MODEL_GRAPHQL_STRING, headers=headers) as response:
            return await response.json(loads=_get_loads(NoonModel))

    async def query_space(self, guid: str) -> NoonModel:
        headers = {'Content-Type': 'application/graphql'}
        async with await self.__authrequest(hdrs.METH_POST, self.__endpoints.query + '/api/query', data='{ spaces (guid: ' + guid + ') { name, icon, guid, type, lightsOn, lightingConfigModified, devices { name, guid, type, isMaster, isOnline, serial, displayName, softwareVersion, expectedSoftwareVersion, batteryLevel, expectedLinesGuid, actualLinesGuid, expectedScenesGuid, actualScenesGuid, scenesAllowed, line { guid, preconfigured }, otaState { guid, type, retryCount, installState, percentDownloaded }, base { guid, firmwareVersion, serial, capabilities { dimming, powerRating } }, capabilities { iconSet, maxScenes, hue, gridView, dimmingBase, dimming, wholeHomeScenes } }, lines {  guid, displayName, lineState, dimmingLevel, dimmable, remoteControllable, preconfigured, bulbType, multiwayMaster { guid }, lights { guid, fixtureType, bulbBrand, bulbQuantity }, externalDevices { externalId, isOnline} }, subspaces { guid, name, lines { guid }, type }, sceneOrder,  activeSceneSchedule { guid }, scenes { guid, icon, name, type, isActive, lightLevels { recommendedMax, recommendedMin, value, lineState, line { guid, lineState, dimmingLevel, displayName, bulbType, remoteControllable } } }, activeScene { guid, name, icon } } }', headers=headers) as response:
            return await response.json(loads=_get_loads(NoonModel))

    async def set_line_light_level(self, noon_set_line_light_level_request: NoonSetLineLightLevelRequest) -> None:
        self.__transactionid += 1
        noon_set_line_light_level_request.tid = self.__transactionid
        await self.__authrequest(hdrs.METH_POST, self.__endpoints.action + '/api/action/line/lightLevel', json=noon_set_line_light_level_request)

    async def set_line_lights_on(self, noon_set_line_lights_on_request: NoonSetLineLightsOnRequest) -> None:
        self.__transactionid += 1
        noon_set_line_lights_on_request.tid = self.__transactionid
        await self.__authrequest(hdrs.METH_POST, self.__endpoints.action + '/api/action/line/lightsOn', json=noon_set_line_lights_on_request)

    async def _listen(self):
        async with self.__session.ws_connect(self.__endpoints.notification_ws + '/api/notifications', headers={'Authorization': 'Token ' + self.__token}) as ws:
            await ws.ping(NoonClient._PING)
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.PONG:
                    pass
                if "notification" in msg.data:
                    noon_viper: NoonViper = msg.json(
                        loads=_get_loads(NoonViper))
                    for change in noon_viper.data.changes:
                        yield change

    async def listen(self):
        try:
            async for change in self._listen():
                yield change
        except ClientResponseError as err:
            if err.status != 401:
                raise err

            await self._renew_token_sync()

            async for change in self._listen():
                yield change
