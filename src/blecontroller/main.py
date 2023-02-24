#!@PYTHON@

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

from __future__ import annotations

from bleak import BleakScanner, BleakClient, BLEDevice
from typing import Callable, Awaitable
from ..bledom import BleLedDevice
from bleak.exc import BleakError

import logging
import sys

logger = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)

DEVICE_NAMES_KEY = 'ELK'


class BledomDevice:

    def __init__(self, device: BLEDevice, group: str = None, last_connect: int = -1,
                 auto_connect: bool = False, connection_status: bool = False):

        self.name = device.name
        self.address = device.address
        self.device = device
        self.group = group
        self.last_connect = last_connect
        self.auto_connect = auto_connect,
        self.connection_status = connection_status
        self.led_control: BleLedDevice = None

        self.is_power_on = False

    # def __await__(self):
    #
    #     self.led_control = None
    #
    #     if self.auto_connect:
    #         await self.connect()

    async def __set_led_client(self, client):
        self.led_control = await BleLedDevice.new(client)

    def __unset_led_client(self):
        self.led_control = None

    async def connect(self, _callback: Callable[[BledomDevice], Awaitable[None]] = None):
        if self.connection_status:
            logger.warning(f'Already connected device {self.name}')

        async with BleakClient(self.device) as client:
            if client.is_connected:
                await self.__set_led_client(client)
            else:
                try:
                    await client.connect()
                    await self.__set_led_client(client)
                except Exception as e:
                    logger.error(f'Connecting error -> {e}')

            self.connection_status = client.is_connected

            # NOTE
            if _callback:
                await _callback(self)

    async def terminate_connection(self, _callback: Callable[[BledomDevice], Awaitable[None]] = None):
        if self.connection_status:
            logger.warning(f'Already disconnected device {self.name}')

        else:
            async with BleakClient(self.device) as client:
                if client.is_connected:
                    try:
                        await client.disconnect()
                        self.__unset_led_client()
                        self.connection_status = False
                    except Exception as e:
                        logger.error(f'Disconnecting error -> {e}')
                        self.connection_status = client.is_connected
                else:
                    self.connection_status = False
                    self.__unset_led_client()

        if _callback:
            await _callback(self)


class BleController:
    """
    Bledom devices control class.
    Use it for creating and control connections between PC and bledom.
    """

    def __init__(self):
        self.devices: [BledomDevice] = []
        self.groups: [str] = ['default']
        self.current_group = None

        logger.debug('Init ble controller...')

    async def update_devices(self, _callback: Callable[[[BledomDevice], int], Awaitable[None]] = None):
        """
        Align for *get_devices* function
        :param _callback: callback function. The function will be called after finding each device (args: BledomDevice)
        :return: None
        """
        logger.debug('Update devices request...')
        await self.get_devices(_callback=_callback)

    async def get_devices(self, _callback: Callable[[[BledomDevice], int], Awaitable[None]] = None):
        """
        Getting devices func.
        :param _callback: callback function. The function will be called after finding each device (args: BledomDevice)
        :return: None
        """

        try:

            for device in await BleakScanner.discover():
                logger.debug(f'Found device {device.name}')

                if DEVICE_NAMES_KEY in device.name:

                    if self.__check_exist(address=device.address):
                        logger.debug(f'Elk device {device.name} already exists')
                        continue

                    logger.debug(f'Found elk device {device.name}')

                    new_device = BledomDevice(device=device, group=self.groups[0])
                    self.devices.append(new_device)

                    # NOTE: it's important to be there (in with case)
                    if _callback:
                        await _callback(self.devices, len(self.devices) - 1)

        except BleakError as e:
            logger.error(e)

    def __check_exist(self, address: str) -> bool:
        """
        Check is device exists by address
        :param address: address of new device
        :return: True - already exists in devices list
        """
        return address in map(lambda device: device.address, self.devices)
