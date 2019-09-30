import pyrebase
from bet_parser.settings import *


class FirebaseWriter:
    """
    Writer class able to write Parsed Matches to Firebase.

    """
    db_root: str = ''

    def __init__(self, db_root=FIREBASE_DEFAULT_DB_ROOT):
        self.db_root = db_root

    """
    Minimum required data structure:
    parsed_matches = [ {'Bookmaker':, 'StartDate':, 'Team1':, 'Team2':}, ... ]
    """
    def write(self, parsed_matches: list):
        # Init Firebase app
        firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
        # Get Database
        db = firebase.database()

        for match in parsed_matches:
            db_path = self.db_root + match['Bookmaker'] + '/' + match['StartDate']
            db_key = self.clean_string(match['Team1']) + '_' + self.clean_string(match['Team2'])
            db.child(db_path).child(db_key).set(match)

    @staticmethod
    def clean_string(string):
        return string.replace(" ", "").replace(".", "").lower()


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
    Required data structure:
    parsed_matches = [ {'Bookmaker':, 'StartDate':, 'StartTime':, 'RealTime':, 
                        'Team1':, 'Team2':, 'Result':, 'Quote1':, 'QuoteX': , 'Quote2':}, ... ]
    """
    def write(self, filename: str, parsed_matches: list, html: bytes = None):
        # Write Matches quotes to CSV file
        filename_csv = (self.out_folder + '/' if self.out_folder else '') + filename + self.format_csv
        with open(filename_csv, 'w') as f:
            f.write('Bookmaker,StartDate,StartTime,RealTime,Team1,Team2,Result,Quote1,QuoteX,Quote2;\n')
            for match in parsed_matches:
                line = ''
                for key, item in match.items():
                    line += item + (',' if key != 'Quote2' else ';')
                f.write('%s\n' % line)

        # Dumps, if available, Matches webpage to file
        if html:
            filename_html = (self.out_folder + '/' if self.out_folder else '') + filename + self.format_html
            with open(filename_html, 'wb') as f:
                f.write(html)
