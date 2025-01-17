import struct
from sphero_constants import *
from bleak import BleakClient
from bleak import BleakScanner

class ForceBandScan:
    def __init__(self):
        self.bolts = []

    async def scan(self, name=None):
        print(f'[SCAN] Scanning for Force Band device with name {name}')
        devices = await BleakScanner.discover()
        for de in devices:
            #print(de)
            try:
                if de.name.startswith('FB-'):
                    if name == None:
                        return de.address
                    else:
                        if name == de.name:
                            return de.address
            except Exception as e:
                print(e)


    async def scanAll(self):
        print(f'[SCAN] Scanning for all nearby Force Band devices')
        d = []
        devices = await BleakScanner.discover()
        for de in devices:
            try:
                if de.name.startswith('FB-'):
                    d += [de]
                    print('[SCAN] Force Band detected with name ' + de.name + ' and address ' + de.address)
            except:
                pass
        print('[SCAN] {} Force Band device detected'.format(len(d)))

        return d


class ForceBand:
    def __init__(self, address):
        self.sequence = 0
        self.address = address
        self.notificationPacket = []
        self.API_V2_characteristic = "00010002-574f-4f20-5370-6865726f2121"
        self.Anti_DOS_characteristic = "00020005-574f-4f20-5370-6865726f2121"
        self.DFU_Control_characteristic = "00020002-574f-4f20-5370-6865726f2121"
        self.DFU_Info_characteristic = "00020004-574f-4f20-5370-6865726f2121"


    async def connect(self):
        """
        Connects to a Force Band of a specified MAC address if it can find it.
        """
        self.client = BleakClient(self.address)
        await self.client.connect()
        print("[FOBA] Connected: {0}".format(self.client.is_connected))

        # cancel if not connected
        if not self.client.is_connected:
            return False

        # get device name
        #try:
        #DEVICE_NAME_UUID = "2A00"
        #DEVICE_NAME_UUID = "00002A00-0000-1000-8000-00805f9b34fb"
        #device_name = await self.client.read_gatt_char('2A00')
        #print(device_name)
        #print("Device Name: {0}".format("".join(map(chr, device_name))))
        #except Exception:
        #    pass
        # https://github.com/hbldh/bleak/issues/1498

        # Unlock code: prevent the sphero mini from going to sleep again after 10 seconds
        print("[INIT] Writing Anti DOS characteristic unlock code")
        try:
            await self.client.write_gatt_char(self.Anti_DOS_characteristic, b"usetheforce...band", response=True)
        except:
            return False

        print("[INIT] Initialization complete\n")

        return True

    async def disconnect(self):
        """
        Disconnects the Force Band
        """
        return await self.client.disconnect()

    async def send(self, characteristic=None, devID=None, commID=None, targetId=None, data=[]):
        """
        Generate databytes of command using input dictionary
        This protocol copied completely from JS library
        Messages are represented as:
        [start flags targetID sourceID deviceID commandID seqNum data
        checksum end]
        The flags byte indicates which fields are populated.
        The checksum is the ~sum(message[1:-2]) | 0xff.
        """
        try:
            self.sequence = (self.sequence + 1) % 256
            running_sum = 0
            command = []
            command.append(SendPacketConstants["StartOfPacket"])
            if targetId is None:
                cmdflg = Flags["requestsResponse"] | \
                         Flags["resetsInactivityTimeout"] | 0
                command.append(cmdflg)
                running_sum += cmdflg
            else:
                cmdflg = Flags["requestsResponse"] | \
                         Flags["resetsInactivityTimeout"] | targetId
                command.append(cmdflg)
                running_sum += cmdflg
                command.append(targetId)
                running_sum += targetId

            command.append(devID)
            running_sum += devID
            command.append(commID)
            running_sum += commID
            command.append(self.sequence)
            running_sum += self.sequence

            if data is not None:
                for datum in data:
                    command.append(datum)
                    running_sum += datum
            checksum = (~running_sum) & 0xff
            command.append(checksum)
            command.append(SendPacketConstants["EndOfPacket"])
            await self.client.write_gatt_char(characteristic, command)
            print("[PACK {}] {}".format(sequence, command))
        except Exception as e:
            #print(e)
            return

    async def wake(self):
        """
        Bring device out of sleep mode (can only be done if device was in sleep, not deep sleep).
        If in deep sleep, the device should be connected to USB power to wake.
        To be confirmed if sleep and wake work at all on the Force Band
        """
        print("[SEND {}] Waking".format(self.sequence))
        while True:
            try:
                await self.send(
                    characteristic=self.API_V2_characteristic,
                    devID=DeviceID["powerInfo"],
                    commID=PowerCommandIDs["wake"],
                    data=[])  # empty payload
                return
            except Exception as e:
                print('Error waking retrying', e)

    async def switch_system_mode(self, mode=None):
        """
        Switches the force band to another system mode. Possible values found so far
        0x0d This mode is a prerequisite for playing sounds on the force band. In this mode the dand doesn't react to button press
        0x0e The default "main menu" system mode where you can choose between the different activites.
        """
        print("[MODE {}] Switch System Mode".format(self.sequence))

        await self.send(characteristic=self.API_V2_characteristic,
            devID=DeviceID["system_modes"],
            commID=SystemModeCommandIDs["set_system_mode"],
            data=[mode])

    async def play_audio(self):
        """
        Playing an audio file stored on the force band.
        Prerequisite is calling switch_to_audio_mode first
        ID of the audio file is passed in the data payload
        Tbd which audio file has which payload
        [0x05, 0x8e, 0x00] is the id of the sound being played when changing the volume from the app
        """
        print("[SEND {}] Sound Test".format(self.sequence))

        await self.send(characteristic=self.API_V2_characteristic,
            devID=DeviceID["userIO"],
            commID=UserIOCommandIDs["play_audio_file"],
            data=[0x05, 0x8e, 0x00])

    async def set_volume(self, vol=None):
        """
        Changing the audio volume.
        Values between 0x00 and 0xff can be passed in the data payload
        """
        print("[SEND {0}] Set Volume {1}".format(self.sequence, vol))

        await self.send(characteristic=self.API_V2_characteristic,
            devID=DeviceID["userIO"],
            commID=UserIOCommandIDs["set_audio_volume"],
            data=[vol])

    def bitsToNum(self, bits):
        """
        This helper function decodes bytes from sensor packets into single precision floats. Encoding follows the
        the IEEE-754 standard.
        """
        num = int(bits, 2).to_bytes(len(bits) // 8, byteorder='little')
        num = struct.unpack('f', num)[0]
        return num
