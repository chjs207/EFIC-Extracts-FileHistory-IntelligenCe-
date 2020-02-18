# -*- coding: utf-8 -*-
"""Parser for the Microsoft File History ESE database."""

from __future__ import unicode_literals

from dfdatetime import filetime as dfdatetime_filetime
from dfdatetime import semantic_time as dfdatetime_semantic_time
from dfdatetime import java_time as dfdatetime_java_time

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import definitions
from plaso.parsers import esedb
from plaso.parsers.esedb_plugins import interface


class FileHistoryNamespaceEventData(events.EventData):
  """File history namespace table event data.

  Attributes:
    file_attribute (int): file attribute.
    identifier (str): identifier.
    original_filename (str): original file name.
    parent_identifier (str): parent identifier.
    usn_number (int): USN number.
  """

  DATA_TYPE = 'filehistory:namespace:event'

  def __init__(self):
    """Initializes event data."""
    super(FileHistoryNamespaceEventData, self).__init__(
        data_type=self.DATA_TYPE)
    self.backuped_date = None #tCreated
    self.file_attribute = None
    self.file_size = None
    self.full_filepath = None #parent folder path + original filename
    self.usn_number = None
    self.created_timestamp = None
    self.modified_timestamp = None
    self.file_recordid = None

class FileHistoryGlobalEventData(events.EventData):
  """File History global table event data.

  Attributes:
      first_backup_timestamp (str):
      last_backup_timestamp (str):
  """
  DATA_TYPE = 'filehistory:global:event'

  def __init__(self):
    """Initializes event data."""
    super(FileHistoryGlobalEventData, self).__init__(
      data_type=self.DATA_TYPE)
    self.first_backup_timestamp = None
    self.last_backup_timestamp = None

class FileHistoryLibraryEventData(events.EventData):
  """File History library table event data.

  Attributes:
      backup_folder (str):
  """
  DATA_TYPE = 'filehistory:library:event'

  def __init__(self):
    """Initializes event data."""
    super(FileHistoryLibraryEventData, self).__init__(
      data_type=self.DATA_TYPE)
    self.backup_folder = None

