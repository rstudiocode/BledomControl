#  Copyright 2023. Artem Sukhanov
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  SPDX-License-Identifier: GPL-3.0-or-later

import asyncio
import logging
import sys

from bleak import BleakError
from src.blecontroller.main import BledomDevice, BleController

logger = logging.getLogger(__file__)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)


async def connected(device: BledomDevice):
    logger.debug(f'Status {device.name} -> {device.connection_status}')


    try:
        if device.connection_status:
            pass
            # SOME TESTS
            await device.led_control.power_on()
            await device.led_control.set_color(0, 255, 0)
            await asyncio.sleep(1)
            await device.led_control.set_color('#0000FF')

            # await device.led_control.set_color(_hex_3='#EE3300')
            logger.debug('Complete')
    except BleakError as e:
        logger.error(e)
        print(f'Retry send command: {device.name} -> {device.connection_status}')
        await device.connect(_callback=connected)


async def dis(device: BledomDevice):
    await device.connect(_callback=connected)


async def founded(devices: [BledomDevice], index: int):
    logger.debug(f'Founded {devices[index].name}')
    await devices[index].terminate_connection(_callback=dis)


async def main():
    controller = BleController()
    await controller.update_devices(_callback=founded)


if __name__ == '__main__':
    asyncio.run(main())
