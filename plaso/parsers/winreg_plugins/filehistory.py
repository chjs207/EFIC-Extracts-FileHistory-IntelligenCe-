# -*- coding: utf-8 -*-
"""File containing a Windows Registry plugin to parse the FileHistory."""

from __future__ import unicode_literals

from dfdatetime import filetime as dfdatetime_filetime

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import definitions
from plaso.lib import errors
from plaso.parsers import winreg
from plaso.parsers.winreg_plugins import interface


class WindowsFileHistoryHomegroupEventData(events.EventData):
    """Windows Registry of FileHistory Homegroup event data attribute container.

    Attributes:
        key_path (str): Windows Registry key path.
        user_type (str): user_type of FileHistory homegroup storage in DeviceType value
        folder_path (str): drive_letter of FileHistory homegroup storage
        friendly_name (str): friendly_name of FileHistory homegroup storage
        share_name (str): share_name of FileHistory homegroup storage
        url (str): url of FileHistory homegroup storage
    """

    DATA_TYPE = 'windows:registry:filehistory_homegroup'

    def __init__(self):
        """Initialize event data."""
        super(WindowsFileHistoryHomegroupEventData, self).__init__(data_type=self.DATA_TYPE)
        self.key_path = None
        self.user_type = None
        self.folder_path = None
        self.friendly_name = None
        self.share_name = None
        self.url = None


class WindowsFileHistoryUsageEventData(events.EventData):
    """Windows Registry of FileHistory Usage event data attribute container.

    Attributes:
        key_path (str): Windows Registry key path.
        last_backup_time (str): last_backup_date of FileHistory
        target_changed (str): target_changed of FileHistory Storage
    """

    DATA_TYPE = 'windows:registry:filehistory_usage'

    def __init__(self):
        """Initialize event data."""
        super(WindowsFileHistoryUsageEventData, self).__init__(data_type=self.DATA_TYPE)
        self.key_path = None
        self.last_backup_time = None
        self.target_changed = None


class FileHistoryHomegroupPlugin(interface.WindowsRegistryPlugin):
    """Windows registry plugin for FileHistory
    """

    NAME = 'windows_filehistory_homegroup'
    DESCRIPTION = 'Parser for FileHistory Homegroup Registry entries.'

    FILTERS = frozenset([interface.WindowsRegistryKeyPathFilter(
        'HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\'
        'CurrentVersion\\FileHistory\\HomeGroup\\Target')])

    def ExtractEvents(self, parser_mediator, registry_key, **kwargs):
        """Extracts events from a Windows Registry key.

        Args:
            parser_mediator (ParserMediator): mediates interactions between parsers
            and other components, such as storage and dfvfs.
            registry_key (dfwinreg.WinRegistryKey): Windows Registry key.
        """
        event_data = WindowsFileHistoryHomegroupEventData()
        event_data.key_path = registry_key.path

        for values in registry_key.GetValues():
            try:
                name = values.name
                if 'DeviceType' in name:
                    data = values.GetDataAsObject()
                    device_type = int(data)
                    if device_type == 1:
                        event_data.user_type = 'Homegroup Participant'
                    elif device_type == 2:
                        event_data.user_type = 'Homegroup Owner'
                    else:
                        event_data.user_type = 'Unknown'
                    continue
                elif 'FolderPath' in name:
                    data = values.GetDataAsObject()
                    event_data.folder_path = str(data)
                    continue
                elif 'FriendlyName' in name:
                    data = values.GetDataAsObject()
                    event_data.friendly_name = str(data)
                    continue
                elif 'ShareName' in name:
                    data = values.GetDataAsObject()
                    event_data.share_name = str(data)
                    continue
                elif 'Url' in name:
                    data = values.GetDataAsObject()
                    event_data.url = str(data)
                    continue
                else:
                    continue
            except:
                errors.UnableToParseFile(
                    'Unable to parse SOFTWARE Hivefile for FileHistory homegroup')
                return
        event = time_events.DateTimeValuesEvent(
            registry_key.last_written_time, definitions.TIME_DESCRIPTION_CONNECTION_ESTABLISHED)
        parser_mediator.ProduceEventWithEventData(event, event_data)

class FileHistoryUsagePlugin(interface.WindowsRegistryPlugin):
    """Windows Registry plugin for FileHistory usage.
    """

    NAME = 'windows_filehistory_usage'
    DESCRIPTION = 'Parser for FileHistory Usage Registry entries.'

    FILTERS = frozenset([
        interface.WindowsRegistryKeyPathFilter(
            'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\FileHistory')])

    def ExtractEvents(self, parser_mediator, registry_key, **kwargs):
        """Extract events from a Windows Registry key.

        Args:
            parser_mediator (ParserMediator): mediates interactions between parsers
            and other components, such as storage and dfvfs.
            registry_key (dfwinreg.WinRegistryKey): Windows Registry key.
        """
        event_data = WindowsFileHistoryUsageEventData()
        event_data.key_path = registry_key.path

        for values in registry_key.GetValues():
            try:
                name = values.name
                date_time = None
                if 'ProtectedUpToTime' in name:
                    last_backup_time = int(values.GetDataAsObject())
                    date_time = dfdatetime_filetime.Filetime(timestamp=last_backup_time)
                    event_data.last_backup_time = date_time.CopyToDateTimeString()
                    continue
                elif 'TargetChanged' in name:
                    target_changed = int(values.GetDataAsObject())
                    if target_changed == 0:
                        event_data.target_changed = 'Not Backup storage changed'
                        continue
                    else:
                        event_data.target_changed = 'Backup storage changed'
                        continue
                else:
                    continue
            except:
                errors.UnableToParseFile(
                    'Unable to parse NTUSER Hive for FileHistory usage')
                return
        event = time_events.DateTimeValuesEvent(
            date_time, definitions.TIME_DESCRIPTION_BACKUP)
        parser_mediator.ProduceEventWithEventData(event, event_data)


winreg.WinRegistryParser.RegisterPlugins([FileHistoryHomegroupPlugin, FileHistoryUsagePlugin])