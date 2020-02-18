## EFIC(Extracts Filehistory IntelligenCe) 

EFIC is an analyzing digital forensic artifacts of Windows FileHistory.

1. We developed a preprocessor works as a parser module for plaso.

When using plaso, you can input the module as follows.
"--parsers "mbr,gpt_entry,winreg/windows_filehistory_homegroup,winreg/windows_filehistory_usage,winreg/windows_mounted_devices,esedb/filehistory_catalogedb,filehistory_restore,filehistory_config""

For testing filehistory_parser

a) generate plaso storage
"log2timeline.py --parsers "mbr,gpt_entry,winreg/windows_filehistory_homegroup,winreg/windows_filehistory_usage,winreg/windows_mounted_devices,esedb/filehistory_catalogedb,filehistory_restore,filehistory_config" test_filehistory.plaso ResultFile/test_new_data.vhd"

b) generate log2timeline table
"psort.py -o 4n6time_sqlite -w test.db test_filehistory.plaso"

2. We developed an extractor from plaso result database

"EFIC.py test.db(psor result database) efic_result.db"
