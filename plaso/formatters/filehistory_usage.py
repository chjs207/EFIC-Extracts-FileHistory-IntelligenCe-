# -*- coding: utf-8 -*-
"""The FileHistory Usage Windows Registry event formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class FileHistoryUsageWindowsRegistryEventFormatter(
    interface.ConditionalEventFormatter):
    """Formatter for a FileHistory Usage Windows Registry event."""

    DATA_TYPE = 'windows:registry:filehistory_usage'

    FORMAT_STRING_PIECES = [
        '[{key_path}]',
        'Last Backup Time:{last_backup_time}',
        'Backup Storage Changed:{target_changed}'
    ]

    SOURCE_LONG = 'Registry Key:FileHistoryUsage'
    SOURCE_SHORT = 'REG'


manager.FormattersManager.RegisterFormatter(
    FileHistoryUsageWindowsRegistryEventFormatter)
