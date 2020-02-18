# -*- coding: utf-8 -*-
"""The MountedDeivces Windows Registry event formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class MountedDevicesWindowsRegistryEventFormatter(
    interface.ConditionalEventFormatter):
    """Formatter for a MountedDevices Windows Registry event."""

    DATA_TYPE = 'windows:registry:mounteddevices'

    FORMAT_STRING_PIECES = [
        '[{key_path}]',
        'Drive Letter: {drive_letter}',
        'Disk Signature: {drive_signature}',
        'Raw Data: {raw_data}'
    ]

    SOURCE_LONG = 'Registry Key: MountedDeivces'
    SOURCE_SHORT = 'REG'


manager.FormattersManager.RegisterFormatter(
    MountedDevicesWindowsRegistryEventFormatter)