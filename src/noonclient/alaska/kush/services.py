from abc import abstractmethod, ABC
from aiohttp.client_reqrep import ClientResponse
from typing import Any, Union
from noonclient.alaska.model import NoonAlterLightRequest, NoonAlterLightResponse, NoonBulbDetectionRequest, NoonBulbDetectionResponse, NoonChangeLightsOnRequest, NoonChangeSceneRequest, NoonChangeWholeHomeSceneRequest, NoonCurrentSamplingRequest, NoonDeviceAttribute, NoonDeviceAttributeResponse, NoonDexResponse, NoonDexUrls, NoonGeofenceEvent, NoonLightsOnStructureRequest, NoonMobileTelemetryRequest, NoonModel, NoonLoginRequest, NoonLoginResponse, NoonOtaRequest, NoonProvisionedKeyHolder, NoonPulseLineRequest, NoonSetDeviceModeRequest, NoonSetLineLightLevelRequest, NoonSetLineLightsOnRequest, NoonStructure, NoonStructureInvitationsResponse, NoonVersions
from noonclient._http import get, post, put, headers


class ApiClient(ABC):
    @abstractmethod
    async def alter_device(str: str, noon_device_attribute: NoonDeviceAttribute) -> NoonDeviceAttributeResponse:
        pass

    @abstractmethod
    async def alter_light(str: str, noonAlterLightRequest: NoonAlterLightRequest) -> NoonAlterLightResponse:
        pass

    @abstractmethod
    async def alter_scene(str: str, noonAlterSceneRequest: NoonAlterSceneRequest) -> NoonAlterSceneResponse:
        pass

    @abstractmethod
    async def alter_scene_schedule(str: str, noonSceneScheduleRequest: NoonSceneScheduleRequest) -> ClientResponse:
        pass

    @abstractmethod
    async def alter_space(str: str, noonAlterSpaceRequest: NoonAlterSpaceRequest) -> NoonSpace:
        pass

    @abstractmethod
    async def alter_structure(str: str) -> ClientResponse:
        pass

    @abstractmethod
    async def change_password(str: str, str2: str, str3: str) -> ClientResponse:
        pass

    @abstractmethod
    async def fetch_key(str: str) -> NoonProvisionedKeyHolder:
        pass

    @abstractmethod
    async def fetch_model() -> NoonModel:
        pass

    @abstractmethod
    async def login(self, noon_login_request: NoonLoginRequest) -> NoonLoginResponse:
        pass

    @abstractmethod
    async def renew_token(self, noon_login_response: NoonLoginResponse) -> NoonLoginResponse:
        pass

    @abstractmethod
    async def setPreferences(list: list[NoonPreferenceRequest]) -> NoonPreferenceRequest:
        pass

    @abstractmethod
    async def setScene(str: str, str2: str, z: bool) -> ClientResponse:
        pass

    @abstractmethod
    async def setSpaceLights(str: str, z: bool) - ClientResponse:
        pass


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
    @abstractmethod
    async def force_ota_deploy(noon_ota_request: NoonOtaRequest) -> ClientResponse:
        pass

    @put("/api/action/device/firmware/download")
    @abstractmethod
    async def force_ota_download(noon_ota_request: NoonOtaRequest) -> ClientResponse:
        pass

    @post("/api/action/structure/geofence")
    @abstractmethod
    async def geofence_crossed(noon_geofence_event: NoonGeofenceEvent) -> NoonGeofenceEvent:
        pass

    @post("/api/action/line/pulse")
    @abstractmethod
    async def pulse_line_light(noon_pulse_line_request: NoonPulseLineRequest) -> ClientResponse:
        pass

    @post("/api/action/line/bulbDetection")
    @abstractmethod
    async def request_bulb_detection(noon_bulb_detection_request: NoonBulbDetectionRequest) -> NoonBulbDetectionResponse:
        pass

    @post("/api/action/line/currentSampling")
    @abstractmethod
    async def request_current_sampling(noon_current_sampling_request: NoonCurrentSamplingRequest) -> ClientResponse:
        pass

    @post("/api/action/device/mode")
    @abstractmethod
    async def set_device_mode(noon_set_device_mode_request: NoonSetDeviceModeRequest) -> ClientResponse:
        pass

    @post("/api/action/line/lightLevel")
    @abstractmethod
    async def set_line_light_level(noon_set_line_light_level_request: NoonSetLineLightLevelRequest) -> ClientResponse:
        pass

    @post("/api/action/line/lightsOn")
    @abstractmethod
    async def set_line_lights_on(noon_set_line_rights_on_request: NoonSetLineLightsOnRequest) -> ClientResponse:
        pass

    @post("/api/action/space/scene")
    @abstractmethod
    async def set_scene(noon_change_scene_request: NoonChangeSceneRequest) -> ClientResponse:
        pass

    @post("/api/action/structure/scene")
    @abstractmethod
    async def set_whole_home_scene(noon_change_whole_home_scene_request: NoonChangeWholeHomeSceneRequest) -> None:
        pass

    @post("/api/mobileTelemetry")
    @abstractmethod
    async def store_telemetry_data(noon_mobile_telemetry_request: NoonMobileTelemetryRequest) -> ClientResponse:
        pass


class DexService(ABC):
    @get("/api/endpoints")
    @abstractmethod
    async def retrieve_endpoints() -> NoonDexResponse:
        pass

    @get("/api/urls")
    @abstractmethod
    async def retrieve_urls() -> NoonDexUrls:
        pass

    @get("/api/versions")
    @abstractmethod
    async def retrieve_versions() -> NoonVersions:
        pass


class FinnService(ABC):
    @post("/api/login")
    @headers({"Content-Type: application/graphql"})
    @abstractmethod
    async def login(self, noon_login_request: NoonLoginRequest) -> NoonLoginResponse:
        pass

    @post("/api/token/renew")
    @abstractmethod
    async def renew_token(self, noon_login_response: NoonLoginResponse) -> NoonLoginResponse:
        pass


class VipService(ABC):
    @get("/api/notifications")
    @abstractmethod
    async def get_notifications() -> ClientResponse:
        pass


class YodaService(ABC):
    @post("/api/query")
    @headers({"Content-Type: application/graphql"})
    @abstractmethod
    async def query(request_body: Union[Any, None]) -> NoonModel:
        pass

    @post("/api/query")
    @headers({"Content-Type: application/graphql"})
    @abstractmethod
    async def query_all_structure_invitations(request_body: Union[Any, None]) -> NoonStructureInvitationsResponse:
        pass

    @post("/api/query")
    @headers({"Content-Type: application/graphql"})
    @abstractmethod
    async def query_key(request_body: Union[Any, None]) -> NoonProvisionedKeyHolder:
        pass

    @post("/api/query")
    @headers({"Content-Type: application/graphql"})
    @abstractmethod
    async def query_leases(request_body: Union[Any, None]) -> NoonModel:
        pass

    @post("/api/query")
    @headers({"Content-Type: application/graphql"})
    @abstractmethod
    async def query_space(request_body: Union[Any, None]) -> NoonStructure:
        pass

    @post("/api/query")
    @headers({"Content-Type: application/graphql"})
    @abstractmethod
    async def query_user(request_body: Union[Any, None]) -> NoonModel:
        pass
