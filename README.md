## filehistory_parser

This project is a parser for analyzing digital forensic artifacts of Windows FileHistory.
The developed parser works as a parser module for plaso.

When using plaso, you can input the module as follows.
"--parsers esedb/filehistory_catalogedb,filehistory_config,filehistory_restore"

For testing filehistory_parser
1. generate plaso storage
"log2timeline.py --parsers esedb/filehistory_catalogedb,filehistory_config,filehistory_restore test_filehistory.plaso ResultFile/test_vhd.vhd"

2. generate log2timeline table
"psort.py -o 4n6time_sqlite -w test_filehistory.db test_filehistory.plaso"
