# -*- coding: utf-8 -*-
"""Parser for the MBR file."""

from __future__ import unicode_literals

from dfdatetime import posix_time as dfdatetime_posix_time

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import errors
from plaso.lib import definitions
from plaso.parsers import interface
from plaso.parsers import manager


class MBREventData(events.EventData):
    """MBR event data.

    Attributes:
        drive_signature (str):
    """
    DATA_TYPE = 'storage:mbr:event'

    def __init__(self):
        """Initialize event data"""
        super(MBREventData, self).__init__(data_type=self.DATA_TYPE)
        self.drive_signature = None

class MBRParser(interface.FileObjectParser):
    """Parses MBR file-like object"""

    NAME = 'mbr'
    DESCRIPTION = 'Parsers for mbr dump files'

    def ParseFileObject(self, parser_mediator, file_object):
        """Parses a MBR file-like object.

        Args:
            parser_mediator (ParseMediator): mediates interactions between parsers
            and other components, such as storage and dfvfs.
            file_object():

        Raises:
            ParseError: when the file_object is not MBR.
        """
        event_data = MBREventData()

        try:
            read_file = file_object.read()

            if len(read_file) != 512:
                errors.UnableToParseFile('Not a MBR file')
                return

            if read_file[510] != 85 or read_file[511] != 170:
                errors.UnableToParseFile('Not a MBR file')
                return

            event_data.drive_signature = format(read_file[440], 'x') \
                                         + format(read_file[441], 'x') \
                                         + format(read_file[442], 'x') \
                                         + format(read_file[443], 'x')
        except:
            errors.UnableToParseFile('Not a MBR file')
        date_time = dfdatetime_posix_time.PosixTime(timestamp=0)
        event = time_events.DateTimeValuesEvent(date_time, definitions.TIME_DESCRIPTION_NOT_A_TIME)
        parser_mediator.ProduceEventWithEventData(event, event_data)


manager.ParsersManager.RegisterParser(MBRParser)