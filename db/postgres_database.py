import os
import psycopg2
from psycopg2.extras import RealDictCursor

class PostgresDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(os.environ["DATABASE_URL"], cursor_factory=RealDictCursor)
        self.ensure_tables()

    def ensure_tables(self):
        with self.conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS fragrances (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    emotion TEXT,
                    image_url TEXT
                );
            ''')
            self.conn.commit()

    def add_fragrance(self, name, description, emotion, image_url=None):
        with self.conn.cursor() as cur:
            cur.execute('''
                INSERT INTO fragrances (name, description, emotion, image_url)
                VALUES (%s, %s, %s, %s)
                RETURNING *;
            ''', (name, description, emotion, image_url))
            self.conn.commit()
            return cur.fetchone()

    def get_fragrances(self, emotion=None):
        with self.conn.cursor() as cur:
            if emotion:
                cur.execute('SELECT * FROM fragrances WHERE emotion = %s', (emotion,))
            else:
                cur.execute('SELECT * FROM fragrances')
            return cur.fetchall()

    def get_fragrance_by_id(self, fragrance_id):
        with self.conn.cursor() as cur:
            cur.execute('SELECT * FROM fragrances WHERE id = %s', (fragrance_id,))
            return cur.fetchone()

    def close(self):
        self.conn.close() 