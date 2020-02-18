# -*- coding: utf-8 -*-
"""Parser for the GPT file."""

from __future__ import unicode_literals

from dfdatetime import posix_time as dfdatetime_posix_time

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import errors
from plaso.lib import definitions
from plaso.parsers import interface
from plaso.parsers import manager

class GPTEventData(events.EventData):
    """GPT event data.

    Attributes:
        drive_signature (str):
    """
    DATA_TYPE = 'storage:gpt:event'

    def __init__(self):
        """Initialize event data"""
        super(GPTEventData, self).__init__(data_type=self.DATA_TYPE)
        self.drive_signature = None


class GPTParser(interface.FileObjectParser):
    """Parses GPT file-like object"""

    NAME = 'gpt_entry'
    DESCRIPTION = 'Parsers for gpt dump files'

    def _convert_guid(self, bytearray):
        first_part = reversed(bytearray[0:4])
        second_part = reversed(bytearray[4:6])
        third_part = reversed(bytearray[6:8])
        fourth_part = bytearray[8:10]
        fifth_part = bytearray[10:16]

        guid = ''.join('{:02x}'.format(byte) for byte in first_part) + "-" \
               + ''.join('{:02x}'.format(byte) for byte in second_part) + "-" \
               + ''.join('{:02x}'.format(byte) for byte in third_part) + "-" \
               + ''.join('{:02x}'.format(byte) for byte in fourth_part) + "-" \
               + ''.join('{:02x}'.format(byte) for byte in fifth_part)

        return guid

    def _check_entry(self, entry_signature):
        if entry_signature.upper() == 'E3C9E316-0B5C-4DB8-817D-F92DF00215AE' or \
           entry_signature.upper() == 'EBD0A0A2-B9E5-4433-87C0-68B6B72699C7' or \
           entry_signature.upper() == '5808C8AA-7E8F-42E0-85D2-E1E90434CFB3' or \
           entry_signature.upper() == 'AF9B60A0-1431-4F62-BC68-3311714A69AD' or \
           entry_signature.upper() == 'DE94BBA4-06D1-4D40-A16A-BFD50179D6AC' or \
           entry_signature.upper() == '37AFFC90-EF7D-4E96-91C3-2D7AE055B174' or \
           entry_signature.upper() == 'DB97DBA9-0840-4BAE-97F0-FFB9A327C7E1':
            return True
        else:
            return False

    def ParseFileObject(self, parser_mediator, file_object):
        """Parses a GPT file-like object.

        Args:
            Parser_mediator (ParserMediator): mediates interactions between parsers
            and other components, such as storage and dfvfs.
            file_object ():

        Raises:
            ParseError: when the file_object is not GPT.
        """
        event_data = GPTEventData()

        try:
            read_file = file_object.read()
            file_size = len(read_file)
            if file_size < 128:
                errors.UnableToParseFile('Not a GPT file')
                return

            entry_signature = self._convert_guid(bytearray(read_file[0:16]))

            if not self._check_entry(entry_signature):
                errors.UnableToParseFile('Not a GPT file')
                return

            if (file_size % 128) != 0:
                return
            entry_data = bytearray(read_file)

            index_number = int(file_size/128)
            for index in range(index_number):
                current_entry = entry_data[index*128:128+index*128]
                current_entry_guid = self._convert_guid(current_entry)
                if not self._check_entry(current_entry_guid):
                    continue
                event_data.drive_signature = '{'+self._convert_guid(current_entry[16:32])+'}'
                date_time = dfdatetime_posix_time.PosixTime(timestamp=0)
                event = time_events.DateTimeValuesEvent(date_time, definitions.TIME_DESCRIPTION_NOT_A_TIME)
                parser_mediator.ProduceEventWithEventData(event, event_data)

        except:
            errors.UnableToParseFile('Not a GPT file')
            return


manager.ParsersManager.RegisterParser(GPTParser)