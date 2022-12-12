"""Platform for light integration."""
import logging

# Import the device class from the component that you want to support
from homeassistant.components.climate import (
    ClimateEntity,
    HVACMode,
    ClimateEntityFeature,
    PRESET_HOME,
    HVACAction,
)
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS
from .const import (
    DOMAIN,
    HVAC_MODES,
    SUPPORT_PRESET,
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
        HVAC_action: HVACAction,
        HVAC_mode: HVACMode,
        current_temperature,
        target_temperature,
        cool_Limit_Max,
        cool_Limit_Min,
        heat_Limit_Max,
        heat_Limit_Min,
        climate_hub,
        temperature_unit=TEMP_CELSIUS,
    ):
        _LOGGER.debug(
            "###[%s]\ncurrent_temperature: %s\ntarget_temperature: %s\ncool_Limit_Max: %s\ncool_Limit_Min: %s\nheat_Limit_Max: %s\nheat_Limit_Min: %s\nHVAC_mode: %s\nHVAC_action: %s",
            id,
            current_temperature,
            target_temperature,
            cool_Limit_Max,
            cool_Limit_Min,
            heat_Limit_Max,
            heat_Limit_Min,
            HVAC_mode,
            HVAC_action,
        )

        ComelitDevice.__init__(self, id, None, description)
        self._climate = climate_hub
        self._current_temperature = current_temperature
        self._target_temperature = target_temperature
        self._cool_Limit_Max = cool_Limit_Max
        self._cool_Limit_Min = cool_Limit_Min
        self._heat_Limit_Max = heat_Limit_Max
        self._heat_Limit_Min = heat_Limit_Min
        self._hvac_mode = HVAC_mode
        self._hvac_action = HVAC_action
        self._temperature_unit = temperature_unit
        self._supported_features = ClimateEntityFeature.TARGET_TEMPERATURE

    @property
    def supported_features(self):
        return self._supported_features

    @property
    def temperature_unit(self):
        return self._temperature_unit

    @property
    def current_temperature(self):
        return self._current_temperature

    @property
    def target_temperature(self):
        return self._target_temperature

    @property
    def min_temp(self):
        if self._hvac_mode == HVACMode.cool:
            return self._cool_Limit_Min
        return self.heat_Limit_Min

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        if self._hvac_mode == HVACMode.cool:
            return self.cool_Limit_Max
        return self.heat_Limit_Max

    @property
    def hvac_mode(self) -> HVACMode:
        return self._hvac_mode

    @property
    def hvac_modes(self):
        return HVAC_MODES

    @property
    def hvac_action(self):
        return self._hvac_action

    @property
    def preset_mode(self):
        return PRESET_HOME

    @property
    def preset_modes(self):
        return SUPPORT_PRESET

    def update_state(
        self,
        state,
        hvac_action: HVACAction,
        hvac_mode: HVACMode,
        current_temperature,
        target_temperature,
    ):
        super().update_state(state)
        if (
            self._current_temperature != current_temperature
            or self._target_temperature != target_temperature
            or self._hvac_mode != hvac_mode
            or self._hvac_action != hvac_action
        ):
            _LOGGER.debug(
                "[%s] Switching to %s [%s] with %s °C [%s °C]",
                self.name,
                hvac_mode,
                hvac_action,
                current_temperature,
                target_temperature,
            )

        self._current_temperature = current_temperature
        self._target_temperature = target_temperature
        self._hvac_mode = hvac_mode
        self._hvac_action = hvac_action

        # TODO: check if update than do that

        self.async_schedule_update_ha_state()

    def set_hvac_mode(self, hvac_mode: HVACMode):
        if hvac_mode == HVACMode.AUTO:
            self._climate.climate_on_auto(self._id)
        elif hvac_mode == HVACMode.HEAT:
            self._climate.climate_set_winter(self._id)
        elif hvac_mode == HVACMode.COOL:
            self._climate.climate_set_summer(self._id)
        elif hvac_mode == HVACMode.OFF:
            self._climate.climate_off(self._id)

        _LOGGER.debug(
            "[%s] Switching to %s",
            self.name,
            hvac_mode,
        )

    def set_temperature(self, **kwargs):
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return

        if self._hvac_mode in (HVACMode.AUTO):
            self._climate.climate_on_manual(self._id)

        self._climate.climate_set_temperature(self._id, temperature)

        _LOGGER.debug(
            "[%s] Switching to %s °C",
            self.name,
            self._target_temperature,
        )
