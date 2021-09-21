from __future__ import annotations
from dataclasses import dataclass
from typing import Any

def serializedname(name: str, serializedname: str):
    def set_serializedname(cls):
        if not hasattr(cls, '_serializednames'):
            cls._serializednames = dict()
            cls._serializednames_rev = dict()
        cls._serializednames[name] = serializedname
        cls._serializednames_rev[serializedname] = name
        return cls
    return set_serializedname

@dataclass
class NoonAccountInvitation:
    type: str = None
    guid: str = None
    state: str = None
    structure: NoonStructure__ = None


@dataclass
class NoonActiveSceneSchedule:
    guid: str = None


@serializedname('old_fixture_type', 'oldFixtureType')
@serializedname('fixture_type', 'fixtureType')
@serializedname('old_bulb_type', 'oldBulbType')
@serializedname('old_smart_bulb_id', 'oldSmartBulbId')
@serializedname('old_bulb_brand', 'oldBulbBrand')
@serializedname('bulb_quantity', 'bulbQuantity')
@serializedname('old_bulb_quantity', 'oldBulbQuantity')
@serializedname('bulb_type', 'bulbType')
@serializedname('bulb_brand', 'bulbBrand')
@serializedname('smart_bulb_id', 'smartBulbId')
@dataclass
class NoonAlterLightResponse:
    old_fixture_type: str = None
    fixture_type: str = None
    old_bulb_type: str = None
    old_smart_bulb_id: str = None
    old_bulb_brand: str = None
    bulb_quantity: int = None
    old_bulb_quantity: int = None
    bulb_type: str = None
    bulb_brand: str = None
    smart_bulb_id: str = None


@serializedname('fixture_type', 'fixtureType')
@serializedname('bulb_type', 'bulbType')
@serializedname('bulb_quantity', 'bulbQuantity')
@serializedname('smart_bulb', 'smartBulb')
@serializedname('smart_bulb_id', 'smartBulbId')
@dataclass
class NoonAlterLightRequest:
    fixture_type: str = None
    bulb_type: str = None
    bulb_quantity: str = None
    smart_bulb: NoonSmartBulb = None
    smart_bulb_id: str = None


@dataclass
class NoonArea:
    name: str = None
    guid: str = None
    type: str = None
    lines: list[NoonLine] = None


@dataclass
class NoonAttribute:
    key: str = None
    value: str = None


@serializedname('firmware_version', 'firmwareVersion')
@dataclass
class NoonBase:
    guid: str = None
    serial: str = None
    firmware_version: str = None
    capabilities: NoonCapabilities = None


@serializedname('average_distance', 'averageDistance')
@dataclass
class NoonBeaconItem:
    uuid: str = None
    major: str = None
    minor: str = None
    state: int = None
    distances: list[float] = None
    average_distance: float = None


@dataclass
class NoonBLEEventRequest:
    driver_version: str = None
    noise_dbm: int = None
    firmware_version: int = None
    chip_hardware_version: str = None
    ble_connect_state: str = None
    rssi_dbm: int = None
    mtu_size: int = None
    security_type: Any = None
    data_rate: int = None
    mac_address: str = None
    ble_on_off_state: str = None
    security_family: str = None
    timestamp: str = None


@serializedname('propagate_dim_curve', 'propagateDimCurve')
@serializedname('is_steady_state', 'isSteadyState')
@dataclass
class NoonBulbDetectionRequest:
    line: str = None
    propagate_dim_curve: bool = None
    is_steady_state: bool = None


@serializedname('bulb_type', 'bulbType')
@dataclass
class NoonBulbDetectionResponse:
    line: str
    bulb_type: str
    dimmable: bool


@serializedname('power_rating', 'powerRating')
@dataclass
class NoonCapabilities:
    power_rating: Any = None
    dimming: Any = None


@dataclass
class NoonChange:
    guid: str = None
    tid: int = None
    fields: list[NoonField] = None


@serializedname('lights_on', 'lightsOn')
@dataclass
class NoonChangeLightsOnRequest:
    space: str = None
    lights_on: bool = None
    tid: int = None


