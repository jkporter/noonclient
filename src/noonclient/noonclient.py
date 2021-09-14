from datetime import datetime, timedelta
from types import TracebackType
from typing import Any, Callable, Coroutine, Optional, Type
from noonclient.alaska.model import NoonArea, NoonBase, NoonChange, NoonDevice, NoonDexResponse, NoonEndpoints, NoonLight, NoonLine, NoonLoginRequest, NoonLoginResponse, NoonModel, NoonScene, NoonSpace, NoonStructure, NoonViper
import aiohttp
from noonclient.alaska.model import NoonLoginResponse
from noonclient._serialization import _models_fields_types, _json_seralize, _get_loads
from noonclient.alaska.kush import GraphQLGenerator

SUBSCRIBABLE_MODEL_TYPES = [NoonArea,
                            NoonBase,
                            NoonDevice,
                            NoonLight,
                            NoonLine,
                            NoonScene,
                            NoonSpace,
                            NoonStructure]


def _model_assign(target: Any, *sources: dict[str, Any]):
    for source in sources:
        for k, v in source.items():
            if getattr(target, k) != v:
                setattr(target, k, v)

    return target


class NoonClient:
    def __init__(self, email: str, password: str, *, on_change: Callable[[NoonChange], None] = None):
        self.email = email
        self.password = password
        self.on_change: Callable[[NoonChange], None] = on_change
        self.__loginReponse: NoonLoginResponse = None
        self.__loginResponseDate: datetime = None
        self.__models = dict()
        self.__session = aiohttp.ClientSession(
            raise_for_status=True, json_serialize=_json_seralize)
        self.__subscriptions = set()
        self.__endpoints: NoonEndpoints = None

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

    async def authenticate(self):
        if(self.__loginResponseDate is None or (seconds_delta := (datetime.now() - self.__loginResponseDate).total_seconds()) >= self.__loginReponse.renewLifetime):
            path = '/api/login'
            data = NoonLoginRequest(self.email, self.password)
        elif(seconds_delta >= self.__loginReponse.lifetime):
            path = '/token/renew'
            data = self.__loginReponse
        else:
            return

        async with self.__session.post('https://finn.api.noonhome.com' + path, json=data) as response:
            self.__loginReponse = await response.json(loads=_get_loads(NoonLoginResponse))
            self.__loginResponseDate = datetime.strptime(
                response.headers['Date'], '%a, %d %b %Y %H:%M:%S %Z')
            headers = {'Content-Type': 'application/graphql',
                       'Authorization': 'Token ' + self.token}
            async with self.__session.get('https://dex.api.noonhome.com/api/endpoints', headers=headers) as response:
                self.__endpoints = (await response.json(loads=_get_loads(NoonDexResponse))).endpoints

    @property
    def endpoints(self) -> NoonEndpoints:
        return self.__endpoints

    @property
    def token(self):
        return self.__loginReponse.token

    @property
    def tokenExpire(self) -> datetime:
        return self.__loginResponseDate + timedelta(seconds=self.__loginReponse.lifetime)

    @property
    def tokenRenewalExpire(self) -> datetime:
        return self.__loginResponseDate + timedelta(seconds=self.__loginReponse.renewLifetime)

    def _create_get_model(self):
        def get_model(d: dict[str, Any], type: Type):
            if type not in SUBSCRIBABLE_MODEL_TYPES:
                return type(**d)

            if d['guid'] in self.__models:
                model = _model_assign(self.__models[d['guid']], d)
            else:
                model = type(**d)
                self.__models[model.guid] = model
            return model

        return get_model

    async def query(self) -> NoonModel:
        await self.authenticate()
        headers = {'Content-Type': 'application/graphql',
                   'Authorization': 'Token ' + self.token}
        async with self.__session.post(self.__endpoints.query + '/api/query', data=GraphQLGenerator.generate(NoonModel), headers=headers) as response:
            return await response.json(loads=_get_loads(NoonModel, self._create_get_model()))

    async def listen(self):
        await self.authenticate()
        headers = {'Authorization': 'Token ' + self.token}
        async with self.__session.ws_connect(self.__endpoints.notification_ws + '/api/notifications', headers=headers) as ws:
            async for msg in ws:
                viper: NoonViper = msg.json(loads=_get_loads(NoonViper))
                if self.on_change is not None and viper.event == 'notification':
                    for change in viper.data.changes:
                        if change.guid in self.__subscriptions:
                            self.on_change(change)

    def subscribe(self, guid: str):
        self.__subscriptions.add(guid)

    def unsubscribe(self, guid: str):
        self.__subscriptions.discard(guid)
