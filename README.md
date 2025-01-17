# Sphero_Force_Band_Python

This code allows you to control the Sphero Force Band, which was offered as an optional accessory to the Sphero BB-8 robot, programmatically, using Python. It utilises the Bleak Library (https://github.com/hbldh/bleak) for Bluetooth LE connectivity. Developed and tested on Linux. Should work
on Windows and MacOS, too.

It's still very basic and wip, but I plan to extend it as time permits.

# Similarities to other Sphero Toys

The force band is *very* similar to the Sphero Robots.
* It's offering the same Bluetooh services and characteristics with the same UUIDs.
* The package format and protocol is the same (https://sdk.sphero.com/documentation/api-documents).
* The device IDs, commands and data payload are (mostly?) the same as for comparable actions of the Sphero Robots.

The many Python libraries and tools for controlling Sphero Robots that exist out there, should mostly also work for the Force Band with some smaller adaptations:
*  Extending the initialization, so the Force Band is also identified as a supported device.
*  Figuring out, which devices / commands are supported by the Force Band (still working on that).

# Commands supported

* System mode switch
  * Activity selection mode
  * Mode required for playing audio
* Playing audio files stored on the device
* Setting the audio volume

Todo:
* Reading audio volume
* Stopping audio before it has finished playing
* Reading battery information
* Reading sensor (gyroscope, accelerometer, magnetometer?) data
* Enabling "rumble/force feedback" effect (if at all possible independently of force awareness mode)
* Figuring out, which audio files stored on the device have which IDs
* Change colour and brightness of the LED around the button (if possible at all)
* Receive notification when the buttion is being pressed
* Switching weapons
* Change aiming mode
* Reading an manipulating information about available weapons
* Manipulate holocron count
* Enter and manipulate force awareness mode
* ...

# Installation
* Clone the repo
* Install dependencies: asyncio, bleak ("python -m pip install -r requirements.txt")

The code was written and tested in Python 3.12

# Inspirations
The code is based on and inspired from
* https://github.com/Artucuno/Sphero_Bolt_Bleak/
* https://github.com/al5681/Sphero_Bolt_Multiplatform_Python_Bleak
* https://github.com/artificial-intelligence-class/spherov2.py
* https://sdk.sphero.com/documentation/api-documents


