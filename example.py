import asyncio

from sphero_force_band import ForceBand, ForceBandScan
from random import randrange
import random

async def spt(address):
    my_forceband = ForceBand(address)
    try:
        await my_forceband.connect()

        await my_forceband.wake()

        await asyncio.sleep(5)

        await my_forceband.switch_system_mode(0x0d)

        await my_forceband.set_volume(0xff)
        await my_forceband.play_audio()

        await asyncio.sleep(5)

        await my_forceband.set_volume(0x10)
        await my_forceband.play_audio()

        await my_forceband.switch_system_mode(0x0e)
        await asyncio.sleep(10)
    finally:
        await my_forceband.disconnect()

async def run():
    #Fixed MAC for testing
    #address = (
        #"C7:6B:67:C6:E3:B7"
    #)
    scan = ForceBandScan()
    #address = [await scan.scan()]
    address = await scan.scanAll()
    tasks = []
    for f in address:
        task = asyncio.ensure_future(spt(f))
        tasks.append(task)
        #await asyncio.create_task(spt(f))
        #await task_1
    # connect to Force Band
    responses = await asyncio.gather(*tasks)



if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.set_debug(True)
    loop.run_until_complete(run())
