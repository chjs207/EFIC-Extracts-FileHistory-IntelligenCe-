# -*- coding: utf-8 -*-
"""The GPT Entry formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class GPTEntryFormatter(interface.ConditionalEventFormatter):
    """Formatter for a GPT Entry parsing result."""

    DATA_TYPE = 'storage:gpt:event'

    FORMAT_STRING_PIECES = [
        'GPT Entry DriveSignature:{drive_signature}']

    SOURCE_LONG = 'GPT Entry DriveSignature'
    SOURCE_SHORT = 'GPT'


manager.FormattersManager.RegisterFormatter(GPTEntryFormatter)