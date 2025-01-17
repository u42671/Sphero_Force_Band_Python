DeviceID = {"apiProcessor": 16,
            "systemInfo": 17,
            "system_modes": 0x12,
            "powerInfo": 19,
#            "driving": 22,
            "sensor": 24,
            "userIO": 26,
            }

SendPacketConstants = {"StartOfPacket": 141,
                       "EndOfPacket": 216,
                       "ESC": 171}

UserIOCommandIDs = {"play_audio_file": 0x07,
                    "set_audio_volume": 0x08,
                    "get_audio_volume": 0x09,
#                    "allLEDs": 28,
#                    "matrixColor": 47,
#                    "matrixPix": 45,
#                    "printChar": 66
                    }

SystemModeCommandIDs = {"set_system_mode": 0x00,
                        "get_system_mode": 0x01,
                        "enable_system_mode_notification": 0x02,
                        "system_mode_changed": 0x03,
                        "enable_menu_item_change_notification": 0x0b,
                        }

SensorCommandIds = {"calibrateToNorth": 37}

PowerCommandIDs = {"wake": 13}

#DrivingCommands = {"driveWithHeading": 7,
#                   "resetYaw": 6}

Flags = {
    "isResponse": 1,
    "requestsResponse": 2,
    "requestsOnlyErrorResponse": 4,
    "resetsInactivityTimeout": 8,
    "commandHasTargetId": 16,
    "commandHasSourceId": 32
}

# Charcteristics
# =====================================================================

# API V2 Characteristic         <00010002-574f-4f20-5370-6865726f2121>
# Unknown2 Characteristic <00010003-574f-4f20-5370-6865726f2121>

# DFU Control Characteristic    <00020002-574f-4f20-5370-6865726f2121>
# Unknown1 Characteristic       <00020003-574f-4f20-5370-6865726f2121>
# DFU Info Characteristic       <00020004-574f-4f20-5370-6865726f2121>
# Anti DOS Characteristic       <00020005-574f-4f20-5370-6865726f2121>

# Name Characteristic <Device Name>
# Appearance Characteristic <Appearance>
# Peripheral Preferred Connection Parameters Characteristic <Peripheral Preferred Connection Parameters>

# Service Changed Characteristic <Service Changed>

# Battery Level Characteristic <Battery Level>
