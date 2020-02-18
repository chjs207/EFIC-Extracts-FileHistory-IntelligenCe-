## filehistory_preprocessor

This project is a preprocessor for analyzing digital forensic artifacts of Windows FileHistory.
The developed parser works as a parser module for plaso.

When using plaso, you can input the module as follows.
"--parsers esedb/filehistory_catalogedb,filehistory_config,filehistory_restore"

For testing filehistory_parser
1. generate plaso storage
"log2timeline.py --parsers "mbr,gpt_entry,winreg/windows_filehistory_homegroup,winreg/windows_filehistory_usage,winreg/windows_mounted_devices,esedb/filehistory_catalogedb,filehistory_restore,filehistory_config" test_filehistory.plaso ResultFile/test_new_data.vhd"

2. generate log2timeline table
"psort.py -o 4n6time_sqlite -w test.db test_filehistory.plaso"
