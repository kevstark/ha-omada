"""Platform for sensor integration."""
from homeassistant.const import DATA_BYTES, DATA_RATE_BYTES_PER_SECOND
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.device_registry import format_mac
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.core import callback

from homeassistant.components.device_tracker import DOMAIN, PLATFORM_SCHEMA

from custom_components.omada.api.controller import Controller

from .controller import OmadaController
from .const import CONF_SSID_FILTER, CONF_SITE, DATA_OMADA, DOMAIN as OMADA_DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):

    controller: OmadaController = hass.data[OMADA_DOMAIN][config_entry.entry_id][
        DATA_OMADA
    ]
    controller.entities[DOMAIN] = set()

    def get_devices():
        devices = set()

        for mac in controller.api.devices:
            device = controller.api.devices[mac]
            devices.add(device.mac)

        return devices

    @callback
    def items_added(macs: set = get_devices()):
        add_entities(controller, async_add_entities, macs)

    config_entry.async_on_unload(
        async_dispatcher_connect(hass, controller.signal_update, items_added)
    )

    initial_set = set()

    # Add connected entries
    for mac in get_devices():
        initial_set.add(mac)

    items_added(initial_set)


@callback
def add_entities(controller: Controller, async_add_entities, macs):
    sensors = []

    for mac in macs:
        if mac in controller.entities[DOMAIN]:
            continue

        if mac in controller.api.devices:
            sensors.append(UploadSensor(controller, mac))
            sensors.append(DownloadSensor(controller, mac))
            sensors.append(TxSensor(controller, mac))
            sensors.append(RxSensor(controller, mac))

    if sensors:
        async_add_entities(sensors)


class UploadSensor(Entity):
    """Representation of a Sensor."""

    DOMAIN = DOMAIN

    def __init__(self, controller: OmadaController, mac):
        """Initialize the sensor."""
        self._state = None
        self._controller = controller
        self._mac = mac
        self._controller.entities[DOMAIN].add(mac)

    @property
    def device_info(self):
        device = self._controller.api.devices[self._mac]
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (self.DOMAIN, format_mac(self._mac))
            }
        }

    @property
    def unique_id(self) -> str:
        return f"{format_mac(self._mac)}_upload"

    @property
    def name(self):
        """Return the name of the sensor."""
        # Replace default site name if not set
        site = self._controller.api.site
        if site == "Default":
            site = "Omada"
        name = self._controller.api.devices[self._mac].name
        return f"{site.title()} {name.title()} Upload"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return DATA_BYTES

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._controller.api.devices[self._mac].upload


class DownloadSensor(Entity):
    """Representation of a Sensor."""

    DOMAIN = DOMAIN

    def __init__(self, controller: OmadaController, mac):
        """Initialize the sensor."""
        self._state = None
        self._controller = controller
        self._mac = mac
        self._controller.entities[DOMAIN].add(mac)

    @property
    def device_info(self):
        device = self._controller.api.devices[self._mac]
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (self.DOMAIN, format_mac(self._mac))
            }
        }

    @property
    def unique_id(self) -> str:
        return f"{format_mac(self._mac)}_download"

    @property
    def name(self):
        """Return the name of the sensor."""
        # Replace default site name if not set
        site = self._controller.api.site
        if site == "Default":
            site = "Omada"
        name = self._controller.api.devices[self._mac].name
        return f"{site.title()} {name.title()} Download"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return DATA_BYTES

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._controller.api.devices[self._mac].download


class TxSensor(Entity):
    """Representation of a Sensor."""

    DOMAIN = DOMAIN

    def __init__(self, controller: OmadaController, mac):
        """Initialize the sensor."""
        self._state = None
        self._controller = controller
        self._mac = mac
        self._controller.entities[DOMAIN].add(mac)

    @property
    def device_info(self):
        device = self._controller.api.devices[self._mac]
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (self.DOMAIN, format_mac(self._mac))
            }
        }

    @property
    def unique_id(self) -> str:
        return f"{format_mac(self._mac)}_tx"

    @property
    def name(self):
        """Return the name of the sensor."""
        # Replace default site name if not set
        site = self._controller.api.site
        if site == "Default":
            site = "Omada"
        name = self._controller.api.devices[self._mac].name
        return f"{site.title()} {name.title()} Tx"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return DATA_RATE_BYTES_PER_SECOND

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._controller.api.devices[self._mac].tx_rate


class RxSensor(Entity):
    """Representation of a Sensor."""

    DOMAIN = DOMAIN

    def __init__(self, controller: OmadaController, mac):
        """Initialize the sensor."""
        self._state = None
        self._controller = controller
        self._mac = mac
        self._controller.entities[DOMAIN].add(mac)

    @property
    def device_info(self):
        device = self._controller.api.devices[self._mac]
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (self.DOMAIN, format_mac(self._mac))
            }
        }

    @property
    def unique_id(self) -> str:
        return f"{format_mac(self._mac)}_rx"

    @property
    def name(self):
        """Return the name of the sensor."""
        # Replace default site name if not set
        site = self._controller.api.site
        if site == "Default":
            site = "Omada"
        name = self._controller.api.devices[self._mac].name
        return f"{site.title()} {name.title()} Rx"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return DATA_RATE_BYTES_PER_SECOND

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._controller.api.devices[self._mac].rx_rate
