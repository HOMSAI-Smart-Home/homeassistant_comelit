"""Platform for light integration."""
import logging

# Import the device class from the component that you want to support
from homeassistant.components.climate import ClimateEntity
from homeassistant.const import STATE_ON

from .const import DOMAIN
from .comelit_device import ComelitDevice

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    hass.data[DOMAIN]['hub'].light_add_entities = add_entities
    _LOGGER.info("Comelit Light Integration started")


class ComelitClimate(ComelitDevice, ClimateEntity):

    def __init__(self, id, description, state, , climate_hub):
        ComelitDevice.__init__(self, id, None, description)
        self._climate = climate_hub
        self._state = state
        self._current_temperature = current_temperature
        self._current_temperature = target_temperature

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

    def turn_on(self, **kwargs):
        self._climate.climate_on(self._id)

    def turn_off(self, **kwargs):
        self._climate.climate_off(self._id)
