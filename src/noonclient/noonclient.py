import asyncio
from datetime import datetime, time
from types import TracebackType
from typing import Any, Optional, Type, Union
import random
import aiohttp
from aiohttp import hdrs
from aiohttp.client_exceptions import ClientResponseError
from aiohttp.client_reqrep import ClientResponse
from aiohttp.typedefs import StrOrURL
from noonclient.alaska.model import NoonChange, NoonChangeSceneRequest, \
    NoonChangeWholeHomeSceneRequest, \
    NoonDexResponse, \
    NoonEndpoints, \
    NoonGeofenceEvent, \
    NoonLease, \
    NoonLightsOnStructureRequest, \
    NoonLoginRequest, \
    NoonLoginResponse, \
    NoonModel, NoonSetDeviceModeRequest, \
    NoonSetLineLightLevelRequest, \
    NoonSetLineLightsOnRequest, \
    NoonStructure, \
    NoonViper, \
    NoonChangeLightsOnRequest
from noonclient.alaska.model import NoonLoginResponse
from noonclient._serialization import _json_seralize, _get_loads, deserializednames
from noonclient.alaska.kush import GraphQLGenerator


class NoonClient:
    _PING = '{"ping":"milk shake"}'
    __noon_model_query: str = None
    __noon_endpoints: NoonEndpoints = None

    @staticmethod
    def get_endpoints():
        return NoonClient.__noon_endpoints

    @staticmethod
    def set_endpoints(noon_endpoints):
        NoonClient.__noon_endpoints = noon_endpoints

    def __init__(self):
        self.__session = aiohttp.ClientSession(
            raise_for_status=True, json_serialize=_json_seralize)

        self.__noon_user_query = "{ user { guid, name, emailValid, incomingInvitations { guid, type, token, structure { guid }, state }, outgoingInvitations { guid, type, token, structure { guid }, state } }, preferences { key, value } }"
        self.noon_basic_lease_query = "{ leases { grants, structure { guid, name, icon, vacationMode { enabled }, nightLightMode { enabled }, scenes { guid, name, type }, spaces { guid, name, icon, type, lightsOn, lines { guid, bulbType, preconfigured, lights { fixtureType }, multiwayMaster { guid } }, activeScene { guid }, scenes { guid, name, icon }, devices { guid, type, isMaster, isOnline, capabilities { wholeHomeScenes } } } } } }"
        # self.__noon_lease_query = "{ leases { grants, structure { guid, name, icon, vacationMode { enabled }, nightLightMode { enabled }, scenes { guid, name }, spaces { guid, name, type, lightsOn, lines { guid, bulbType, lights { fixtureType } }, activeScene { guid }, scenes { guid, name, icon }, devices { guid, type, isMaster, isOnline } } } } }"

        self.__transactionid: int = random.randrange(1073741823) + 1000
        self.__startid: int = self.__transactionid

        NoonClient.__noon_model_query = GraphQLGenerator.generate(NoonModel)

        self.__token: str = None

    def _is_our_transaction(self, i: int):
        return self.__startid <= i and self.__transactionid - 1 >= i

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

    async def __authrequest(self, method: str, url: StrOrURL, **kwargs: Any):
        raise_for_status: Union[bool, None] = kwargs.get(
            'raise_for_status', None)

        kwargs = dict(kwargs)
        if 'headers' not in kwargs:
            kwargs['headers'] = dict()

        renew_token = True
        while(True):
            kwargs['headers']['Authorization'] = 'Token ' + self.__token
            if renew_token:
                kwargs['raise_for_status'] = False
            elif raise_for_status is None:
                del kwargs['raise_for_status']
            elif raise_for_status:
                kwargs['raise_for_status'] = True

            response = await self.__session.request(method, url, **kwargs)
            if not renew_token or response.status != 401:
                if renew_token and raise_for_status:
                    response.raise_for_status()
                return response

            await self.renew_token_sync()
            renew_token = False

    async def renew_token(self, noon_login_response: NoonLoginResponse) -> NoonLoginResponse:
        async with self.__session.post('https://finn.api.noonhome.com/api/token/renew', json=noon_login_response) as response:
            return await response.json(loads=_get_loads(NoonLoginResponse))

    async def renew_token_sync(self) -> None:
        if self.__token is not None:
            self.__token = (await self.renew_token(NoonLoginResponse(self.__token))).token

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, token: str):
        self.__token = token

    async def login(self, email: str, password: str) -> NoonLoginResponse:
        async with self.__session.post('https://finn.api.noonhome.com/api/login', json=NoonLoginRequest(email, password)) as response:
            loginresponse: NoonLoginResponse = await response.json(loads=_get_loads(NoonLoginResponse))
            self.__token = loginresponse.token

            await self.retrieve_endpoints_sync()

            return loginresponse

    def sign_out(self):
        self.__token = None

    def is_logged_in(self) -> bool:
        return self.__token is not None

    async def retrieve_endpoints_sync(self) -> bool:
        try:
            async with await self.__authrequest(hdrs.METH_GET, 'https://finn.api.noonhome.com/api/endpoints') as response:
                NoonClient.set_endpoints((await response.json(loads=_get_loads(NoonDexResponse))).endpoints)
                return True
        except:
            return False

    async def query_user_leases(self) -> NoonModel:
        headers = {'Content-Type': 'application/graphql'}
        async with await self.__authrequest(hdrs.METH_POST, NoonClient.get_endpoints().query + '/api/query', data=self.noon_basic_lease_query, headers=headers) as response:
            return await response.json(loads=_get_loads(NoonModel))

    async def query_user_info(self) -> NoonModel:
        headers = {'Content-Type': 'application/graphql'}
        async with await self.__authrequest(hdrs.METH_POST, NoonClient.get_endpoints().query + '/api/query', data=self.__noon_user_query, headers=headers) as response:
            return await response.json(loads=_get_loads(NoonModel))

    async def query_space(self, space: str) -> NoonStructure:
        headers = {'Content-Type': 'application/graphql'}
        async with await self.__authrequest(hdrs.METH_POST, NoonClient.get_endpoints().query + '/api/query', data='{ spaces (guid: "' + space + '") { name, icon, guid, type, lightsOn, lightingConfigModified, devices { name, guid, type, isMaster, isOnline, serial, displayName, softwareVersion, expectedSoftwareVersion, batteryLevel, expectedLinesGuid, actualLinesGuid, expectedScenesGuid, actualScenesGuid, scenesAllowed, line { guid, preconfigured }, otaState { guid, type, retryCount, installState, percentDownloaded }, base { guid, firmwareVersion, serial, capabilities { dimming, powerRating } }, capabilities { iconSet, maxScenes, hue, gridView, dimmingBase, dimming, wholeHomeScenes } }, lines {  guid, displayName, lineState, dimmingLevel, dimmable, remoteControllable, preconfigured, bulbType, multiwayMaster { guid }, lights { guid, fixtureType, bulbBrand, bulbQuantity }, externalDevices { externalId, isOnline} }, subspaces { guid, name, lines { guid }, type }, sceneOrder,  activeSceneSchedule { guid }, scenes { guid, icon, name, type, isActive, lightLevels { recommendedMax, recommendedMin, value, lineState, line { guid, lineState, dimmingLevel, displayName, bulbType, remoteControllable } } }, activeScene { guid, name, icon } } }', headers=headers) as response:
            return await response.json(loads=_get_loads(NoonStructure))

    async def fetch_model(self) -> NoonModel:
        headers = {'Content-Type': 'application/graphql'}
        async with await self.__authrequest(hdrs.METH_POST, NoonClient.get_endpoints().query + '/api/query', data=NoonClient.__noon_model_query, headers=headers) as response:
            return await response.json(loads=_get_loads(NoonModel))

    async def get_model(self) -> NoonModel:
        headers = {'Content-Type': 'application/graphql'}
        async with await self.__authrequest(hdrs.METH_POST, NoonClient.get_endpoints().query + '/api/query', data=self.noon_basic_lease_query, headers=headers) as response:
            return await response.json(loads=_get_loads(NoonModel))

    async def query_structure(self, structure: str) -> NoonLease:
        headers = {'Content-Type': 'application/graphql'}
        async with await self.__authrequest(hdrs.METH_POST, NoonClient.get_endpoints().query + '/api/query', data='{ structure (guid: "' + structure + '") { name, guid, zipcode, timezone, icon, sceneOrder, sceneSchedules { guid, name, enabled, onTime { hour, minute, relativeTo, type }, offTime { hour,  minute, relativeTo, type }, daysOfWeek, space { guid, name }, scene { guid, name } }, vacationMode { enabled, spaces { guid } }, nightLightMode { enabled, spaces { guid }, scheduleOn { hour, minute }, scheduleOff { hour, minute } }, scenes { guid, name, type, controlSpaces { guid }, spaces {allOff, spaceGuid, sceneGuid } }, spaces { name, icon, guid, type, lightsOn, occupancyDetected, lightingConfigModified, activeScene { guid }, lines { bulbType, dimmingLevel, displayName, externalDevices { externalId, isOnline }, guid, lights { bulbBrand, bulbQuantity, bulbType, fixtureType, guid }, lineState, multiwayMaster { guid }, remoteControllable }, subspaces { guid, name, lines { guid }, type }, sceneOrder, activeSceneSchedule { guid }, scenes { name, guid, icon, type, lightLevels { lineState, recommendedMax, recommendedMin, value, line { guid } } }, devices { accessoryControlGuid, activeDimmingCurve, actualLinesGuid, actualScenesGuid, apRssi, base { capabilities { dimming, powerRating }, firmwareVersion, guid, serial }, baseSerial, batteryLevel, capabilities { elvisCapability, gridView, hue, iconSet, maxScenes, wholeHomeRequest, wholeHomeScenes, wholeHomeState }, currentSamplingState, dimmingAllowed, displayName, expectedLinesGuid, expectedScenesGuid, expectedSoftwareVersion, guid, hardwareRevision, isActive, isMaster, isOnline, line { guid }, mode, modelNumber, name, otaState { guid, installState, percentDownloaded, retryCount, type }, pairingToken, scenesAllowed, serial, smartBulbs { attributes { key, value  }, brand, fixtureType, guid, name }, softwareVersion, type } } } }', headers=headers) as response:
            return await response.json(loads=_get_loads(NoonLease))

    async def set_light(self, space: str, lights_on: bool) -> ClientResponse:
        noon_change_lights_on_request = NoonChangeLightsOnRequest(
            space, lights_on)
        self.__transactionid += 1
        noon_change_lights_on_request.tid = self.__transactionid
        return await self.__authrequest(hdrs.METH_POST, NoonClient.get_endpoints().action + '/api/action/space/light', json=noon_change_lights_on_request)

    async def set_structure_lights(self, structure: str, lights_on: bool) -> None:
        noon_change_lights_on_request = NoonLightsOnStructureRequest(
            structure, lights_on)
        self.__transactionid += 1
        noon_change_lights_on_request.tid = self.__transactionid
        await self.__authrequest(hdrs.METH_POST, NoonClient.get_endpoints().action + '/api/action/structure/light', json=noon_change_lights_on_request)

    async def set_scene(self, space: str, active_scene: str, on: bool) -> ClientResponse:
        noon_change_scene_request = NoonChangeSceneRequest(
            space, active_scene, on)
        self.__transactionid += 1
        noon_change_scene_request.tid = self.__transactionid
        return await self.__authrequest(hdrs.METH_POST, NoonClient.get_endpoints().action + '/api/action/space/light', json=noon_change_scene_request)

    async def send_geofence_crossed_event(self, noon_geofence_event: NoonGeofenceEvent) -> ClientResponse:
        return await self.__authrequest(hdrs.METH_POST, NoonClient.get_endpoints().action + '/api/action/structure/geofence', json=noon_geofence_event)

    async def set_line_light_level(self, noon_set_line_light_level_request: NoonSetLineLightLevelRequest) -> ClientResponse:
        self.__transactionid += 1
        noon_set_line_light_level_request.tid = self.__transactionid
        return await self.__authrequest(hdrs.METH_POST, NoonClient.get_endpoints().action + '/api/action/line/lightLevel', json=noon_set_line_light_level_request)

    async def set_line_lights_on(self, noon_set_line_lights_on_request: NoonSetLineLightsOnRequest) -> ClientResponse:
        self.__transactionid += 1
        noon_set_line_lights_on_request.tid = self.__transactionid
        return await self.__authrequest(hdrs.METH_POST, NoonClient.get_endpoints().action + '/api/action/line/lightsOn', json=noon_set_line_lights_on_request)

    async def set_device_mode(self, guid: str,  mode: str, line: str = None) -> ClientResponse:
        return await self.__authrequest(hdrs.METH_POST, NoonClient.get_endpoints().action + '/api/action/device/mode', json=NoonSetDeviceModeRequest(guid, mode, line))

    async def set_whole_home_scene(self, noon_change_whole_home_scene_request: NoonChangeWholeHomeSceneRequest):
        await self.__authrequest(hdrs.METH_POST, NoonClient.get_endpoints().action + '/api/action/structure/scene', json=noon_change_whole_home_scene_request)

    async def _auth_ws_connect(self):
        try:
            return self.__session.ws_connect(NoonClient.get_endpoints().notification_ws + '/api/notifications',
                                             headers={
                                                 'Authorization': 'Token ' + self.__token},
                                             heartbeat=15)
        except ClientResponseError as err:
            if err.status != 401:
                raise
            await self.renew_token_sync()
            return self.__session.ws_connect(NoonClient.get_endpoints().notification_ws + '/api/notifications',
                                             headers={
                                                 'Authorization': 'Token ' + self.__token},
                                             heartbeat=15)

    async def listen(self, fld_deseralized_names=True):
        def should_listen():
            return self.is_logged_in() and self.__noon_endpoints is not None and self.__noon_endpoints.notification_ws is not None

        def set_deseralized_fld_names(change: NoonChange):
            for f in change.fields:
                f.name = deserializednames.get(f.name, f.name)
            return change

        transform = set_deseralized_fld_names if fld_deseralized_names else lambda name: name
        while should_listen():
            try:
                async with await self._auth_ws_connect() as ws:
                    async for msg in ws:
                        if "notification" not in msg.data:
                            continue
                        noon_viper: NoonViper = msg.json(
                            loads=_get_loads(NoonViper))
                        for change in noon_viper.data.changes:
                            yield transform(change)
            except ClientResponseError:
                pass

            await asyncio.sleep(10)
