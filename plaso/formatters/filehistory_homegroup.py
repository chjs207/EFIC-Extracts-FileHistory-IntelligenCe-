# -*- coding: utf-8 -*-
"""The UserAssist Windows Registry event formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class FileHistoryHomegroupWindowsRegistryEventFormatter(
    interface.ConditionalEventFormatter):
    """Formatter for a FileHistory Homegroup Windows Registry event."""

    DATA_TYPE = 'windows:registry:filehistory_homegroup'

    FORMAT_STRING_PIECES = [
        '[{key_path}]',
        'User type:{user_type}',
        'Folder Path:{folder_path}',
        'Friendly name:{friendly_name}',
        'Share name:{share_name}',
        'Share point:{url}'
    ]

    SOURCE_LONG = 'Registry Key: FileHistory_Homegroup'
    SOURCE_SHORT = 'REG'


manager.FormattersManager.RegisterFormatter(
    FileHistoryHomegroupWindowsRegistryEventFormatter)