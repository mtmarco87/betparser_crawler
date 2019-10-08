import pyrebase
from bet_parser.settings import *
from bet_parser.models.Match import Match
from typing import List
import unidecode
import os


class FirebaseWriter:
    """
    Writer class able to write Parsed Matches to Firebase.
    """
    db_root: str = ''

    def __init__(self, db_root=FIREBASE_DEFAULT_DB_ROOT):
        self.db_root = db_root

    """
    Input: List[Match] - Matches list 
    Minimum required data: Bookmaker, StartDate, Team1, Team2 (for unique key in DB)
    """
    def write(self, parsed_matches: List[Match], deduplicate: bool = True):
        # Init Firebase app
        firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
        # Get Database
        db = firebase.database()

        inserted_paths = []
        for match in parsed_matches:
            db_path = self.db_root + '/' + match.StartDate + '/' + self.clean_string(match.Team1) + \
                      '_' + self.clean_string(match.Team2)
            if db_path not in inserted_paths:
                if deduplicate:
                    inserted_paths.append(db_path)
                db_key = match.Bookmaker
                db.child(db_path).child(db_key).set(match.dict())

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
