"""Light platform for the BTL4 Bluetooth Dimmer."""

from __future__ import annotations

import asyncio
import logging

from bleak import BleakClient
from bleak_retry_connector import establish_connection

from homeassistant.components import bluetooth
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ColorMode,
    LightEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CHANNEL_COUNT,
    CHANNEL_HANDLES,
    DOMAIN,
    INIT_DATA,
    INIT_HANDLE,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up BTL4 light entities."""

    address = entry.data[CONF_ADDRESS].upper()
    controller = BTL4Controller(hass, address)

    entities = [
        BTL4Channel(controller, channel, address)
        for channel in range(1, CHANNEL_COUNT + 1)
    ]

    controller.set_entities(entities)
    async_add_entities(entities)


class BTL4Controller:
    """Manage one BTL4 Bluetooth Dimmer."""

    def __init__(
        self,
        hass: HomeAssistant,
        address: str,
    ) -> None:
        """Initialize the controller."""

        self.hass = hass
        self.address = address

        self.client: BleakClient | None = None
        self.lock = asyncio.Lock()

        self.initialized = False
        self.notifications_started = False
        self.entities: dict[int, BTL4Channel] = {}

    def set_entities(
        self,
        entities: list[BTL4Channel],
    ) -> None:
        """Associate entities with the controller."""

        self.entities = {
            entity.channel: entity
            for entity in entities
        }

    def _disconnected(
        self,
        client: BleakClient,
    ) -> None:
        """Handle a Bluetooth disconnection."""

        _LOGGER.debug(
            "BTL4 %s disconnected",
            self.address,
        )

        self.client = None
        self.initialized = False
        self.notifications_started = False

    async def _connect(self) -> None:
        """Establish a Bluetooth connection when needed."""

        if self.client is not None and self.client.is_connected:
            return

        device = bluetooth.async_ble_device_from_address(
            self.hass,
            self.address,
            connectable=True,
        )

        if device is None:
            raise RuntimeError(
                f"BTL4 {self.address} is currently not visible "
                "to Home Assistant Bluetooth"
            )

        _LOGGER.debug(
            "Connecting to BTL4 %s",
            self.address,
        )

        self.client = await establish_connection(
            BleakClient,
            device,
            self.address,
            disconnected_callback=self._disconnected,
        )

        self.initialized = False
        self.notifications_started = False

        await self._start_notifications()

        _LOGGER.debug(
            "Connected to BTL4 %s",
            self.address,
        )

    async def _start_notifications(self) -> None:
        """Subscribe to status notifications."""

        if self.notifications_started:
            return

        if self.client is None:
            raise RuntimeError(
                "BTL4 Bluetooth client is not connected"
            )

        for channel, handle in CHANNEL_HANDLES.items():
            characteristic = self.client.services.get_characteristic(
                handle
            )

            if characteristic is None:
                raise RuntimeError(
                    f"BTL4 channel {channel}: "
                    f"characteristic 0x{handle:04X} not found"
                )

            await self.client.start_notify(
                characteristic,
                self._make_notification_callback(channel),
            )

        self.notifications_started = True

    def _make_notification_callback(
        self,
        channel: int,
    ):
        """Create notification callback for one channel."""

        def callback(sender, data):
            self._handle_status(channel, bytes(data))

        return callback

    def _handle_status(
        self,
        channel: int,
        data: bytes,
    ) -> None:
        """Process a channel status notification."""

        _LOGGER.debug(
            "BTL4 %s channel %s notification: %s",
            self.address,
            channel,
            data.hex(" "),
        )

        if len(data) < 2:
            return

        entity = self.entities.get(channel)

        if entity is None:
            return

        entity._attr_is_on = data[0] == 0x01

        if entity._attr_is_on and data[1] > 0:
            entity._attr_brightness = data[1]

        if entity.hass is not None:
            entity.async_write_ha_state()

    async def _initialize(self) -> None:
        """Initialize the BTL4 after connecting."""

        if self.initialized:
            return

        if self.client is None:
            raise RuntimeError(
                "BTL4 Bluetooth client is not connected"
            )

        characteristic = self.client.services.get_characteristic(
            INIT_HANDLE
        )

        if characteristic is None:
            raise RuntimeError(
                "BTL4 initialization characteristic not found"
            )

        await self.client.write_gatt_char(
            characteristic,
            INIT_DATA,
            response=True,
        )

        self.initialized = True

        _LOGGER.debug(
            "BTL4 %s initialized",
            self.address,
        )

    async def write_channel(
        self,
        channel: int,
        data: bytes,
    ) -> None:
        """Write a command to one BTL4 channel."""

        async with self.lock:
            try:
                await self._connect()
                await self._initialize()

                if self.client is None:
                    raise RuntimeError(
                        "BTL4 Bluetooth client is not connected"
                    )

                handle = CHANNEL_HANDLES[channel]

                characteristic = (
                    self.client.services.get_characteristic(handle)
                )

                if characteristic is None:
                    raise RuntimeError(
                        f"BTL4 channel {channel}: "
                        f"characteristic 0x{handle:04X} not found"
                    )

                _LOGGER.debug(
                    "BTL4 %s channel %s write: %s",
                    self.address,
                    channel,
                    data.hex(" "),
                )

                await self.client.write_gatt_char(
                    characteristic,
                    data,
                    response=True,
                )

            except Exception:
                self.initialized = False
                self.notifications_started = False

                client = self.client
                self.client = None

                if client is not None and client.is_connected:
                    try:
                        await client.disconnect()
                    except Exception:
                        _LOGGER.debug(
                            "Error disconnecting BTL4 %s",
                            self.address,
                            exc_info=True,
                        )

                raise


class BTL4Channel(LightEntity):
    """Represent one BTL4 dimmer channel."""

    _attr_has_entity_name = True
    _attr_translation_key = "channel"

    _attr_supported_color_modes = {
        ColorMode.BRIGHTNESS
    }
    _attr_color_mode = ColorMode.BRIGHTNESS

    def __init__(
        self,
        controller: BTL4Controller,
        channel: int,
        address: str,
    ) -> None:
        """Initialize one BTL4 channel."""

        self.controller = controller
        self.channel = channel

        self._attr_translation_placeholders = {
            "channel": str(channel)
        }

        normalized_address = (
            address
            .replace(":", "")
            .replace("-", "")
            .lower()
        )

        self._attr_unique_id = (
            f"btl4_{normalized_address}_channel_{channel}"
        )

        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    normalized_address,
                )
            },
            name="BTL4 Bluetooth Dimmer",
            manufacturer="Wilhelm Koch",
            model="BTL4",
        )

        self._attr_is_on = False
        self._attr_brightness = 127

    async def async_turn_on(
        self,
        **kwargs,
    ) -> None:
        """Turn the channel on or set brightness."""

        if ATTR_BRIGHTNESS in kwargs:
            brightness = int(
                kwargs[ATTR_BRIGHTNESS]
            )

            brightness = max(
                1,
                min(255, brightness),
            )

            await self.controller.write_channel(
                self.channel,
                bytes(
                    [
                        0x01,
                        brightness,
                    ]
                ),
            )

        else:
            await self.controller.write_channel(
                self.channel,
                bytes(
                    [
                        0x01,
                        0x00,
                    ]
                ),
            )

    async def async_turn_off(
        self,
        **kwargs,
    ) -> None:
        """Turn the channel off."""

        await self.controller.write_channel(
            self.channel,
            bytes(
                [
                    0x00,
                    0x7F,
                ]
            ),
        )