@serializedname('active_scene', 'activeScene')
@dataclass
class NoonChangeSceneRequest:
    space: str = None
    active_scene: str = None
    f129on: bool = None
    tid: int = None


@dataclass
class NoonChangeWholeHomeSceneRequest:
    structure: str = None
    scene: str = None


@serializedname('propagate_dim_curve', 'propagateDimCurve')
@serializedname('is_steady_state', 'isSteadyState')
@dataclass
class NoonCurrentSamplingRequest:
    line: str = None
    propagate_dim_curve: bool = None
    is_steady_state: bool = None


@dataclass
class NoonData:
    changes: list[NoonChange] = None


@serializedname('accessory_control_guid', 'accessoryControlGuid')
@serializedname('display_name', 'displayName')
@serializedname('is_active', 'isActive')
@serializedname('is_master', 'isMaster')
@serializedname('is_online', 'isOnline')
@serializedname('hardware_revision', 'hardwareRevision')
@serializedname('software_version', 'softwareVersion')
@serializedname('expected_software_version', 'expectedSoftwareVersion')
@serializedname('expected_lines_guid', 'expectedLinesGuid')
@serializedname('actual_lines_guid', 'actualLinesGuid')
@serializedname('expected_scenes_guid', 'expectedScenesGuid')
@serializedname('actual_scenes_guid', 'actualScenesGuid')
@serializedname('base_serial', 'baseSerial')
@serializedname('model_number', 'modelNumber')
@serializedname('battery_level', 'batteryLevel')
@serializedname('ap_rssi', 'apRssi')
@serializedname('current_sampling_state', 'currentSamplingState')
@serializedname('dimming_allowed', 'dimmingAllowed')
@serializedname('scenes_allowed', 'scenesAllowed')
@serializedname('active_dimming_curve', 'activeDimmingCurve')
@serializedname('pairing_token', 'pairingToken')
@serializedname('ota_state', 'otaState')
@serializedname('smart_bulbs', 'smartBulbs')
@serializedname('beacon_item', 'beaconItem')
@dataclass
class NoonDevice:
    guid: str = None
    accessory_control_guid: str = None
    name: str = None
    display_name: str = None
    serial: str = None
    is_active: bool = None
    type: str = None
    is_master: bool = None
    is_online: bool = None
    hardware_revision: str = None
    software_version: str = None
    expected_software_version: str = None
    expected_lines_guid: str = None
    actual_lines_guid: str = None
    expected_scenes_guid: str = None
    actual_scenes_guid: str = None
    base_serial: str = None
    mode: str = None
    model_number: str = None
    battery_level: int = None
    ap_rssi: int = None
    current_sampling_state: str = None
    dimming_allowed: bool = None
    scenes_allowed: bool = None
    active_dimming_curve: int = None
    pairing_token: str = None
    base: NoonBase = None
    line: NoonLine = None
    ota_state: NoonOtaState = None
    smart_bulbs: list = None
    capabilities: NoonDeviceCapability = None
    #beacon_item: NoonBeaconItem = None


@serializedname('display_name', 'displayName')
@dataclass
class NoonDeviceAttribute:
    name: str = None
    display_name: str = None


@serializedname('display_name', 'displayName')
@serializedname('old_display_name', 'old_displayName')
@dataclass
class NoonDeviceAttributeResponse:
    name: str = None
    old_name: str = None
    display_name: str = None
    old_display_name: str = None


@serializedname('max_scenes', 'maxScenes')
@serializedname('whole_home_request', 'wholeHomeRequest')
@serializedname('whole_home_state', 'wholeHomeState')
@serializedname('elvis_capability', 'elvisCapability')
@serializedname('icon_set', 'iconSet')
@serializedname('grid_view', 'gridView')
@serializedname('preconfigured_multiway', 'preconfiguredMultiway')
@serializedname('whole_home_scenes', 'wholeHomeScenes')
@dataclass
class NoonDeviceCapability:
    max_scenes: int = None
    whole_home_request: int = None
    whole_home_state: int = None
    hue: int = None
    elvis_capability: int = None
    icon_set: int = None
    grid_view: int = None
    preconfigured_multiway: int = None
    whole_home_scenes: int = None


