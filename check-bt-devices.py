#!/data/data/com.termux/files/usr/bin/env python
# -*- coding: utf-8 -*-

from able import BluetoothDispatcher, GATT_SUCCESS

class BLE(BluetoothDispatcher):

    def on_connection_state_change(self, status, state):
        Logger.info("on_connection_state_change: status=%s, state=%s", status, state)
        if status == GATT_SUCCESS and state:
            Logger.info("Connection: succeed")

    def on_services(self, status, services):
        Logger.info("on_services: status=%s", status)
        if status == GATT_SUCCESS:
            Logger.info("services discovered: %s", list(services.keys()))
            # save discovered services object
            self.services = services

    def on_characteristic_read(self, characteristic, status):
        Logger.info("on_characteristic_read: status=%s, characteristic=%s", status,
                    characteristic.getUuid().toString())
        if status == GATT_SUCCESS:
            Logger.info("Characteristic read: succeed")

ble = BLE()

for device in ble.bonded_devices:
    # device: https://developer.android.com/reference/android/bluetooth/BluetoothDevice
    print(type(device), device.getName(), "address:", device.getAddress())
