# memory/memory_store.py
import sqlite3
import datetime

class MemoryStore:
    def __init__(self, db_file='memory.db'):
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT, type TEXT, intent TEXT,
            extracted TEXT, timestamp TEXT
        )
        ''')

    def log(self, source, filetype, intent, extracted):
        self.conn.execute('''
        INSERT INTO memory (source, type, intent, extracted, timestamp)
        VALUES (?, ?, ?, ?, ?)
        ''', (source, filetype, intent, str(extracted), datetime.datetime.now().isoformat()))
        self.conn.commit()

    def delete_log(self, log_id):
        self.conn.execute('DELETE FROM memory WHERE id = ?', (log_id,))
        self.conn.commit()

    def delete_all_logs(self):
        self.conn.execute('DELETE FROM memory')
        self.conn.commit()

    def fetch_logs(self, intent_filter=None, limit=5):
        if intent_filter and intent_filter != "All":
            cursor = self.conn.execute(
                "SELECT id, source, type, intent, extracted, timestamp FROM memory WHERE intent = ? ORDER BY id DESC LIMIT ?",
                (intent_filter, limit)
            )
        else:
            cursor = self.conn.execute(
                "SELECT id, source, type, intent, extracted, timestamp FROM memory ORDER BY id DESC LIMIT ?",
                (limit,)
            )
        return cursor.fetchall()

    def fetch_intents(self):
        cursor = self.conn.execute("SELECT DISTINCT intent FROM memory")
        return [row[0] for row in cursor.fetchall()]
