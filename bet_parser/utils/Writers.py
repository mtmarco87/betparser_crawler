import pyrebase
from bet_parser.settings import *
from bet_parser.models.Match import Match
from typing import List


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
    def write(self, parsed_matches: List[Match]):
        # Init Firebase app
        firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
        # Get Database
        db = firebase.database()

        for match in parsed_matches:
            db_path = self.db_root + match.Bookmaker + '/' + match.StartDate
            db_key = self.clean_string(match.Team1) + '_' + self.clean_string(match.Team2)
            db.child(db_path).child(db_key).set(match.dict())

    @staticmethod
    def clean_string(string):
        return string.replace(" ", "").replace(".", "").replace("/", "").lower()


class FileWriter:
    """
    Writer class able to write Parsed Matches to File (csv+html).

    """
    out_folder: str = ''
    format_csv: str = '.csv'
    format_html: str = '.html'

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
        filename_csv = (self.out_folder + '/' if self.out_folder else '') + filename + self.format_csv
        with open(filename_csv, 'w') as f:
            f.write('Bookmaker,StartDate,StartTime,RealTime,Team1,Team2,Quote1,QuoteX,Quote2,Result;\n')
            for match in parsed_matches:
                line = ''
                for key, item in match.dict().items():
                    line += item + (',' if key != 'Result' else ';')
                f.write('%s\n' % line)

        # Dumps, if available, Matches webpage to file
        if html:
            filename_html = (self.out_folder + '/' if self.out_folder else '') + filename + self.format_html
            with open(filename_html, 'wb') as f:
                f.write(html)
