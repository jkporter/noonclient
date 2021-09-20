from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class NoonAccountInvitation:
    type: str = None
    guid: str = None
    state: str = None
    structure: NoonStructure__ = None


@dataclass
class NoonActiveSceneSchedule:
    guid: str = None


@dataclass
class NoonAlterLightResponse:
    oldFixtureType: str = None
    fixtureType: str = None
    oldBulbType: str = None
    oldSmartBulbId: str = None
    oldBulbBrand: str = None
    bulbQuantity: int = None
    oldBulbQuantity: int = None
    bulbType: str = None
    bulbBrand: str = None
    smartBulbId: str = None


@dataclass
class NoonAlterLightRequest:
    fixtureType: str = None
    bulbType: str = None
    bulbQuantity: str = None
    smartBulb: NoonSmartBulb = None
    smartBulbId: str = None


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


@dataclass
class NoonBase:
    guid: str = None
    serial: str = None
    firmwareVersion: str = None
    capabilities: NoonCapabilities = None


@dataclass
class NoonBeaconItem:
    uuid: str = None
    major: str = None
    minor: str = None
    state: int = None
    distances: list[float] = None
    averageDistance: float = None


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


@dataclass
class NoonBulbDetectionRequest:
    line: str = None
    propagateDimCurve: bool = None
    isSteadyState: bool = None


@dataclass
class NoonBulbDetectionResponse:
    line: str
    bulbType: str
    dimmable: bool


@dataclass
class NoonCapabilities:
    powerRating: Any = None
    dimming: Any = None


@dataclass
class NoonChange:
    guid: str = None
    tid: int = None
    fields: list[NoonField] = None


@dataclass
class NoonChangeLightsOnRequest:
    space: str = None
    lightsOn: bool = None
    tid: int = None


@dataclass
class NoonChangeSceneRequest:
    space: str = None
    activeScene: str = None
    f129on: bool = None
    tid: int = None


@dataclass
class NoonChangeWholeHomeSceneRequest:
    structure: str = None
    scene: str = None


@dataclass
class NoonCurrentSamplingRequest:
    line: str = None
    propagateDimCurve: bool = None
    isSteadyState: bool = None


@dataclass
class NoonData:
    changes: list[NoonChange] = None


@dataclass
class NoonDevice:
    guid: str = None
    accessoryControlGuid: str = None
    name: str = None
    displayName: str = None
    serial: str = None
    isActive: bool = None
    type: str = None
    isMaster: bool = None
    isOnline: bool = None
    hardwareRevision: str = None
    softwareVersion: str = None
    expectedSoftwareVersion: str = None
    expectedLinesGuid: str = None
    actualLinesGuid: str = None
    expectedScenesGuid: str = None
    actualScenesGuid: str = None
    baseSerial: str = None
    mode: str = None
    modelNumber: str = None
    batteryLevel: int = None
    apRssi: int = None
    currentSamplingState: str = None
    dimmingAllowed: bool = None
    scenesAllowed: bool = None
    activeDimmingCurve: int = None
    pairingToken: str = None
    base: NoonBase = None
    line: NoonLine = None
    otaState: NoonOtaState = None
    smartBulbs: list = None
    capabilities: NoonDeviceCapability = None
    #beaconItem: NoonBeaconItem = None


@dataclass
class NoonDeviceAttribute:
    name: str = None
    displayName: str = None


@dataclass
class NoonDeviceAttributeResponse:
    name: str = None
    old_name: str = None
    displayName: str = None
    old_displayName: str = None


@dataclass
class NoonDeviceCapability:
    maxScenes: int = None
    wholeHomeRequest: int = None
    wholeHomeState: int = None
    hue: int = None
    elvisCapability: int = None
    iconSet: int = None
    gridView: int = None
    preconfiguredMultiway: int = None
    wholeHomeScenes: int = None


@dataclass
class NoonDexResponse:
    endpoints: NoonEndpoints = None
    partition: str = None
    ttl: int = None


@dataclass
class NoonDexUrls:
    privacyPolicy: str = None
    termsOfService: str = None
    emailVerificationKB: str = None
    dimmingKB: str = None
    alexaKB: str = None
    schedulingKB: str = None
    googleAssistantKB: str = None
    pairingKB: str = None
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


@dataclass
class NoonExternalDevice:
    externalId: str = None
    isOnline: bool = None


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


@dataclass
class NoonLight:
    guid: str = None
    bulbBrand: str = None
    bulbQuantity: int = None
    bulbType: str = None
    fixtureType: str = None


@dataclass
class NoonLightsOnStructureRequest:
    lightsOn: bool = None
    structure: str = None
    tid: int = None


@dataclass
class NoonLine:
    guid: str = None
    displayName: str = None
    remoteControllable: bool = None
    preconfigured: bool = None
    lineState: str = None
    dimmingLevel: int = None
    bulbType: str = None
    lights: list[NoonLight] = None
    externalDevices: list[NoonExternalDevice] = None
    multiwayMaster: NoonMultiwayMaster = None


