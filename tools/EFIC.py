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
                            '(info_type text, information text, file_name text, '
                            'backup_date text, creation_date text, modification_date text, '
                            'file_record_id text, usn text, file_size text, extra text, from_file text)')
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
            "select distinct description, filename, datetime "
            "from log2timeline where sourcetype like '%FileHistory%Configuration%'")
        rows = cur.fetchall()
        for row in rows:
            description = row[0]
            split_description = description.split('|`')
            for items in split_description:
                if 'UserName:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        user_name = items.replace('UserName:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('User name', user_name, '', '', '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
                elif 'FriendlyName:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        friendly_name = items.replace('FriendlyName:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('User name', friendly_name, '', '', '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
                elif 'PCName:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        pc_name = items.replace('PCName:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?, ?)",
                            ('PC name', pc_name, '', '', '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
                elif 'Library:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        backup_folder = items.replace('Library:', '')
                        folders = backup_folder.split(',')
                        for folder in folders:
                            if folder == ' ':
                                continue
                            self.write_result_file.cursor.execute(
                                "insert into filehistory values (?,?,?,?,?,?,?,?,?,?, ?)",
                                ('Backup folder', folder, '', '', '', '', '', '', '', '', row[1]))
                            self.write_result_file.conn.commit()
                elif 'UserFolder:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        user_folder = items.replace('UserFolder:', '')
                        folders = user_folder.split(',')
                        for folder in folders:
                            if folder == ' ':
                                continue
                            self.write_result_file.cursor.execute(
                                "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                                ('Backup folder', folder, '', '', '', '', '', '', '', '', row[1]))
                            self.write_result_file.conn.commit()
                elif 'FolderExclude:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        exclude_folder = items.replace('FolderExclude:', '')
                        folders = exclude_folder.split(',')
                        for folder in folders:
                            if folder == ' ':
                                continue
                            self.write_result_file.cursor.execute(
                                "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                                ('Exclude folder', folder, '', '', '', '', '', '', '', '', row[1]))
                            self.write_result_file.conn.commit()
                elif 'RetentionPolicy:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        retention_policy = items.replace('RetentionPolicy:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('Retention type', retention_policy, '', '', '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
                elif 'RetentionAge:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        retention_age = items.replace('RetentionAge:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('Retention age', retention_age, '', '', '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
                elif 'FileHistory Frequency:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        filehistory_frequency = items.replace('FileHistory Frequency:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('Backup cycle', filehistory_frequency, '', '', '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
                elif 'FileHistory Status:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        status = items.replace('FileHistory Status:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('Backup status', status, '', '', '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
                elif 'BackupStorage Name:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        backupstorage_name = items.replace('BackupStorage Name:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('Storage name', backupstorage_name, '', '', '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
                elif 'BackupStorage Drive Letter:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        drive_letter = items.replace('BackupStorage Drive Letter:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('Storage letter', drive_letter, '', '', '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
                elif 'BackupStorage Volume GUID:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        if '\\?\Volume' in items:
                            volume_guid = items.replace('BackupStorage Volume GUID:\\\\?\\Volume', '')
                            volume_guid = volume_guid.replace('\\', '')
                            self.write_result_file.cursor.execute(
                                "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                                ('Storage GUID', volume_guid, '', '', '', '', '', '', '', '', row[1]))
                            self.write_result_file.conn.commit()
                        else:
                            volume_guid = items.replace('BackupStorage Volume GUID:', '')
                            self.write_result_file.cursor.execute(
                                "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                                ('Storage GUID', volume_guid, '', '', '', '', '', '', '', '', row[1]))
                            self.write_result_file.conn.commit()
                elif 'BackupStorage Path:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        backupstorage_path = items.replace('BackupStorage Path:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('Backup location', backupstorage_path, '', '', '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
                else:
                    continue

        self.write_result_file.close_result_file()

    def extract_restorelog(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)

        cur = cursor.execute(
            "select distinct description, filename "
            "from log2timeline where sourcetype like '%FileHistory%RestoreLog%'")
        rows = cur.fetchall()
        for row in rows:
            description = row[0]
            split_description = description.split('|`')
            for items in split_description:
                if 'FileRecordID:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        file_record_id = items.replace('FileRecordID:', '')
                elif 'Restored File:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        restore_file = items.replace('Restored File:', '')
                elif 'USN of File:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        file_usn = items.replace('USN of File:', '')
                elif 'Creation Date:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        creation_date = items.replace('Creation Date:')
                elif 'Modification Date:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        modification_date = items.replace('Modification Date:')
                else:
                    continue
            self.write_result_file.cursor.execute(
                "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                ("Restore log", "Restore file", restore_file, '',
                creation_date, modification_date, file_record_id, file_usn, '', '', row[1]))
            self.write_result_file.conn.commit()
        self.write_result_file.close_result_file()

    def extract_backup_folder(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)
        cur = cursor.execute(
            "select distinct description, filename "
            "from log2timeline where sourcetype like '%FileHistory%Backup%Folder%'")
        rows = cur.fetchall()
        for row in rows:
            backup_folders = row[0].replace('BackupFolder:', '')
            backup_folder = backup_folders.split(',')
            if len(backup_folder) > 1:
                for item in backup_folder:
                    if item == ' ':
                        continue
                    elif '?Exclude' in item:
                        exclude_folder = item.replace('?Exclude', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('Exclude folder', exclude_folder, '', '', '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
                    else:
                        include_folder = item
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('Backup folder', include_folder, '', '', '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
            else:
                continue
        self.write_result_file.close_result_file()

    def extract_global(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)

        cur = cursor.execute(
            "select distinct description, filename "
            "from log2timeline where sourcetype like '%FileHistory%Global%'")
        rows = cur.fetchall()
        for row in rows:
            backup_times = row[0].split('|`')
            first_backup_times = backup_times[0].split(':')
            if len(first_backup_times) > 1:
                first_backup_time = backup_times[0].replace('First FileHistory Backup:', '')
                last_backup_time = backup_times[1].replace('Last FileHistory Backup:', '')
                self.write_result_file.cursor.execute(
                    "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                    ('Backup date', "First backup", '', first_backup_time, '', '', '', '', '', '', row[1]))
                self.write_result_file.conn.commit()
                self.write_result_file.cursor.execute(
                    "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                    ('Backup date', "Last backup", '', last_backup_time, '', '', '', '', '', '', row[1]))
                self.write_result_file.conn.commit()
        self.write_result_file.close_result_file()

    def extract_filelist(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)
        cur = cursor.execute(
            "select distinct description, filename "
            "from log2timeline where sourcetype like '%FileHistory%Backup%File%List%'")
        rows = cur.fetchall()
        for row in rows:
            description = row[0].split('|`')
            for items in description:
                if 'Backuped Timestamp:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        backup_date = items.replace('Backuped Timestamp:', '')
                elif 'Filename:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        file_name = items.replace('Filename:', '')
                elif 'USN number:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        usn_number = items.replace('USN number:', '')
                elif 'Creation Date:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        creation_date = items.replace('Creation Date:', '')
                elif 'Modification Date:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        modification_date = items.replace('Modification Date:', '')
                elif 'Filesize:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        file_size = items.replace('Filesize:', '')
                elif 'FileRecordId:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        file_record_id = items.replace('FileRecordId:', '')
                else:
                    continue
            self.write_result_file.cursor.execute(
                "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                ("Backuped file", '', file_name, backup_date, creation_date,
                modification_date, file_record_id, usn_number, file_size, '', row[1]))
            self.write_result_file.conn.commit()
        self.write_result_file.close_result_file()

    def extract_gpt_entry(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)
        cur = cursor.execute(
            "select distinct description, filename "
            "from log2timeline where sourcetype like '%GPT%Entry%DriveSignature%'")
        rows = cur.fetchall()
        for row in rows:
            description = row[0].split(":")
            if len(description) > 1:
                volume_guid = description[1]
                self.write_result_file.cursor.execute(
                    "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                    ('Storage GUID', volume_guid, '', '', '', '', '', '', '', '', row[1]))
                self.write_result_file.conn.commit()
        self.write_result_file.close_result_file()

    def extract_mbr(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)
        cur = cursor.execute(
            "select distinct description, filename "
            "from log2timeline where sourcetype like '%MBR%DriveSignature%'")
        rows = cur.fetchall()
        for row in rows:
            description = row[0].split(':')
            if len(description) > 1:
                drive_signature = description[1]
                self.write_result_file.cursor.execute(
                    "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                    ('Storage GUID', drive_signature, '', '', '', '', '', '', '', '', row[1]))
                self.write_result_file.conn.commit()
        self.write_result_file.close_result_file()

    def extract_mounteddevices(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)
        cur = cursor.execute(
            "select distinct description, filename, datetime "
            "from log2timeline where sourcetype like '%Registry%Key:%MountedDeivces%'")
        rows = cur.fetchall()
        for row in rows:
            description = row[0].split('|`')
            drive_letter = ''
            disk_signature = ''
            if 'Drive Letter:' in description[1]:
                item = description[1].split(':')
                if len(item) > 1:
                    drive_letter = description[1].replace('Drive Letter:', '')
            if 'Disk Signature:' in description[2]:
                item = description[2].split(':')
                if len(item) > 1:
                    disk_signature = description[2].replace('Disk Signature:', '')
            self.write_result_file.cursor.execute(
                "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                ('Storage letter', drive_letter, '', '', '', '', '', '', '', disk_signature, row[1]))
            self.write_result_file.conn.commit()
            self.write_result_file.cursor.execute(
                "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                ('Storage GUID', disk_signature, '', '', '', '', '', '', '', drive_letter, row[1]))
            self.write_result_file.conn.commit()
        self.write_result_file.close_result_file()

    def extract_homegroup(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)
        cur = cursor.execute(
            "select distinct description, filename "
            "from log2timeline where sourcetype like '%Registry%Key:%FileHistory_Homegroup%'")
        rows = cur.fetchall()
        for row in rows:
            description = row[0].split('|`')
            for items in description:
                if 'User type:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        user_type = items.replace('User type:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('User type', user_type, '', '', '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
                elif 'Folder Path:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        drive_letter = items.replace('Folder Path:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('Storage letter', drive_letter, '', '', '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
                elif 'Friendly name:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        backup_storage_name = items.replace('Friendly name:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('Storage name', backup_storage_name, '', '', '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
                elif 'Share point:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        filehistory_pcname = items.replace('\\\\', '')
                        filehistory_pcname = filehistory_pcname.replace('Share point:', '')
                        filehistory_pcname = filehistory_pcname.replace('\\FileHistory1\\', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('PC name', filehistory_pcname, '', '', '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
                else:
                    continue

    def extract_filehistory_usage(self, cursor, output_filepath):
        self.write_result_file.initialize_result_file(output_filepath)
        cur = cursor.execute(
            "select distinct description, filename "
            "from log2timeline where sourcetype like '%Registry%Key:%FileHistoryUsage%'")
        rows = cur.fetchall()
        for row in rows:
            description = row[0].split('|`')
            for items in description:
                if 'Last Backup Time:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        last_backup_time = items.replace('Last Backup Time:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('Backup date', 'Last Backup', '', last_backup_time, '', '', '', '', '', '', row[1]))
                        self.write_result_file.conn.commit()
                elif 'Backup Storage Changed:' in items:
                    item = items.split(':')
                    if len(item) > 1:
                        backup_storage_changed = items.replace('Backup Storage Changed:', '')
                        self.write_result_file.cursor.execute(
                            "insert into filehistory values (?,?,?,?,?,?,?,?,?,?,?)",
                            ('Storage changed', backup_storage_changed, '', '', '', '', '', '', '', '', row[1]))
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