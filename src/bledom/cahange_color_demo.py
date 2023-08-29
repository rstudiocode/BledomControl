
#Demo code to help users


import asyncio
from bledom.device import BleLedDevice
from bleak import BleakScanner, BleakClient


#a first method that scans all bleutooth devices and finds elk bledom device by name . SLOW
async def change_color_scan(r, g, b):
    a= await BleakScanner.discover(timeout=5.0)
    for device in a:
        name=str(device.name)
        address=str(device.address)
        if name=="ELK-BLEDOM":
            client = BleakClient(device)
            await client.connect()
            device = await BleLedDevice.new(client)
            print("connected to", address)
            await device.power_on()
            r,b,g =int(r), int(b), int(g)
            """
            Note : On some bledom controlers,
            blue and green lights are stronger than red so you might add the commented line above to your code """
            #g,b=int(g/2), int(b/2)
            await device.set_color(a,b,c)
            print(done)
asyncio.run(change(r=254, g=254, b=254 , mac=mac_address))


#change color by connecting to bledom via its mac adress FASTER
mac_address="**:**:**:**:**:**"
async def change_color_mac(r, g, b, mac):
    #a= await BleakScanner.discover(timeout=10.0)
    client = BleakClient(mac)
    await client.connect()
    device = await BleLedDevice.new(client)
    await device.power_on()
    r,b,g =int(r), int(b), int(g)
    """
    Note : On some bledom controlers,
    blue and green lights are stronger than red so you might add the commented line above to your code """
    #g,b=int(g/2), int(b/2)
    await device.set_color(a,b,c)
asyncio.run(change(r=254, g=254, b=254 , mac=mac_address))