@dataclass
class NoonDexResponse:
    endpoints: NoonEndpoints = None
    partition: str = None
    ttl: int = None


@serializedname('privacy_policy', 'privacyPolicy')
@serializedname('terms_of_service', 'termsOfService')
@serializedname('email_verification_kb', 'emailVerificationKB')
@serializedname('dimming_kb', 'dimmingKB')
@serializedname('alexa_kb', 'alexaKB')
@serializedname('scheduling_kb', 'schedulingKB')
@serializedname('google_assistant_kb', 'googleAssistantKB')
@serializedname('pairing_kb', 'pairingKB')
@dataclass
class NoonDexUrls:
    privacy_policy: str = None
    terms_of_service: str = None
    email_verification_kb: str = None
    dimming_kb: str = None
    alexa_kb: str = None
    scheduling_kb: str = None
    google_assistant_kb: str = None
    pairing_kb: str = None
    support: str = None
    contact: str = None


@dataclass
class NoonEndpoints:
    action: str = None
    device: str = None
    mutation: str = None
    notification: str = None
    notification_ws: str = None
    query: str = None
    external_device: str = None


@serializedname('external_id', 'externalId')
@serializedname('is_online', 'isOnline')
@dataclass
class NoonExternalDevice:
    external_id: str = None
    is_online: bool = None


@dataclass
class NoonField:
    name: str = None
    value: Any = None
    recursive: bool = None


@dataclass
class NoonGeofenceEvent:
    structure: str = None
    entered: bool = None


@dataclass
class NoonLease:
    structure: NoonStructure = None
    grants: Any = None


@serializedname('bulb_brand', 'bulbBrand')
@serializedname('bulb_quantity', 'bulbQuantity')
@serializedname('bulb_type', 'bulbType')
@serializedname('fixture_type', 'fixtureType')
@dataclass
class NoonLight:
    guid: str = None
    bulb_brand: str = None
    bulb_quantity: int = None
    bulb_type: str = None
    fixture_type: str = None


@serializedname('lights_on', 'lightsOn')
@dataclass
class NoonLightsOnStructureRequest:
    lights_on: bool = None
    structure: str = None
    tid: int = None


@serializedname('display_name', 'displayName')
@serializedname('remote_controllable', 'remoteControllable')
@serializedname('line_state', 'lineState')
@serializedname('dimming_level', 'dimmingLevel')
@serializedname('bulb_type', 'bulbType')
@serializedname('external_devices', 'externalDevices')
@serializedname('multiway_master', 'multiwayMaster')
@dataclass
class NoonLine:
    guid: str = None
    display_name: str = None
    remote_controllable: bool = None
    preconfigured: bool = None
    line_state: str = None
    dimming_level: int = None
    bulb_type: str = None
    lights: list[NoonLight] = None
    external_devices: list[NoonExternalDevice] = None
    multiway_master: NoonMultiwayMaster = None


@dataclass
class NoonLoginRequest:
    email: str = None
    password: int = None
    lifetime: int = None


@serializedname('renew_lifetime', 'renewLifetime')
@dataclass
class NoonLoginResponse:
    token: str = None
    lifetime: int = None
    renew_lifetime: int = None


@serializedname('recommended_max', 'recommendedMax')
@serializedname('recommended_min', 'recommendedMin')
@serializedname('line_state', 'lineState')
@serializedname('smart_bulb', 'smartBulb')
@dataclass
class NoonLightLevel:
    value: int = None
    recommended_max: int = None
    recommended_min: int = None
    line_state: str = None
    line: NoonLine = None
    #smart_bulb: NoonSmartBulb = None


@dataclass
class NoonMobileTelemetryRequest:
    system_event: NoonSystemEventRequest = None
    setup_event: NoonSetupEventRequest = None
    wifi_event: NoonWiFiEventRequest = None
    ble_event: NoonBLEEventRequest = None


