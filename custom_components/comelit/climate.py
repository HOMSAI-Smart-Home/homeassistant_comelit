"""Platform for light integration."""
import logging

# Import the device class from the component that you want to support
from homeassistant.components.climate import (
    ClimateEntity,
    HVACMode,
    ClimateEntityFeature,
    PRESET_HOME,
)
from homeassistant.const import STATE_ON, ATTR_TEMPERATURE, TEMP_CELSIUS
from .const import (
    CONST_MODE_AUTO,
    CONST_MODE_COOL,
    CONST_MODE_HEAT,
    CONST_MODE_OFF,
    CONST_MODE_SMART_SCHEDULE,
    DOMAIN,
    HA_TO_HVAC_MODE_MAP,
    SUPPORT_PRESET,
    TO_HA_HVAC_MODE_MAP,
)
from .comelit_device import ComelitDevice

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    hass.data[DOMAIN]["hub"].climate_add_entities = add_entities
    _LOGGER.info("Comelit climate Integration started")


class ComelitClimate(ComelitDevice, ClimateEntity):
    def __init__(
        self,
        id,
        description,
        state,
        current_temperature,
        target_temperature,
        climate_hub,
        temperature_unit=TEMP_CELSIUS,
    ):
        ComelitDevice.__init__(self, id, None, description)
        self._climate = climate_hub
        self._state = state
        self._current_temperature = current_temperature
        self._target_temperature = target_temperature
        self._hvac_mode = CONST_MODE_HEAT
        self._temperature_unit = temperature_unit
        self._supported_features = (
            ClimateEntityFeature.PRESET_MODE | ClimateEntityFeature.TARGET_TEMPERATURE
        )

    @property
    def supported_features(self):
        return self._supported_features

    @property
    def temperature_unit(self):
        return self._temperature_unit

    @property
    def is_on(self):
        return self._state == STATE_ON

    @property
    def current_temperature(self):
        return self._current_temperature

    @property
    def target_temperature(self):
        return self._target_temperature

    @property
    def hvac_mode(self):
        return TO_HA_HVAC_MODE_MAP.get(self._current_tado_hvac_mode, HVACMode.OFF)

    @property
    def hvac_modes(self):
        hvac_modes = []
        for _, value in HA_TO_HVAC_MODE_MAP.items():
            hvac_modes.append(value)
        return hvac_modes

    @property
    def preset_mode(self):
        return PRESET_HOME

    @property
    def preset_modes(self):
        return SUPPORT_PRESET

    def update(
        self,
        state,
        current_temperature,
        target_temperature,
    ):
        self._state = state
        self._current_temperature = current_temperature
        self._target_temperature = target_temperature

    def set_hvac_mode(self, hvac_mode) -> None:
        self._control_hvac(hvac_mode=HA_TO_HVAC_MODE_MAP[hvac_mode])

        if self._hvac_mode == CONST_MODE_AUTO:
            self._climate.climate_on_auto(self._id)
        elif self._hvac_mode == CONST_MODE_HEAT:
            self._climate.climate_set_winter(self._id)
        elif self._hvac_mode == CONST_MODE_COOL:
            self._climate.climate_set_summer(self._id)
        elif self._hvac_mode == CONST_MODE_OFF:
            self._climate.climate_off(self._id)

    def set_temperature(self, **kwargs) -> None:
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return

        if self._hvac_mode not in (
            CONST_MODE_AUTO,
            CONST_MODE_SMART_SCHEDULE,
        ):
            self._control_hvac(target_temp=temperature)
            return

        # self._climate.climate_on_manual(self._id) # idk if this is necessary, must be tested

    def _control_hvac(self, hvac_mode=None, target_temp=None):
        if hvac_mode:
            self._hvac_mode = hvac_mode

        if target_temp:
            self._target_temperature = target_temp

        if self._hvac_mode == CONST_MODE_OFF:
            _LOGGER.debug("[%s] Switching to OFF", self.name)
            return

        if self._hvac_mode == CONST_MODE_SMART_SCHEDULE:
            _LOGGER.debug("[%s] Switching to SMART_SCHEDULE", self.name)
            return

        if target_temp:
            self._climate.climate_set_temperature(self._id, target_temp)

        _LOGGER.debug(
            "[%s] Switching to %s with temperature %s °C",
            self.name,
            self._hvac_mode,
            self._target_temperature,
        )
