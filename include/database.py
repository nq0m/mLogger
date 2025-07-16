import os
import sqlite3
from typing import Any, Dict, List, Optional
import appdirs

APP_NAME = 'mLogger'
DB_FILENAME = 'mlogger.db'

def get_default_db_path():
    data_dir = appdirs.user_data_dir(APP_NAME)
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, DB_FILENAME)

class ContactDB:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or get_default_db_path()
        self.conn = sqlite3.connect(self.db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                callsign TEXT,
                sent_rst TEXT,
                recv_rst TEXT,
                park TEXT,
                frequency TEXT,
                mode TEXT,
                comments TEXT,
                band TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_contact(self, contact: Dict[str, Any]):
        self.conn.execute('''
            INSERT INTO contacts (callsign, sent_rst, recv_rst, park, frequency, mode, comments, band, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            contact.get('callsign'),
            contact.get('sent_rst'),
            contact.get('recv_rst'),
            contact.get('park'),
            contact.get('frequency'),
            contact.get('mode'),
            contact.get('comments'),
            contact.get('band'),
            contact.get('timestamp')
        ))
        self.conn.commit()

    def get_contacts(self) -> List[Dict[str, Any]]:
        cursor = self.conn.execute('SELECT callsign, sent_rst, recv_rst, park, frequency, mode, comments, band, timestamp FROM contacts ORDER BY timestamp DESC')
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def close(self):
        self.conn.close()
