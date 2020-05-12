# EFIC(Extracts Filehistory IntelligenCe) 

## Introduction
*EFIC is an analyzing digital forensic artifacts of Windows FileHistory.

## Usage

1. We developed a preprocessor works as a parser module for plaso.

When using plaso, you can input the parser-plugin as follows.
"--parsers "mbr,gpt_entry,winreg/windows_filehistory_homegroup,winreg/windows_filehistory_usage,winreg/windows_mounted_devices,esedb/filehistory_catalogedb,filehistory_restore,filehistory_config""

To generate psort result database,

a) *generate plaso storage
"log2timeline.py --parsers "mbr,gpt_entry,winreg/windows_filehistory_homegroup,winreg/windows_filehistory_usage,winreg/windows_mounted_devices,esedb/filehistory_catalogedb,filehistory_restore,filehistory_config" "plaso storage" "input evidence image""

b) *generate log2timeline table
"psort.py -o 4n6time_sqlite --evidence "evidence file name" -w "psort result database" "plaso storage""

2. We developed an intelligence extractor from psort result database

"EFIC.py --input_psort "psort result database" --output_result "output database""
