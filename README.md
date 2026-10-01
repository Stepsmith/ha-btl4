# BTL4 Bluetooth Dimmer for Home Assistant

A custom Home Assistant integration for the **BTL4 4-channel Bluetooth dimmer** by **Wilhelm Koch**.

The integration communicates locally with the BTL4 via Bluetooth and exposes its four dimmer channels as individual light entities in Home Assistant.

No cloud connection is required.

## Features

- Automatic Bluetooth discovery
- Local Bluetooth communication
- Four independently controllable light channels
- Turn each channel on and off
- Adjust the brightness of each channel
- Home Assistant device and entity integration
- German and English translations
- Manual setup by Bluetooth MAC address if automatic discovery is not available
- No cloud account required

## Requirements

- Home Assistant with working Bluetooth support
- A Bluetooth adapter supported by Home Assistant
- A compatible BTL4 Bluetooth dimmer
- The BTL4 must be within Bluetooth range of Home Assistant or a supported Bluetooth proxy

## Supported hardware

This integration was developed for the **BTL4 4-Kanal Dimmer Bluetooth** manufactured by **Wilhelm Koch**.

Known device characteristics:

- Model: BTL4
- Supply voltage: 12 V DC
- Maximum load: 36 W
- Four dimmer channels
- Bluetooth Low Energy (BLE)

The integration uses Bluetooth advertisement data to identify compatible BTL4 devices.

Support for other Bluetooth dimmers or other devices from the same manufacturer is not implied.

## Installation with HACS

Until this repository is available in the default HACS repository list, it can be added as a custom repository.

1. Open HACS in Home Assistant.
2. Open the custom repository dialog.
3. Add:

   `https://github.com/Stepsmith/ha-btl4`

4. Select **Integration** as the repository type.
5. Install **BTL4 Bluetooth Dimmer**.
6. Restart Home Assistant.

After the restart, Home Assistant should automatically discover a compatible BTL4 that is in Bluetooth range.

## Manual installation

Copy the directory:

`custom_components/btl4`

from this repository to:

`/config/custom_components/btl4`

in your Home Assistant installation.

The resulting structure should look like this:

```text
/config/custom_components/btl4/
├── __init__.py
├── config_flow.py
├── const.py
├── light.py
├── manifest.json
└── translations/
    ├── de.json
    └── en.json
cat > /config/ha-btl4/README.md <<'EOF'
# BTL4 Bluetooth Dimmer for Home Assistant

A custom Home Assistant integration for the **BTL4 4-channel Bluetooth dimmer** by **Wilhelm Koch**.

The integration communicates locally with the BTL4 via Bluetooth and exposes its four dimmer channels as individual light entities in Home Assistant.

No cloud connection is required.

## Features

- Automatic Bluetooth discovery
- Local Bluetooth communication
- Four independently controllable light channels
- Turn each channel on and off
- Adjust the brightness of each channel
- Home Assistant device and entity integration
- German and English translations
- Manual setup by Bluetooth MAC address if automatic discovery is not available
- No cloud account required

## Requirements

- Home Assistant with working Bluetooth support
- A Bluetooth adapter supported by Home Assistant
- A compatible BTL4 Bluetooth dimmer
- The BTL4 must be within Bluetooth range of Home Assistant or a supported Bluetooth proxy

## Supported hardware

This integration was developed for the **BTL4 4-Kanal Dimmer Bluetooth** manufactured by **Wilhelm Koch**.

Known device characteristics:

- Model: BTL4
- Supply voltage: 12 V DC
- Maximum load: 36 W
- Four dimmer channels
- Bluetooth Low Energy (BLE)

The integration uses Bluetooth advertisement data to identify compatible BTL4 devices.

Support for other Bluetooth dimmers or other devices from the same manufacturer is not implied.

## Installation with HACS

Until this repository is available in the default HACS repository list, it can be added as a custom repository.

1. Open HACS in Home Assistant.
2. Open the custom repository dialog.
3. Add `https://github.com/Stepsmith/ha-btl4`.
4. Select **Integration** as the repository type.
5. Install **BTL4 Bluetooth Dimmer**.
6. Restart Home Assistant.

After the restart, Home Assistant should automatically discover a compatible BTL4 that is in Bluetooth range.

## Manual installation

Copy the directory `custom_components/btl4` from this repository to `/config/custom_components/btl4` in your Home Assistant installation.

The resulting structure should look like this:

    /config/custom_components/btl4/
    ├── __init__.py
    ├── config_flow.py
    ├── const.py
    ├── light.py
    ├── manifest.json
    └── translations/
        ├── de.json
        └── en.json

Restart Home Assistant after copying the files.

## Setup

### Automatic discovery

With a compatible BTL4 in Bluetooth range, Home Assistant should display **BTL4 Bluetooth Dimmer discovered**.

Select **Add** and follow the Home Assistant setup dialog.

Four light entities will be created:

- Channel 1
- Channel 2
- Channel 3
- Channel 4

With the German Home Assistant language, these are displayed as:

- Kanal 1
- Kanal 2
- Kanal 3
- Kanal 4

### Manual setup

If automatic discovery is not available:

1. Go to **Settings → Devices & services**.
2. Select **Add integration**.
3. Search for **BTL4 Bluetooth Dimmer**.
4. Enter the Bluetooth MAC address of the BTL4.

## Bluetooth

The integration communicates directly with the BTL4 using Bluetooth Low Energy.

Pairing or bonding the BTL4 with the operating system is not required for normal operation.

For reliable operation, make sure that the BTL4 has a sufficiently strong Bluetooth connection to Home Assistant or a supported Bluetooth proxy.

## Troubleshooting

If the BTL4 is not discovered automatically:

- Verify that Bluetooth is working in Home Assistant.
- Make sure the BTL4 is powered on.
- Make sure the BTL4 is within Bluetooth range.
- Check that Home Assistant can see the device in the Bluetooth integration.
- Restart the BTL4 and wait for it to advertise again.

If the device is discovered but cannot be controlled, check the Home Assistant logs for messages containing `btl4`.

## Compatibility

This integration is based on the Bluetooth protocol observed on the BTL4 hardware used during development.

Different hardware or firmware revisions may behave differently.

If you have another BTL4 revision that does not work, please open an issue and include as much information about the device and Home Assistant Bluetooth diagnostics as possible.

## Issues

Problems and compatibility reports can be submitted at:

https://github.com/Stepsmith/ha-btl4/issues

## Disclaimer

This is an independent community project.

It is not an official integration from Wilhelm Koch and is not affiliated with or endorsed by the manufacturer.

## Deutsch

Diese benutzerdefinierte Home-Assistant-Integration ermöglicht die lokale Steuerung des **BTL4 4-Kanal Bluetooth-Dimmers von Wilhelm Koch**.

Unterstützt werden:

- automatische Bluetooth-Erkennung
- vier unabhängig steuerbare Kanäle
- Ein- und Ausschalten
- Helligkeitssteuerung
- lokale Kommunikation ohne Cloud
- deutsche Bezeichnungen `Kanal 1` bis `Kanal 4`
- manuelle Einrichtung über die Bluetooth-MAC-Adresse als Alternative zur automatischen Erkennung

Nach der Installation und einem Neustart von Home Assistant sollte ein kompatibler BTL4 automatisch unter **Einstellungen → Geräte & Dienste** als entdeckt angezeigt werden.

Diese Integration ist ein unabhängiges Community-Projekt und keine offizielle Integration des Herstellers.

## License

See [LICENSE](LICENSE).
