"""Platform for light integration."""
import logging

# Import the device class from the component that you want to support
from homeassistant.components.climate import ClimateEntity
from homeassistant.const import STATE_ON, ATTR_TEMPERATURE
from .const import (
    CONST_MODE_AUTO,
    CONST_MODE_COOL,
    CONST_MODE_HEAT,
    CONST_MODE_OFF,
    DOMAIN)
from .comelit_device import ComelitDevice

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    hass.data[DOMAIN]['hub'].light_add_entities = add_entities
    _LOGGER.info("Comelit Light Integration started")


class ComelitClimate(ComelitDevice, ClimateEntity):

    def __init__(self, id, description, state, climate_hub):
        ComelitDevice.__init__(self, id, None, description)
        self._climate = climate_hub
        self._state = state
        self._current_temperature = current_temperature
        self._target_temperature = target_temperature

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state == STATE_ON

    @property
    def current_temperature(self):
        return self._current_temperature

    @property
    def target_temperature(self):
        return self._target_temperature

    def update(self):
        pass
        # self._state = self._light.state(self._id)

    def set_hvac_mode(self, hvac_mode) -> None:
        if hvac_mode == CONST_MODE_AUTO:
            self._climate.climate_on_auto(self._id)
        elif hvac_mode == CONST_MODE_HEAT:
            self._climate.climate_set_winter(self._id)
        elif hvac_mode == CONST_MODE_COOL:
            self._climate.climate_set_summer(self._id)
        elif hvac_mode == CONST_MODE_OFF:
            self._climate.climate_off(self._id)

    def set_temperature(self, **kwargs) -> None:
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return
        #self._climate.climate_on_manual(self._id) # idk if this is necessary, must be tested
        self._climate.climate_set_temperature(self._id, temperature)

