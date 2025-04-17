import firebase_admin
from firebase_admin import credentials, db
from bet_parser.settings import FIREBASE_CONFIG, FIREBASE_DEFAULT_DB_ROOT
from bet_parser.models.Match import Match
from typing import List
import unidecode
import os

class FirebaseWriter:
    """
    Writer class able to write Parsed Matches to Firebase using the firebase-admin SDK.
    """
    db_root: str = ''

    def __init__(self, db_root=FIREBASE_DEFAULT_DB_ROOT):
        self.db_root = db_root

        # Initialize Firebase Admin SDK
        if not firebase_admin._apps:  # Ensure Firebase is initialized only once
            cred = None
            if FIREBASE_CONFIG["serviceAccountKeyPath"]:
                cred = credentials.Certificate(FIREBASE_CONFIG["serviceAccountKeyPath"])
            firebase_admin.initialize_app(cred, {
                'databaseURL': FIREBASE_CONFIG["databaseURL"]
            })

    """
    Writes parsed matches to Firebase Realtime Database.
    Minimum required data: Bookmaker, StartDate, Team1, Team2 (for unique key in DB)
    :param parsed_matches: List of Match objects to write.
    :param deduplicate: Whether to deduplicate entries before writing.
    """
    def write(self, parsed_matches: List[Match], deduplicate: bool = True):
        inserted_paths = []
        for match in parsed_matches:
            db_path = f"{self.db_root}/{match.StartDate}_{self.clean_string(match.Team1)}_{self.clean_string(match.Team2)}"
            if db_path not in inserted_paths:
                if deduplicate:
                    inserted_paths.append(db_path)
                db_key = match.Bookmaker
                db.reference(db_path).child(db_key).set(match.dict())

    """
    Renames a root key in Firebase Realtime Database by copying data to a new key and deleting the old key.
    
    :param old_key: The existing root key to rename.
    :param new_key: The new root key name.
    """
    def rename_root_key(self, old_key: str, new_key: str):
        ref = db.reference('/')
        
        # Read data from the old key
        old_data = ref.child(old_key).get()
        if old_data is None:
            print(f"No data found under the key '{old_key}'.")
            return

        # Write data to the new key
        ref.child(new_key).set(old_data)
        print(f"Data successfully copied from '{old_key}' to '{new_key}'.")

        # Delete the old key
        ref.child(old_key).delete()
        print(f"Old key '{old_key}' has been deleted.")

    """
    Cleans a string by removing spaces, special characters, and converting to lowercase.
    :param string: The string to clean.
    :return: Cleaned string.
    """
    @staticmethod
    def clean_string(string):
        return unidecode.unidecode(string.replace(" ", "").replace(".", "").replace("/", "").lower())

class FileWriter:
    """
    Writer class able to write Parsed Matches to File (csv+html).
    """
    out_folder: str = ''
    format_csv: str = 'csv'
    format_html: str = 'html'
    format_txt: str = 'txt'

    def __init__(self, out_folder=''):
        self.out_folder = out_folder

    """
    Input: str          - Output Filename
    Input: List[Match]  - Matches list
    Input: bytes        - Page html (optional)
    Minimum required data: None (no need of unique key, sequential write)
    """

    def write(self, filename: str, parsed_matches: List[Match], html: bytes = None):
        # Write Matches quotes to CSV file
        filename_csv = self.get_file_path(filename, self.format_csv)
        with open(filename_csv, 'w') as f:
            f.write('Bookmaker,StartDate,StartTime,RealTime,Team1,Team2,Quote1,QuoteX,Quote2,Result;\n')
            for match in parsed_matches:
                line = ''
                for key, item in match.dict().items():
                    line += item + (',' if key != 'Result' else ';')
                f.write('%s\n' % line)

        # Dumps, if available, Matches webpage to file
        if html:
            filename_html = self.get_file_path(filename, self.format_html)
            with open(filename_html, 'wb') as f:
                f.write(html)

    """
    Input: str          - Output File Name
    Input: str          - Content to append
    Appends raw string data to file
    """

    def append(self, filename: str, content: str, file_format: str = None):
        filename_out = self.get_file_path(filename, file_format)
        with open(filename_out, 'a+') as f:
            f.write(content)

    """
    Input: str          - File Name to read
    """

    def readlines(self, filename: str, file_format: str = None):
        filename_in = self.get_file_path(filename, file_format)
        with open(filename_in, 'r') as f:
            return f.readlines()

    def deduplicate(self, in_filename: str, file_format: str = None, by_first_column: bool = False):
        content = self.readlines(in_filename, file_format)

        already_inserted = {}
        for line in content:
            splitted = line.split(',')
            if by_first_column and len(splitted) > 1 and splitted[0] not in already_inserted.keys():
                already_inserted[splitted[0]] = line
                self.append(in_filename + '_deduplicate', line, file_format)
            elif not by_first_column and line not in already_inserted.keys():
                already_inserted.setdefault(line)
                self.append(in_filename + '_deduplicate', line, file_format)

    def deduplicate_and_replace(self, in_filename: str, file_format: str = None, by_first_column: bool = False):
        # Create Deduplicate file
        self.deduplicate(in_filename, file_format, by_first_column)

        old_file = self.get_file_path(in_filename, file_format)
        new_file = self.get_file_path(in_filename + '_deduplicate', file_format)
        # Remove old file
        os.remove(old_file)
        os.rename(new_file, old_file)

    def get_file_path(self, filename: str, file_format: str = None):
        return (self.out_folder + '/' if self.out_folder else '') + filename + '.' + \
               (file_format or self.format_txt)

    @staticmethod
    def deduplicate_ml_data():
        file_writer = FileWriter(TEAM_NAMES_VALIDATION_PATH)
        file_writer.deduplicate('team_names', 'csv', True)