@dataclass
class NoonModel:
    user: NoonUser = None
    preferences: list[NoonPreference] = None
    leases: list[NoonLease] = None


@dataclass
class NoonMultiwayMaster:
    guid: str = None


@serializedname('schedule_on', 'scheduleOn')
@serializedname('schedule_off', 'scheduleOff')
@dataclass
class NoonNightLightMode:
    enabled: bool = None
    schedule_on: NoonScheduleOn = None
    schedule_off: NoonScheduleOff = None
    spaces: list[NoonSpace] = None


@dataclass
class NoonOtaRequest:
    guid: str = None


@serializedname('retry_count', 'retryCount')
@serializedname('install_state', 'installState')
@serializedname('percent_downloaded', 'percentDownloaded')
@dataclass
class NoonOtaState:
    type: str = None
    guid: str = None
    retry_count: int = None
    install_state: str = None
    percent_downloaded: float = None


@dataclass
class NoonPreference:
    key: str = None
    value: str = None


@dataclass
class NoonProvisionedKey:
    serial: str = None
    guid: str = None
    key: str = None


@serializedname('provisioned_key', 'provisionedKey')
@dataclass
class NoonProvisionedKeyHolder:
    provisioned_key: NoonProvisionedKey = None


@serializedname('on_time', 'onTime')
@serializedname('off_time', 'offTime')
@dataclass
class NoonPulseLineRequest:
    line: str = None
    on_time: int = None
    off_time: int = None
    count: int = None


@serializedname('is_active', 'isActive')
@serializedname('light_levels', 'lightLevels')
@serializedname('transition_on', 'transitionOn')
@serializedname('transition_off', 'transitionOff')
@serializedname('motion_activated', 'motionActivated')
@dataclass
class NoonScene:
    guid: str = None
    name: str = None
    icon: str = None
    is_active: bool = None
    light_levels: list[NoonLightLevel] = None
    transition_on: int = None
    transition_off: int = None
    hidden: bool = None
    motion_activated: bool = None
    type: str = None


@serializedname('on_time', 'onTime')
@serializedname('off_time', 'offTime')
@dataclass
class NoonSceneSchedule:
    guid: str = None
    name: str = None
    enabled: bool = None
    on_time: NoonSchedule = None
    off_time: NoonSchedule = None
    daysOfWeek = list
    space: NoonSpace = None
    scene: NoonScene = None


@serializedname('relative_to', 'relativeTo')
@dataclass
class NoonSchedule:
    day: int = None
    hour: int = None
    minute: int = None
    type: str = None
    relative_to: str = None


@dataclass
class NoonScheduleOff:
    hour: int = None
    minute: int = None


@dataclass
class NoonScheduleOn:
    hour: int = None
    minute: int = None


@dataclass
class NoonSetDeviceModeRequest:
    device: str = None
    mode: str = None
    line: str = None


@serializedname('light_level', 'lightLevel')
@serializedname('transition_time', 'transitionTime')
@dataclass
class NoonSetLineLightLevelRequest:
    line: str = None
    light_level: int = None
    tid: int = None
    transition_time: int = None


@serializedname('lights_on', 'lightsOn')
@dataclass
class NoonSetLineLightsOnRequest:
    line: str = None
    lights_on: bool = None
    tid: int = None


@dataclass
class NoonSetupEventRequest:
    transaction_id: str = None
    device_type: str = None
    operation: str = None
    event_message: str = None
    error_code: str = None
    status: str = None
    user_id: str = None
    event_type: str = None
    device_id: str = None
    timestamp: str = None


@serializedname('fixture_type', 'fixtureType')
@dataclass
class NoonSmartBulb:
    guid: str = None
    name: str = None
    fixture_type: str = None
    brand: str = None
    attributes: list[NoonAttribute] = None


