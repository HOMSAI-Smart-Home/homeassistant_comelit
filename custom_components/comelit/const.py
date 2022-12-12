from homeassistant.components.climate import HVACMode, PRESET_HOME

DOMAIN = "comelit"
HUB_DOMAIN = "comelit.hub"
VEDO_DOMAIN = "comelit.vedo"
CONF_MQTT_USER = "mqtt-user"
CONF_MQTT_PASSWORD = "mqtt-password"
CONF_SERIAL = "serial"
CONF_CLIENT = "client"
COVER_CLOSING_TIME = 30  # TODO config

HVAC_MODES = [
    HVACMode.OFF,
    HVACMode.AUTO,
    HVACMode.HEAT,
    HVACMode.COOL,
]

SUPPORT_PRESET = [PRESET_HOME]