@dataclass
class NoonLoginRequest:
    email: str = None
    password: int = None
    lifetime: int = None


@dataclass
class NoonLoginResponse:
    token: str = None
    lifetime: int = None
    renewLifetime: int = None


@dataclass
class NoonLightLevel:
    value: int = None
    recommendedMax: int = None
    recommendedMin: int = None
    lineState: str = None
    line: NoonLine = None
    #smartBulb: NoonSmartBulb = None


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


@dataclass
class NoonNightLightMode:
    enabled: bool = None
    scheduleOn: NoonScheduleOn = None
    scheduleOff: NoonScheduleOff = None
    spaces: list[NoonSpace] = None


@dataclass
class NoonOtaRequest:
    guid: str = None


@dataclass
class NoonOtaState:
    type: str = None
    guid: str = None
    retryCount: int = None
    installState: str = None
    percentDownloaded: float = None


@dataclass
class NoonPreference:
    key: str = None
    value: str = None


@dataclass
class NoonProvisionedKey:
    serial: str = None
    guid: str = None
    key: str = None


@dataclass
class NoonProvisionedKeyHolder:
    provisionedKey: NoonProvisionedKey = None


@dataclass
class NoonPulseLineRequest:
    line: str = None
    onTime: int = None
    offTime: int = None
    count: int = None


@dataclass
class NoonScene:
    guid: str = None
    name: str = None
    icon: str = None
    isActive: bool = None
    lightLevels: list[NoonLightLevel] = None
    transitionOn: int = None
    transitionOff: int = None
    hidden: bool = None
    motionActivated: bool = None
    type: str = None


@dataclass
class NoonSceneSchedule:
    guid: str = None
    name: str = None
    enabled: bool = None
    onTime: NoonSchedule = None
    offTime: NoonSchedule = None
    daysOfWeek = list
    space: NoonSpace = None
    scene: NoonScene = None


@dataclass
class NoonSchedule:
    day: int = None
    hour: int = None
    minute: int = None
    type: str = None
    relativeTo: str = None


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


@dataclass
class NoonSetLineLightLevelRequest:
    line: str = None
    lightLevel: int = None
    tid: int = None
    transitionTime: int = None


@dataclass
class NoonSetLineLightsOnRequest:
    line: str = None
    lightsOn: bool = None
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


@dataclass
class NoonSmartBulb:
    guid: str = None
    name: str = None
    fixtureType: str = None
    brand: str = None
    attributes: list[NoonAttribute] = None


@dataclass
class NoonSpace:
    name: str = None
    guid: str = None
    icon: str = None
    type: str = None
    occupancyDetected: bool = None
    lightingConfigModified: bool = None
    lines: list[NoonLine] = None
    lightsOn: bool = None
    activeScene: NoonScene = None
    activeSceneSchedule: NoonActiveSceneSchedule = None
    scenes: list[NoonScene] = None
    devices: list[NoonDevice] = None
    subspaces: list[NoonArea] = None
    settings: list[NoonSpaceSetting] = None


@dataclass
class NoonSpaceSetting:
    key: str = None
    value: str = None


@dataclass
class NoonStructure:
    name: str = None
    guid: str = None
    icon: str = None
    spaces: list[NoonSpace] = None
    timezone: str = None
    zipcode: str = None
    vacationMode: NoonVacationMode = None
    nightLightMode: NoonNightLightMode = None
    sceneSchedules: list[NoonSceneSchedule] = None
    activeScene: str = None
    sceneOrder: str = None
    scenes: list[NoonWholeHomeScene] = None


@dataclass
class NoonStructure__:
    guid: str = None
    accountInvitations: list[NoonAccountInvitation] = None


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


@dataclass
class NoonUser:
    guid: str = None
    name: str = None
    emailValid: str = None
    #incomingInvitations: list[NoonIncomingInvitation] = None
    #outgoingInvitations: list[NoonOutgoingInvitation] = None


@dataclass
class NoonVacationMode:
    enabled: bool = None
    spaces: list[NoonSpace] = None

    # def describeContents():
    #    return 0


@dataclass
class NoonVersions:
    currentVersion: int = None
    recommendedVersion: int = None
    requiredVersion: int = None


@dataclass
class NoonViper:
    event: str = None
    data: NoonData = None


@dataclass
class NoonWholeHomeScene:
    name: str = None
    guid: str = None
    spaces: list[NoonWholeHomeSceneSpace] = None
    controlSpaces: list[NoonWholeHomeSceneControlSpace] = None


@dataclass
class NoonWholeHomeSceneControlSpace:
    guid: str = None


@dataclass
class NoonWholeHomeSceneSpace:
    spaceGuid: str = None
    sceneGuid: str = None
    allOff: bool = None


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