@serializedname('occupancy_detected', 'occupancyDetected')
@serializedname('lighting_config_modified', 'lightingConfigModified')
@serializedname('lights_on', 'lightsOn')
@serializedname('active_scene', 'activeScene')
@serializedname('active_scene_schedule', 'activeSceneSchedule')
@dataclass
class NoonSpace:
    name: str = None
    guid: str = None
    icon: str = None
    type: str = None
    occupancy_detected: bool = None
    lighting_config_modified: bool = None
    lines: list[NoonLine] = None
    lights_on: bool = None
    active_scene: NoonScene = None
    active_scene_schedule: NoonActiveSceneSchedule = None
    scenes: list[NoonScene] = None
    devices: list[NoonDevice] = None
    subspaces: list[NoonArea] = None
    settings: list[NoonSpaceSetting] = None


@dataclass
class NoonSpaceSetting:
    key: str = None
    value: str = None


@serializedname('vacation_mode', 'vacationMode')
@serializedname('night_light_mode', 'nightLightMode')
@serializedname('scene_schedules', 'sceneSchedules')
@serializedname('active_scene', 'activeScene')
@serializedname('scene_order', 'sceneOrder')
@dataclass
class NoonStructure:
    name: str = None
    guid: str = None
    icon: str = None
    spaces: list[NoonSpace] = None
    timezone: str = None
    zipcode: str = None
    vacation_mode: NoonVacationMode = None
    night_light_mode: NoonNightLightMode = None
    scene_schedules: list[NoonSceneSchedule] = None
    active_scene: str = None
    scene_order: str = None
    scenes: list[NoonWholeHomeScene] = None


@serializedname('account_invitations', 'accountInvitations')
@dataclass
class NoonStructure__:
    guid: str = None
    account_invitations: list[NoonAccountInvitation] = None


@dataclass
class NoonStructureInvitationsResponse:
    structure: NoonStructure__ = None


@dataclass
class NoonSystemEventRequest:
    transaction_id: str = None
    user_id: str = None
    timestamp: str = None
    app_name: str = None
    app_version: str = None
    phone_hardware: str = None
    phone_os: str = None
    firmware_version: str = None
    phone_name: str = None
    location_permission: str = None
    notification_permission: str = None
    app_launch_time: int = None


@serializedname('email_valid', 'emailValid')
@serializedname('incoming_invitations', 'incomingInvitations')
@serializedname('outgoing_invitations', 'outgoingInvitations')
@dataclass
class NoonUser:
    guid: str = None
    name: str = None
    email_valid: str = None
    #incoming_invitations: list[NoonIncomingInvitation] = None
    #outgoing_invitations: list[NoonOutgoingInvitation] = None


@dataclass
class NoonVacationMode:
    enabled: bool = None
    spaces: list[NoonSpace] = None

    # def describeContents():
    #    return 0


@serializedname('current_version', 'currentVersion')
@serializedname('recommended_version', 'recommendedVersion')
@serializedname('required_version', 'requiredVersion')
@dataclass
class NoonVersions:
    current_version: int = None
    recommended_version: int = None
    required_version: int = None


@dataclass
class NoonViper:
    event: str = None
    data: NoonData = None


@serializedname('control_spaces', 'controlSpaces')
@dataclass
class NoonWholeHomeScene:
    name: str = None
    guid: str = None
    spaces: list[NoonWholeHomeSceneSpace] = None
    control_spaces: list[NoonWholeHomeSceneControlSpace] = None


@dataclass
class NoonWholeHomeSceneControlSpace:
    guid: str = None


@serializedname('space_guid', 'spaceGuid')
@serializedname('scene_guid', 'sceneGuid')
@serializedname('all_off', 'allOff')
@dataclass
class NoonWholeHomeSceneSpace:
    space_guid: str = None
    scene_guid: str = None
    all_off: bool = None


@dataclass
class NoonWiFiEventRequest:
    driver_version: str = None
    n_capable_bit: int = None
    noise_dbm: int = None
    ht_mode: str = None
    firmware_version: str = None
    ssid: str = None
    bssid: str = None
    chip_hardware_version: str = None
    rssi_dbm: int = None
    mtu_size: int = None
    security_type: str = None
    data_rate: int = None
    mac_address: str = None
    timestamp: str = None