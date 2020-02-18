# -*- coding: utf-8 -*-
"""File containing a Windows Registry plugin to parse the USB Device key."""

from __future__ import unicode_literals

from dfdatetime import semantic_time as dfdatetime_semantic_time

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import definitions
from plaso.parsers import logger
from plaso.parsers import winreg
from plaso.parsers.winreg_plugins import interface


class WindowsMountedDevicesEventData(events.EventData):
    """Windows MountedDevices event data attribute container.

    Attributes:
         key_path (str): Windows Registry key path.
         drive_letter (str): drive_letter of the Mounted device.
         drive_signature (str): drive_signature of the Mounted device.
         raw_data (str): raw data of the Mounted device.
    """

    DATA_TYPE = 'windows:registry:mounteddevices'

    def __init__(self):
        """Initialize event data."""
        super(WindowsMountedDevicesEventData, self).__init__(data_type=self.DATA_TYPE)
        self.key_path = None
        self.drive_letter = None
        self.drive_signature = None
        self.raw_data = None


class MountedDevicePlugin(interface.WindowsRegistryPlugin):
    """Windows registry plugin for mounted device
    """

    NAME = 'windows_mounted_devices'
    DESCRIPTION = 'Parser for Mounted device Registry entries.'

    FILTERS = frozenset([
        interface.WindowsRegistryKeyPathFilter(
            'HKEY_LOCAL_MACHINE\\System\\MountedDevices')])

    def ExtractEvents(self, parser_mediator, registry_key, **kwargs):
        """Extracts events from a Windows Registry key.

        Args:
            parser_mediator (ParserMediator): mediates interactions between parsers
            and other components, such as storage and dfvfs.
            registry_key (dfwinreg.WinRegistryKey): Windows Registry key.
        """
        event_data = WindowsMountedDevicesEventData()
        event_data.key_path = registry_key.path

        for values in registry_key.GetValues():
            try:
                if values.DataIsBinaryData():
                    data = values.GetDataAsObject()
                    name = values.name
                    if '\\DosDevices\\' in name:
                        if len(data) == 12:
                            device = bytearray(data[0:4])
                            event_data.drive_signature = "{"+''.join('{:02x}'.format(byte) for byte in device)+"}"
                            event_data.drive_letter = name.replace('\\DosDevices\\', '')
                            event_data.raw_data = data
                        else:
                            if str(data).find('DMIO'):
                                device = bytearray(data[8:24])
                                tmp1 = reversed(device[0:4])
                                tmp2 = reversed(device[4:6])
                                tmp3 = reversed(device[6:8])
                                tmp4 = device[8:10]
                                tmp5 = device[10:16]
                                event_data.drive_signature = "{"+\
                                                 ''.join('{:02x}'.format(byte) for byte in tmp1)+\
                                                 "-"+''.join('{:02x}'.format(byte) for byte in tmp2)+\
                                                 "-"+''.join('{:02x}'.format(byte) for byte in tmp3)+\
                                                 "-"+''.join('{:02x}'.format(byte) for byte in tmp4)+\
                                                 "-"+''.join('{:02x}'.format(byte) for byte in tmp5)+\
                                                 "}"
                                event_data.drive_letter = name.replace('\\DosDevices\\', '')
                                event_data.raw_data = data
                            else:
                                event_data.drive_signature = 'Unknown'
                                event_data.drive_letter = name.replace('\\DosDevices\\', '')
                                event_data.raw_data = str(data)
                    elif '\\??\\Volume' in name:
                        event_data.drive_letter = 'Unknown'
                        event_data.drive_signature = name.replace('\\??\\Volume', '')
                        event_data.raw_data = str(data)
                    elif '#' in name:
                        event_data.drive_letter = 'Unknown'
                        event_data.drive_signature = name.replace('#', '')
                        event_data.raw_data = str(data)
                    else:
                        event_data.drive_letter = 'Unknown'
                        event_data.drive_signature = 'Unknown'
                        event_data.raw_data = str(data)
                else:
                    continue

                date_time = dfdatetime_semantic_time.SemanticTime('Not set')
                event = time_events.DateTimeValuesEvent(
                    date_time, definitions.TIME_DESCRIPTION_NOT_A_TIME)
                parser_mediator.ProduceEventWithEventData(event, event_data)
            except:
                return


winreg.WinRegistryParser.RegisterPlugin(MountedDevicePlugin)
