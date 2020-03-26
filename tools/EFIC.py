import sqlite3
import argparse


class WriteFilehistoryIntelligenCe():
    conn = None
    cursor = None
    file_path = None

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.file_path = None

    def initialize_result_file(self, file_path):
        self.file_path = file_path
        self.conn = sqlite3.connect(self.file_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists filehistory '
                            '(Who_PC_name_ text, Who_User_name_ text, When_ text, Time_source_ text, '
                            'Where_ text, How_ text, What_ text, Source_ text)')
        self.conn.commit()

    def close_result_file(self):
        self.cursor.close()
        self.conn.close()


class ExtractFilehistoryIntelligenCe():

    def __init__(self):
        self.write_result_file = WriteFilehistoryIntelligenCe()

    def extract_configuration(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath) #initialize result database

        cur = cursor.execute(
            "select distinct description, filename, datetime, evidence "
            "from log2timeline where sourcetype like '%FileHistory%Configuration%'")
        rows = cur.fetchall()

        for row in rows:
            source_file = row[3] + row[1]
            description = row[0]
            date_time = row[2]
            default_backup_folder = []
            user_backup_folder = []
            user_exclude_folder = []
            split_description = description.split('|`')
            for items in split_description:
                if 'UserName:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        user_name = items.replace('UserName:', '')
                    else:
                        user_name = ''
                elif 'FriendlyName:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        friendly_name = items.replace('FriendlyName:', '')
                    else:
                        friendly_name = ''
                elif 'PCName:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        pc_name = items.replace('PCName:', '')
                    else:
                        pc_name = ''
                elif 'Library:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        backup_folder = items.replace('Library:', '')
                        folders = backup_folder.split(',')
                        for folder in folders:
                            if folder == '':
                                continue
                            default_backup_folder.append(folder)
                    else:
                        default_backup_folder = []
                elif 'UserFolder:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        user_folder = items.replace('UserFolder:', '')
                        folders = user_folder.split(',')
                        for folder in folders:
                            if folder == '':
                                continue
                            user_backup_folder.append(folder)
                    else:
                        user_backup_folder = []
                elif 'FolderExclude:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        exclude_folder = items.replace('FolderExclude:', '')
                        folders = exclude_folder.split(',')
                        for folder in folders:
                            if folder == '':
                                continue
                            user_exclude_folder.append(folder)
                    else:
                        user_exclude_folder = []
                elif 'RetentionPolicy:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        retention_policy = items.replace('RetentionPolicy:', '')
                    else:
                        retention_policy = ''
                elif 'RetentionAge:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        retention_age = items.replace('RetentionAge:', '')
                    else:
                        retention_age = ''
                elif 'FileHistory Frequency:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        filehistory_frequency = items.replace('FileHistory Frequency:', '')
                    else:
                        filehistory_frequency = ''
                elif 'FileHistory Status:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        filehistory_status = items.replace('FileHistory Status:', '')
                    else:
                        filehistory_status = ''
                elif 'BackupStorage Name:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        backupstorage_name = items.replace('BackupStorage Name:', '')
                    else:
                        backupstorage_name = ''
                elif 'BackupStorage Drive Letter:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        drive_letter = items.replace('BackupStorage Drive Letter:', '')
                    else:
                        drive_letter = ''
                elif 'BackupStorage Volume GUID:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        if '\\?\Volume' in items:
                            volume_guid = items.replace('BackupStorage Volume GUID:\\\\?\\Volume', '')
                            volume_guid = volume_guid.replace('\\', '')
                        else:
                            volume_guid = items.replace('BackupStorage Volume GUID:', '')
                    else:
                        volume_guid = ''
                elif 'BackupStorage Type:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        storage_type = items.replace('BackupStorage Type:', '')
                    else:
                        storage_type = ''
                elif 'BackupStorage Path:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        backup_data = items.replace('BackupStorage Path:', '')
                    else:
                        backup_data = ''
                else:
                    continue

            for list_backup_folder in default_backup_folder:
                self.write_result_file.cursor.execute(
                    "insert into filehistory values (?,?,?,?,?,?,?,?)",
                    (pc_name, user_name, date_time, 'Modified time of Config.xml',
                     'Host Windows', 'Include folder to backup', list_backup_folder, source_file))
                self.write_result_file.conn.commit()
            for list_backup_folder in user_backup_folder:
                self.write_result_file.cursor.execute(
                    "insert into filehistory values (?,?,?,?,?,?,?,?)",
                    (pc_name, user_name, date_time, 'Modified time of Config.xml',
                     'Host Windows', 'Include folder to backup', list_backup_folder, source_file))
                self.write_result_file.conn.commit()
            for list_backup_folder in user_exclude_folder:
                self.write_result_file.cursor.execute(
                    "insert into filehistory values (?,?,?,?,?,?,?,?)",
                    (pc_name, user_name, date_time, 'Modified time of Config.xml',
                     'Host Windows', 'Exclude folder to backup', list_backup_folder, source_file))
            self.write_result_file.cursor.execute(
                "insert into filehistory values (?,?,?,?,?,?,?,?)",
                (pc_name, user_name, date_time, 'Modified time of Config.xml',
                 'Host Windows', 'Set Retention Policy of FileHistory backup data', retention_policy, source_file))
            self.write_result_file.conn.commit()
            self.write_result_file.cursor.execute(
                "insert into filehistory values (?,?,?,?,?,?,?,?)",
                (pc_name, user_name, date_time, 'Modified time of Config.xml',
                 'Host Windows', 'Set Retention Age of FileHistory backup data', retention_age, source_file))
            self.write_result_file.conn.commit()
            self.write_result_file.cursor.execute(
                "insert into filehistory values (?,?,?,?,?,?,?,?)",
                (pc_name, user_name, date_time, 'Modified time of Config.xml',
                 'Host Windows', 'Set FileHistory Backup Cycle', filehistory_frequency, source_file))
            self.write_result_file.conn.commit()
            self.write_result_file.cursor.execute(
                "insert into filehistory values (?,?,?,?,?,?,?,?)",
                (pc_name, user_name, date_time, 'Modified time of Config.xml',
                 'Host Windows', 'Set FileHistory Status', filehistory_status, source_file))
            self.write_result_file.conn.commit()
            self.write_result_file.cursor.execute(
                "insert into filehistory values (?,?,?,?,?,?,?,?)",
                (pc_name, user_name, date_time, 'Modified time of Config.xml',
                 'Host Windows', 'Use FileHistory Backup Storage',
                 backupstorage_name + "," + volume_guid + "," + storage_type, source_file))
            self.write_result_file.conn.commit()
            self.write_result_file.cursor.execute(
                "insert into filehistory values (?,?,?,?,?,?,?,?)",
                (pc_name, user_name, date_time, 'Modified time of Config.xml',
                 'Host Windows', 'Store Backup Data', backup_data, source_file))
            self.write_result_file.conn.commit()
        self.write_result_file.close_result_file()

    def extract_restorelog(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)

        cur = cursor.execute(
            "select distinct description, filename, evidence, host, datetime "
            "from log2timeline where sourcetype like '%FileHistory%RestoreLog%'")
        rows = cur.fetchall()
        for row in rows:
            pc_name = row[3]
            date_time = row[4]
            source_file = row[2] + row[1]
            description = row[0]
            split_description = description.split('|`')
            for items in split_description:
                if 'FileRecordID:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        file_record_id = items.replace('FileRecordID:', '')
                    else:
                        file_record_id = ''
                elif 'Restored File:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        restore_file = items.replace('Restored File:', '')
                    else:
                        restore_file = ''
                elif 'USN of File:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        file_usn = items.replace('USN of File:', '')
                    else:
                        file_usn = ''
                elif 'Creation Date:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        creation_date = items.replace('Creation Date:')
                    else:
                        creation_date = ''
                elif 'Modification Date:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        modification_date = items.replace('Modification Date:')
                    else:
                        modification_date = ''
                else:
                    continue
            self.write_result_file.cursor.execute(
                "insert into filehistory values (?,?,?,?,?,?,?,?)",
                (pc_name, "-", date_time, 'Modified time of Restore.log',
                'Host Windows', 'Restore File by using FileHistory',
                 restore_file + ", " + "Tc is " + creation_date + ", Tm is " + modification_date +
                 ", Fid is " + file_record_id + ", Fus is " + file_usn, source_file))
            self.write_result_file.conn.commit()
        self.write_result_file.close_result_file()

    def extract_backup_folder(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)
        cur = cursor.execute(
            "select distinct description, filename, evidence, datetime, host "
            "from log2timeline where sourcetype like '%FileHistory%Backup%Folder%'")
        rows = cur.fetchall()
        for row in rows:
            host = row[4]
            date_time = row[3]
            source_file = row[2] + row[1]
            backup_folders = row[0].replace('BackupFolder:', '')
            backup_folder = backup_folders.split(',')
            if len(backup_folder) > 1:
                for item in backup_folder:
                    if item == '':
                        continue
                    elif '?Exclude' in item:
                        exclude_folder = item.replace('?Exclude', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?)",
                            (host, '-', date_time, '-', 'Host Windows', 'Exclude folder to backup',
                             exclude_folder, source_file))
                        self.write_result_file.conn.commit()
                    else:
                        include_folder = item
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?)",
                            (host, '-', date_time, '-', 'Host Windows', 'Include folder to backup',
                             include_folder, source_file))
                        self.write_result_file.conn.commit()
            else:
                continue
        self.write_result_file.close_result_file()

    def extract_global(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)
        cur = cursor.execute(
            "select distinct description, filename, evidence, datetime, host "
            "from log2timeline where sourcetype like '%FileHistory%Global%'")
        rows = cur.fetchall()

        for row in rows:
            date_time = row[3]
            host = row[4]
            source_file = row[2] + row[1]
            backup_times = row[0].split('|`')
            first_backup_times = backup_times[0].split(':')
            if len(first_backup_times) > 1:
                first_backup_time = backup_times[0].replace('First FileHistory Backup:', '')
                last_backup_time = backup_times[1].replace('Last FileHistory Backup:', '')
                self.write_result_file.cursor.execute(
                    "insert into filehistory values (?,?,?,?,?,?,?,?)",
                    (host, '-', date_time, '-', 'Host Windows', "First Backup", first_backup_time, source_file))
                self.write_result_file.conn.commit()
                self.write_result_file.cursor.execute(
                    "insert into filehistory values (?,?,?,?,?,?,?,?)",
                    (host, '-', date_time, '-', 'Host Windows', "Lasat Backup", last_backup_time, source_file))
                self.write_result_file.conn.commit()
        self.write_result_file.close_result_file()

    def extract_filelist(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)
        cur = cursor.execute(
            "select distinct description, filename, evidence, datetime, host "
            "from log2timeline where sourcetype like '%FileHistory%Backup%File%List%'")
        rows = cur.fetchall()
        for row in rows:
            date_time = row[3]
            host = row[4]
            source_file = row[2] + row[1]
            description = row[0].split('|`')
            for items in description:
                if 'Backuped Timestamp:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        backup_date = items.replace('Backuped Timestamp:', '')
                    else:
                        backup_date = ''
                elif 'Filename:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        file_name = items.replace('Filename:', '')
                    else:
                        file_name = ''
                elif 'USN number:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        usn_number = items.replace('USN number:', '')
                    else:
                        usn_number = ''
                elif 'Creation Date:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        creation_date = items.replace('Creation Date:', '')
                    else:
                        creation_date = ''
                elif 'Modification Date:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        modification_date = items.replace('Modification Date:', '')
                    else:
                        modification_date = ''
                elif 'Filesize:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        file_size = items.replace('Filesize:', '')
                    else:
                        file_size = ''
                elif 'FileRecordId:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        file_record_id = items.replace('FileRecordId:', '')
                    else:
                        file_record_id = ''
                else:
                    continue
            self.write_result_file.cursor.execute(
                "insert into filehistory values (?,?,?,?,?,?,?,?)",
                (host, "-", backup_date, "backupset table of Catalog.edb", "Host Windows", "Back up this file",
                 file_name + "(" + "Fid is " + file_record_id + ", Fus is " + usn_number + ", Fsz is " + file_size + ")", source_file))
            self.write_result_file.conn.commit()
            self.write_result_file.cursor.execute(
                "insert into filehistory values (?,?,?,?,?,?,?,?)",
                (host, "-", creation_date, "namespace table of Catalog.edb", "Host Windows", "Create this file",
                 file_name + "(" + "Fid is " + file_record_id + ", Fus is " + usn_number + ", Fsz is " + file_size + ")",
                 source_file))
            self.write_result_file.conn.commit()
            self.write_result_file.cursor.execute(
                "insert into filehistory values (?,?,?,?,?,?,?,?)",
                (host, "-", modification_date, "backupset table of Catalog.edb", "Host Windows", "Modify this file",
                 file_name + "(" + "Fid is " + file_record_id + ", Fus is " + usn_number + ", Fsz is " + file_size + ")",
                 source_file))
            self.write_result_file.conn.commit()
        self.write_result_file.close_result_file()

    def extract_gpt_entry(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)
        cur = cursor.execute(
            "select distinct description, filename, evidence, datetime, host "
            "from log2timeline where sourcetype like '%GPT%Entry%DriveSignature%'")
        rows = cur.fetchall()
        for row in rows:
            date_time = row[3]
            host = row[4]
            source_file = row[2] + row[1]
            description = row[0].split(":")
            if len(description) > 1:
                volume_guid = description[1]
                self.write_result_file.cursor.execute(
                    "insert into filehistory values (?,?,?,?,?,?,?,?)",
                    (host, "-", date_time, "-", "External Storage", "Use storage", volume_guid, source_file))
                self.write_result_file.conn.commit()
        self.write_result_file.close_result_file()

    def extract_mbr(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)
        cur = cursor.execute(
            "select distinct description, filename, evidence "
            "from log2timeline where sourcetype like '%MBR%DriveSignature%'")
        rows = cur.fetchall()
        for row in rows:
            date_time = row[3]
            host = row[4]
            source_file = row[2] + row[1]
            description = row[0].split(':')
            if len(description) > 1:
                drive_signature = description[1]
                self.write_result_file.cursor.execute(
                    "insert into filehistory values (?,?,?,?,?,?,?,?)",
                    (host, "-", date_time, "-", "External Storage", "Use storage", drive_signature, source_file))
                self.write_result_file.conn.commit()
        self.write_result_file.close_result_file()

    def extract_mounteddevices(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)
        cur = cursor.execute(
            "select distinct description, filename, datetime, evidence, host "
            "from log2timeline where sourcetype like '%Registry%Key:%MountedDeivces%'")
        rows = cur.fetchall()
        for row in rows:
            date_time = row[2]
            host = row[4]
            source_file = row[3] + row[1]
            description = row[0].split('|`')
            drive_letter = ''
            disk_signature = ''
            if 'Drive Letter:' in description[1]:
                item = description[1].split(':')
                if len(item) > 1:
                    drive_letter = description[1].replace('Drive Letter:', '')
                else:
                    drive_letter = ''
            if 'Disk Signature:' in description[2]:
                item = description[2].split(':')
                if len(item) > 1:
                    disk_signature = description[2].replace('Disk Signature:', '')
                else:
                    disk_signature = ''
            self.write_result_file.cursor.execute(
                "insert into filehistory values (?,?,?,?,?,?,?,?)",
                (host, "-", date_time, "Registry key Last written time", 'Host Windows', 'Use storage',
                 "(" + drive_letter + ")" + ", " + disk_signature, source_file))
            self.write_result_file.conn.commit()
        self.write_result_file.close_result_file()

    def extract_homegroup(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)
        cur = cursor.execute(
            "select distinct description, filename, evidence, datetime, host "
            "from log2timeline where sourcetype like '%Registry%Key:%FileHistory_Homegroup%'")
        rows = cur.fetchall()
        for row in rows:
            date_time = row[3]
            host = row[4]
            source_file = row[2] + row[1]
            description = row[0].split('|`')
            user_type = ''
            backup_storage_name = ''
            drive_letter = ''
            filehistory_pcname = ''
            for items in description:
                if 'User type:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        user_type = items.replace('User type:', '')
                    else:
                        user_type = ''
                elif 'Folder Path:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        drive_letter = items.replace('Folder Path:', '')
                    else:
                        drive_letter = ''
                elif 'Friendly name:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        backup_storage_name = items.replace('Friendly name:', '')
                    else:
                        backup_storage_name = ''
                elif 'Share point:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        filehistory_pcname = items.replace('\\\\', '')
                        filehistory_pcname = filehistory_pcname.replace('Share point:', '')
                        filehistory_pcname = filehistory_pcname.replace('\\FileHistory1\\', '')
                    else:
                        filehistory_pcname = ''
                else:
                    continue
            self.write_result_file.cursor.execute(
                "insert into filehistory values (?,?,?,?,?,?,?,?)",
                (host, "-", date_time, "Registry key Last written time", 'Host Windows',
                 "Use stroage as FileHistory " + user_type, backup_storage_name + "(" + drive_letter + ")" + " of " + filehistory_pcname,
                 source_file))
            self.write_result_file.conn.commit()

    def extract_filehistory_usage(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)
        cur = cursor.execute(
            "select distinct description, filename, evidence, datetime, host "
            "from log2timeline where sourcetype like '%Registry%Key:%FileHistoryUsage%'")
        rows = cur.fetchall()
        for row in rows:
            date_time = row[3]
            host = row[4]
            source_file = row[2] + row[1]
            description = row[0].split('|`')
            for items in description:
                if 'Last Backup Time:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        last_backup_time = items.replace('Last Backup Time:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?)",
                            (host, "-", last_backup_time, "Registry value", "Host Windows", "Last Backup", "FileHistory", source_file))
                        self.write_result_file.conn.commit()
                elif 'Backup Storage Changed:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        backup_storage_changed = items.replace('Backup Storage Changed:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?)",
                            (host, "-", date_time, "Registry key Last written time", "Host Windows", backup_storage_changed,
                             "Backup storage", source_file))
                        self.write_result_file.conn.commit()
                else:
                    continue

def main():
    parser = argparse.ArgumentParser(prog='EFIC (Extract Filehistory IntelligenCe)')
    parser.add_argument('--input_psort', type=str, help='input path of Plaso result database as sqlite')
    parser.add_argument('--output_result', type=str, help='output intelligence database as sqlite')

    args = parser.parse_args()

    input_psort = args.input_psort
    output_result = args.output_result
    conn = sqlite3.connect(input_psort)
    cursor = conn.cursor()

    ext_filehistory = ExtractFilehistoryIntelligenCe()
    ext_filehistory.extract_configuration(cursor, output_result)
    ext_filehistory.extract_backup_folder(cursor, output_result)
    ext_filehistory.extract_filelist(cursor, output_result)
    ext_filehistory.extract_global(cursor, output_result)
    ext_filehistory.extract_gpt_entry(cursor, output_result)
    ext_filehistory.extract_homegroup(cursor, output_result)
    ext_filehistory.extract_mbr(cursor, output_result)
    ext_filehistory.extract_mounteddevices(cursor, output_result)
    ext_filehistory.extract_filehistory_usage(cursor, output_result)

if __name__=="__main__":
    main()