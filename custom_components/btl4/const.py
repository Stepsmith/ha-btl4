"""Constants for the BTL4 Bluetooth Dimmer integration."""

DOMAIN = "btl4"

# BTL4 GATT characteristic handles.
INIT_HANDLE = 0x001E

CHANNEL_HANDLES = {
    1: 0x002B,
    2: 0x0031,
    3: 0x0037,
    4: 0x003D,
}

# Command required to initialize the BTL4 after connecting.
INIT_DATA = bytes.fromhex("ff ff ff fd 5c 24")

# Number of independently controllable dimmer channels.
CHANNEL_COUNT = 4