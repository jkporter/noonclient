from abc import abstractmethod, ABC
from aiohttp.client_reqrep import ClientResponse
from typing import Any, Union
from noonclient.alaska.model import NoonBulbDetectionRequest, NoonBulbDetectionResponse, NoonChangeLightsOnRequest, NoonChangeSceneRequest, NoonChangeWholeHomeSceneRequest, NoonCurrentSamplingRequest, NoonDexResponse, NoonDexUrls, NoonGeofenceEvent, NoonLightsOnStructureRequest, NoonMobileTelemetryRequest, NoonModel, NoonLoginRequest, NoonLoginResponse, NoonOtaRequest, NoonProvisionedKeyHolder, NoonPulseLineRequest, NoonSetDeviceModeRequest, NoonSetLineLightLevelRequest, NoonSetLineLightsOnRequest, NoonStructure, NoonStructureInvitationsResponse, NoonVersions
from noonclient._http import get, post, put, headers


class BobbajoService(ABC):
    @post("/api/action/space/light")
    @abstractmethod
    async def change_light(noon_change_lights_on_request: NoonChangeLightsOnRequest) -> ClientResponse:
        pass

    @post("/api/action/structure/light")
    @abstractmethod
    async def change_lights_structure(noon_lights_on_structure_request: NoonLightsOnStructureRequest) -> ClientResponse:
        pass

    @put("/api/action/device/firmware/deploy")
    async def force_ota_deploy(noon_ota_request: NoonOtaRequest) -> ClientResponse:
        pass

    @put("/api/action/device/firmware/download")
    async def force_ota_download(noon_ota_request: NoonOtaRequest) -> ClientResponse:
        pass

    @post("/api/action/structure/geofence")
    async def geofence_crossed(noon_geofence_event: NoonGeofenceEvent) -> NoonGeofenceEvent:
        pass

    @post("/api/action/line/pulse")
    async def pulse_line_light(noonPulseLineRequest: NoonPulseLineRequest) -> ClientResponse:
        pass

    @post("/api/action/line/bulbDetection")
    async def request_bulb_detection(noon_bulb_detection_request: NoonBulbDetectionRequest) -> NoonBulbDetectionResponse:
        pass

    @post("/api/action/line/currentSampling")
    async def request_current_sampling(noonCurrentSamplingRequest: NoonCurrentSamplingRequest) -> ClientResponse:
        pass

    @post("/api/action/device/mode")
    async def setDeviceMode(noonSetDeviceModeRequest: NoonSetDeviceModeRequest) -> ClientResponse:
        pass

    @post("/api/action/line/lightLevel")
    async def setLineLightLevel(noonSetLineLightLevelRequest: NoonSetLineLightLevelRequest) -> ClientResponse:
        pass

    @post("/api/action/line/lightsOn")
    async def setLineLightsOn(noonSetLineLightsOnRequest: NoonSetLineLightsOnRequest) -> ClientResponse:
        pass

    @post("/api/action/space/scene")
    async def setScene(noonChangeSceneRequest: NoonChangeSceneRequest) -> ClientResponse:
        pass

    @post("/api/action/structure/scene")
    async def setWholeHomeScene(noonChangeWholeHomeSceneRequest: NoonChangeWholeHomeSceneRequest) -> None:
        pass

    @post("/api/mobileTelemetry")
    async def storeTelemetryData(noonMobileTelemetryRequest: NoonMobileTelemetryRequest) -> ClientResponse:
        pass


class DexService(ABC):
    @get("/api/endpoints")
    @abstractmethod
    async def retrieveEndpoints() -> NoonDexResponse:
        pass

    @get("/api/urls")
    @abstractmethod
    async def retrieveUrls() -> NoonDexUrls:
        pass

    @get("/api/versions")
    @abstractmethod
    async def retrieveVersions() -> NoonVersions:
        pass


class FinnService(ABC):
    @post("/api/login")
    @headers({"Content-Type: application/graphql"})
    @abstractmethod
    async def login(noon_login_request: NoonLoginRequest) -> NoonLoginResponse:
        pass

    @post("/api/token/renew")
    @abstractmethod
    async def renew_token(noon_login_response: NoonLoginResponse) -> NoonLoginResponse:
        pass


class VipService(ABC):
    @get("/api/notifications")
    @abstractmethod
    async def get_notifications() -> ClientResponse:
        pass


class YodaService(ABC):
    @post("/api/query")
    @headers({"Content-Type: application/graphql"})
    async def query(request_body: Union[Any, None]) -> NoonModel:
        pass

    @post("/api/query")
    @headers({"Content-Type: application/graphql"})
    async def query_all_structure_invitations(request_body: Union[Any, None]) -> NoonStructureInvitationsResponse:
        pass

    @post("/api/query")
    @headers({"Content-Type: application/graphql"})
    async def query_key(request_body: Union[Any, None]) -> NoonProvisionedKeyHolder:
        pass

    @post("/api/query")
    @headers({"Content-Type: application/graphql"})
    async def query_leases(request_body: Union[Any, None]) -> NoonModel:
        pass

    @post("/api/query")
    @headers({"Content-Type: application/graphql"})
    async def query_space(request_body: Union[Any, None]) -> NoonStructure:
        pass

    @post("/api/query")
    @headers({"Content-Type: application/graphql"})
    async def query_user(request_body: Union[Any, None]) -> NoonModel:
        pass
