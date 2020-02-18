# -*- coding: utf-8 -*-
"""The MBR drive_signature formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class MBRFormatter(interface.ConditionalEventFormatter):
    """Formatter for a MBR parsing result."""

    DATA_TYPE = 'storage:mbr:event'

    FORMAT_STRING_PIECES = [
        'MBR DriveSignature:{drive_signature}']

    SOURCE_LONG = 'MBR DriveSignature'
    SOURCE_SHORT = 'MBR'


manager.FormattersManager.RegisterFormatter(MBRFormatter)