class FileHistoryCatalogedbParser(interface.ESEDBPlugin):
  """Parses a File History ESE database file."""

  NAME = 'filehistory_catalogedb'
  DESCRIPTION = 'Parser for File History ESE database files.'

  # TODO: Add support for other tables as well, backupset, file, library, etc.
  REQUIRED_TABLES = {
      'backupset': '',
      'file': '',
      'namespace': 'ParseNameSpace',
      'library': 'ParseLibrary',
      'global': 'ParseGlobal'}

  def _GetDictFromFileTable(self, parser_mediator, table):
    """Build a dictionary of the value in the file table.

    Args:
      parser_mediator (ParserMediator):
      table (pyesedb.table): file table.

    Returns:

    """
    if not table:
      return {}

    record_values = {}
    for record in table.records:
      if parser_mediator.abort:
        break

      if record.get_number_of_values() != 9:
        continue
      id = self._GetRecordValue(record, 0)
      parentId = self._GetRecordValue(record, 1)
      #childId = self._GetRecordValue(record, 2)
      fileSize = self._GetRecordValue(record, 5)

      if not id:
        continue
      record_values[id] = [fileSize, parentId]

    return record_values

  def _GetDictFromBackupsetTable(self, parser_mediator, table):
    """Build a dictionary of the value in the backupset table.

    Args:
      parser_mediator (ParserMediator):
      table (pyesedb.table): backupset table.

    Returns:

    """
    if not table:
      return {}

    record_values = {}
    for record in table.records:
      if parser_mediator.abort:
        break

      if record.get_number_of_values() != 2:
        continue

      identification = self._GetRecordValue(record, 0)
      timestamp = self._GetRecordValue(record, 1)

      if not identification:
        continue
      record_values[identification] = timestamp

    return record_values

  def _GetDictFromStringsTable(self, parser_mediator, table):
    """Build a dictionary of the value in the strings table.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfvfs.
      table (pyesedb.table): strings table.

    Returns:
      dict[str,object]: values per column name.
    """
    if not table:
      return {}

    record_values = {}
    for record in table.records:
      if parser_mediator.abort:
        break

      if record.get_number_of_values() != 2:
        continue

      identification = self._GetRecordValue(record, 0)
      filename = self._GetRecordValue(record, 1)

      if not identification:
        continue
      record_values[identification] = filename

    return record_values

  def ParseNameSpace(
      self, parser_mediator, cache=None, database=None, table=None,
      **unused_kwargs):
    """Parses the namespace table.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfvfs.
      cache (Optional[ESEDBCache]): cache.
      database (Optional[pyesedb.file]): ESE database.
      table (Optional[pyesedb.table]): table.

    Raises:
      ValueError: if the database or table value is missing.
    """
    if database is None:
      raise ValueError('Missing database value.')

    if table is None:
      raise ValueError('Missing table value.')

    strings = cache.GetResults('strings')
    if not strings:
      esedb_table = database.get_table_by_name('string')
      strings = self._GetDictFromStringsTable(parser_mediator, esedb_table)
      cache.StoreDictInCache('strings', strings)

    backupsets = cache.GetResults('backupsets')
    if not backupsets:
      esedb_table = database.get_table_by_name('backupset')
      backupsets = self._GetDictFromBackupsetTable(parser_mediator, esedb_table)
      cache.StoreDictInCache('backupsets', backupsets)

    files = cache.GetResults('files')
    if not files:
      esedb_table = database.get_table_by_name('file')
      files = self._GetDictFromFileTable(parser_mediator, esedb_table)
      cache.StoreDictInCache('files', files)

    for esedb_record in table.records:
      if parser_mediator.abort:
        break

      record_values = self._GetRecordValues(
          parser_mediator, table.name, esedb_record)

      event_data = FileHistoryNamespaceEventData()
      backuped_id = record_values.get('tCreated')
      filerecordid = record_values.get('fileRecordId')
      childid = record_values.get('childId')

      if filerecordid != 0:
        parent_identifier = files.get(filerecordid)[1]
      else:
        parent_identifier = record_values.get('parentId')

      backuped_date = backupsets.get(backuped_id)
      event_data.file_attribute = record_values.get('fileAttrib')
      if filerecordid != 0:
        event_data.file_size = files.get(filerecordid)[0]
      else:
        event_data.file_size = 'Unknown'

      event_data.usn_number = record_values.get('usn')

      event_data.full_filepath = strings.get(parent_identifier) + "\\" + strings.get(childid)
      event_data.file_recordid = record_values.get('fileRecordId')
      created_timestamp = record_values.get('fileCreated')
      modified_timestamp = record_values.get('fileModified')

      if backuped_date:
        backuped_date_time = dfdatetime_filetime.Filetime(timestamp=backuped_date)
        created_date_time = dfdatetime_filetime.Filetime(timestamp=created_timestamp)
        modified_date_time = dfdatetime_filetime.Filetime(timestamp=modified_timestamp)
        event_data.backuped_date_timestamp = backuped_date_time.CopyToDateTimeString()
        event_data.created_timestamp = created_date_time.CopyToDateTimeString()
        event_data.modified_timestamp = modified_date_time.CopyToDateTimeString()
        event = time_events.DateTimeValuesEvent(
            backuped_date_time, definitions.TIME_DESCRIPTION_BACKUP)

      parser_mediator.ProduceEventWithEventData(event, event_data)

  def _GetDictFromGlobalTable(self, parser_mediator, table):
    """Build a dictionary of the value in the global table.
    Args:
        parser_mediator (ParserMediator):
        table (pyesedb.table): global table.
    Returns:
    """
    if not table:
      return {}

    record_values = {}
    for record in table.records:
      if parser_mediator.abort:
        break

      if record.get_number_of_values() != 3:
        continue
      identification = self._GetRecordValue(record, 0)
      key = self._GetRecordValue(record, 1)
      value = self._GetRecordValue(record, 2)

      if not key:
        continue
      record_values[key] = value

    return record_values

  def ParseGlobal(
          self, parser_mediator, cache=None, database=None, table=None,
          **unused_kwargs):
    """Parses the global table.
    Args:
    """
    if database is None:
      raise ValueError('Missing database value.')

    if table is None:
      raise ValueError('Missing table value.')

    globals = cache.GetResults('globals')
    if not globals:
      esedb_table = database.get_table_by_name('global')
      globals = self._GetDictFromGlobalTable(parser_mediator, esedb_table)
      cache.StoreDictInCache('globals', globals)

    event_data = FileHistoryGlobalEventData()
    temp_first_backup = globals.get('FirstBackupTime')[::-1].hex()
    first_backup_timestamp = int(temp_first_backup, 16)
    temp_last_backup = globals.get('LastBackupTime')[::-1].hex()
    last_backup_timestamp = int(temp_last_backup, 16)

    first_backup_datetime = dfdatetime_filetime.Filetime(timestamp=first_backup_timestamp)
    event_data.first_backup_timestamp = first_backup_datetime.CopyToDateTimeString()

    last_backup_datetime = dfdatetime_filetime.Filetime(timestamp=last_backup_timestamp)
    event_data.last_backup_timestamp = last_backup_datetime.CopyToDateTimeString()

    if first_backup_datetime:
      event = time_events.DateTimeValuesEvent(
        first_backup_datetime, definitions.TIME_DESCRIPTION_BACKUP)
      parser_mediator.ProduceEventWithEventData(event, event_data)

    if last_backup_datetime:
      event = time_events.DateTimeValuesEvent(
        last_backup_datetime, definitions.TIME_DESCRIPTION_BACKUP)
      parser_mediator.ProduceEventWithEventData(event, event_data)

    if not first_backup_datetime and not last_backup_datetime:
      date_time = dfdatetime_semantic_time.SemanticTime('Not set')
      event = time_events.DateTimeValuesEvent(
        date_time, definitions.TIME_DESCRIPTION_NOT_A_TIME)
      parser_mediator.ProduceEventWithEventData(event, event_data)

  def ParseLibrary(
          self, parser_mediator, cache=None, database=None, table=None,
          **unused_kwargs):
    """Parses the library table.
    Args:
    """
    if database is None:
      raise ValueError('Missing database value.')

    if table is None:
      raise ValueError('Missing table value.')

    strings = cache.GetResults('strings')
    if not strings:
      esedb_table = database.get_table_by_name('string')
      strings = self._GetDictFromStringsTable(parser_mediator, esedb_table)
      cache.StoreDictInCache('string', strings)

    backup_folder_list = ""

    event_data = FileHistoryLibraryEventData()
    for esedb_record in table.records:
      if parser_mediator.abort:
        break

      record_values = self._GetRecordValues(
        parser_mediator, table.name, esedb_record)

      parentid = record_values.get('parentId')
      childid = record_values.get('childId')
      backup_folder_list += str(strings.get(parentid)) + "\\" \
                            + str(strings.get(childid)) + ","

    event_data.backup_folder = backup_folder_list
    date_time = dfdatetime_java_time.JavaTime(timestamp=0)
    event = time_events.DateTimeValuesEvent(
      date_time, definitions.TIME_DESCRIPTION_NOT_A_TIME)
    parser_mediator.ProduceEventWithEventData(event, event_data)

esedb.ESEDBParser.RegisterPlugin(FileHistoryCatalogedbParser)