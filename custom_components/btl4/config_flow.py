"""Config flow for the BTL4 Bluetooth Dimmer."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak
from homeassistant.const import CONF_ADDRESS
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.device_registry import format_mac

from .const import DOMAIN


class BTL4ConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a config flow for BTL4."""

    VERSION = 1

    async def async_step_bluetooth(
        self,
        discovery_info: BluetoothServiceInfoBleak,
    ) -> FlowResult:
        """Handle Bluetooth discovery."""

        # Manufacturer ID 89 triggers the Bluetooth discovery flow.
        # Verify the BTL4-specific manufacturer-data fingerprint before
        # offering the device for configuration.
        #
        # Byte 1 contains variable data and is deliberately ignored.
        manufacturer_data = discovery_info.manufacturer_data.get(89)

        if (
            manufacturer_data is None
            or len(manufacturer_data) < 6
            or manufacturer_data[2:6] != bytes.fromhex("DE F3 18 02")
        ):
            return self.async_abort(reason="not_btl4")

        address = format_mac(discovery_info.address)

        await self.async_set_unique_id(address)
        self._abort_if_unique_id_configured()

        self.context["title_placeholders"] = {
            "name": "BTL4 Bluetooth Dimmer"
        }

        return await self.async_step_bluetooth_confirm()

    async def async_step_bluetooth_confirm(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Confirm a discovered BTL4."""

        if user_input is not None:
            address = self.unique_id

            if address is None:
                return self.async_abort(
                    reason="cannot_connect"
                )

            return self.async_create_entry(
                title="BTL4 Bluetooth Dimmer",
                data={
                    CONF_ADDRESS: address,
                },
            )

        return self.async_show_form(
            step_id="bluetooth_confirm",
            description_placeholders={
                "name": "BTL4 Bluetooth Dimmer"
            },
        )

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle manual setup."""

        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                address = format_mac(
                    user_input[CONF_ADDRESS]
                )
            except (TypeError, ValueError):
                errors["base"] = "invalid_address"
            else:
                await self.async_set_unique_id(address)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title="BTL4 Bluetooth Dimmer",
                    data={
                        CONF_ADDRESS: address,
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_ADDRESS): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )