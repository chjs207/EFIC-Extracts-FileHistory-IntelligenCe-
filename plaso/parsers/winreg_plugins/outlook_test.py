#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2013 The Plaso Project Authors.
# Please see the AUTHORS file for details on individual authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for the Outlook Windows Registry plugins."""

import unittest

# pylint: disable=unused-import
from plaso.formatters import winreg as winreg_formatter
from plaso.parsers.winreg_plugins import outlook
from plaso.parsers.winreg_plugins import test_lib
from plaso.winreg import test_lib as winreg_test_lib


class MSOutlook2013SearchMRUPluginTest(test_lib.RegistryPluginTestCase):
  """Tests for the Outlook Search MRU Windows Registry plugin."""

  def setUp(self):
    """Sets up the needed objects used throughout the test."""
    self._plugin = outlook.OutlookSearchMRUPlugin()

  def testProcess(self):
    """Tests the Process function."""
    key_path = u'\\Software\\Microsoft\\Office\\15.0\\Outlook\\Search'
    values = []

    values.append(winreg_test_lib.TestRegValue(
        ('C:\\Users\\username\\AppData\\Local\\Microsoft\\Outlook\\'
         'username@example.com.ost'), '\xcf\x2b\x37\x00',
        winreg_test_lib.TestRegValue.REG_DWORD, offset=1892))

    winreg_key = winreg_test_lib.TestRegKey(
        key_path, 1346145829002031, values, 1456)

    event_queue_consumer = self._ParseKeyWithPlugin(self._plugin, winreg_key)
    event_objects = self._GetEventObjectsFromQueue(event_queue_consumer)

    expected_msg = (
        u'[{0:s}] '
        u'C:\\Users\\username\\AppData\\Local\\Microsoft\\Outlook\\'
        u'username@example.com.ost: 0x00372bcf').format(key_path)

    expected_msg_short = u'[{0:s}] C:\\Users\\username\\AppData\\Lo...'.format(
        key_path)

    self.assertEquals(len(event_objects), 1)

    event_object = event_objects[0]

    # This should just be the plugin name, as we're invoking it directly,
    # and not through the parser.
    self.assertEquals(event_object.parser, self._plugin.plugin_name)

    self.assertEquals(event_object.timestamp, 1346145829002031)

    self._TestGetMessageStrings(event_object, expected_msg, expected_msg_short)


# TODO: The catalog for Office 2013 (15.0) contains binary values not
# dword values. Check if Office 2007 and 2010 have the same. Re-enable the
# plug-ins once confirmed and OutlookSearchMRUPlugin has been extended to
# handle the binary data or create a OutlookSearchCatalogMRUPlugin.

# class MSOutlook2013SearchCatalogMRUPluginTest(unittest.TestCase):
#   """Tests for the Outlook Search Catalog MRU Windows Registry plugin."""
#
#   def setUp(self):
#     """Sets up the needed objects used throughout the test."""
#     self._plugin = outlook.MSOutlook2013SearchCatalogMRUPlugin()
#
#   def testProcess(self):
#     """Tests the Process function."""
#     key_path = (
#         u'\\Software\\Microsoft\\Office\\15.0\\Outlook\\Search\\Catalog')
#     values = []
#
#     values.append(winreg_test_lib.TestRegValue(
#         ('C:\\Users\\username\\AppData\\Local\\Microsoft\\Outlook\\'
#          'username@example.com.ost'), '\x94\x01\x00\x00\x00\x00',
#         winreg_test_lib.TestRegValue.REG_BINARY, offset=827))
#
#     winreg_key = winreg_test_lib.TestRegKey(
#         key_path, 1346145829002031, values, 3421)
#
#     # TODO: add test for Catalog key.


if __name__ == '__main__':
  unittest.main()
