"""
User Database Management - Quản lý thông tin người dùng và sở thích
File này chứa logic lưu trữ và truy xuất thông tin user profile
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class UserDatabase:
    def __init__(self, db_path: str = 'chatbot.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Khởi tạo database với các bảng cần thiết"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Bảng users - thông tin cơ bản
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                first_interaction DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_interaction DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_conversations INTEGER DEFAULT 0,
                favorite_emotion TEXT,
                favorite_fragrance TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Bảng user_preferences - sở thích nến thơm
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                emotion TEXT NOT NULL,
                fragrance_name TEXT NOT NULL,
                rating INTEGER DEFAULT 0,
                used_count INTEGER DEFAULT 1,
                last_used DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Bảng conversation_sessions - phiên trò chuyện
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                session_id TEXT NOT NULL,
                start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_time DATETIME,
                total_messages INTEGER DEFAULT 0,
                emotions_discussed TEXT,
                fragrances_suggested TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Cập nhật bảng conversations hiện có (nếu chưa có cột user_id)
        try:
            cursor.execute('ALTER TABLE conversations ADD COLUMN session_id TEXT')
        except sqlite3.OperationalError:
            pass  # Cột đã tồn tại
        
        conn.commit()
        conn.close()
    
    def get_or_create_user(self, user_id: str) -> Dict:
        """Lấy hoặc tạo user mới"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Kiểm tra user có tồn tại không
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        
        if user:
            # Cập nhật last_interaction
            cursor.execute('''
                UPDATE users 
                SET last_interaction = CURRENT_TIMESTAMP,
                    total_conversations = total_conversations + 1
                WHERE user_id = ?
            ''', (user_id,))
            
            user_data = {
                'id': user[0],
                'user_id': user[1],
                'first_interaction': user[2],
                'last_interaction': user[3],
                'total_conversations': user[4] + 1,
                'favorite_emotion': user[5],
                'favorite_fragrance': user[6],
                'created_at': user[7]
            }
        else:
            # Tạo user mới
            cursor.execute('''
                INSERT INTO users (user_id, first_interaction, last_interaction, total_conversations)
                VALUES (?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
            ''', (user_id,))
            
            user_data = {
                'user_id': user_id,
                'first_interaction': datetime.now().isoformat(),
                'last_interaction': datetime.now().isoformat(),
                'total_conversations': 1,
                'favorite_emotion': None,
                'favorite_fragrance': None,
                'created_at': datetime.now().isoformat()
            }
        
        conn.commit()
        conn.close()
        return user_data
    
    def save_user_preference(self, user_id: str, emotion: str, fragrance_name: str, rating: int = 0):
        """Lưu sở thích nến thơm của user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Kiểm tra preference đã tồn tại chưa
        cursor.execute('''
            SELECT id, used_count FROM user_preferences 
            WHERE user_id = ? AND emotion = ? AND fragrance_name = ?
        ''', (user_id, emotion, fragrance_name))
        
        existing = cursor.fetchone()
        
        if existing:
            # Cập nhật preference hiện có
            cursor.execute('''
                UPDATE user_preferences 
                SET used_count = used_count + 1,
                    last_used = CURRENT_TIMESTAMP,
                    rating = ?
                WHERE id = ?
            ''', (rating, existing[0]))
        else:
            # Tạo preference mới
            cursor.execute('''
                INSERT INTO user_preferences (user_id, emotion, fragrance_name, rating, used_count)
                VALUES (?, ?, ?, ?, 1)
            ''', (user_id, emotion, fragrance_name, rating))
        
        conn.commit()
        conn.close()
    
    def get_user_preferences(self, user_id: str) -> List[Dict]:
        """Lấy sở thích của user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT emotion, fragrance_name, rating, used_count, last_used
            FROM user_preferences 
            WHERE user_id = ?
            ORDER BY used_count DESC, last_used DESC
        ''', (user_id,))
        
        preferences = []
        for row in cursor.fetchall():
            preferences.append({
                'emotion': row[0],
                'fragrance_name': row[1],
                'rating': row[2],
                'used_count': row[3],
                'last_used': row[4]
            })
        
        conn.close()
        return preferences
    
    def get_favorite_emotion(self, user_id: str) -> Optional[str]:
        """Lấy cảm xúc yêu thích nhất của user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT emotion, COUNT(*) as count
            FROM user_preferences 
            WHERE user_id = ?
            GROUP BY emotion
            ORDER BY count DESC
            LIMIT 1
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def get_favorite_fragrance(self, user_id: str, emotion: str = None) -> Optional[str]:
        """Lấy nến thơm yêu thích nhất của user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if emotion:
            cursor.execute('''
                SELECT fragrance_name, used_count
                FROM user_preferences 
                WHERE user_id = ? AND emotion = ?
                ORDER BY used_count DESC, rating DESC
                LIMIT 1
            ''', (user_id, emotion))
        else:
            cursor.execute('''
                SELECT fragrance_name, used_count
                FROM user_preferences 
                WHERE user_id = ?
                ORDER BY used_count DESC, rating DESC
                LIMIT 1
            ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def create_session(self, user_id: str, session_id: str) -> str:
        """Tạo phiên trò chuyện mới"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversation_sessions (user_id, session_id, start_time)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (user_id, session_id))
        
        conn.commit()
        conn.close()
        return session_id
    
    def end_session(self, session_id: str, emotions_discussed: List[str] = None, fragrances_suggested: List[str] = None):
        """Kết thúc phiên trò chuyện"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Cập nhật session
        cursor.execute('''
            UPDATE conversation_sessions 
            SET end_time = CURRENT_TIMESTAMP,
                emotions_discussed = ?,
                fragrances_suggested = ?
            WHERE session_id = ?
        ''', (
            json.dumps(emotions_discussed) if emotions_discussed else None,
            json.dumps(fragrances_suggested) if fragrances_suggested else None,
            session_id
        ))
        
        conn.commit()
        conn.close()
    
    def get_user_stats(self, user_id: str) -> Dict:
        """Lấy thống kê của user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Thống kê cơ bản
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return {}
        
        # Thống kê preferences
        cursor.execute('''
            SELECT emotion, COUNT(*) as count
            FROM user_preferences 
            WHERE user_id = ?
            GROUP BY emotion
        ''', (user_id,))
        
        emotion_stats = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Thống kê sessions
        cursor.execute('''
            SELECT COUNT(*) as total_sessions,
                   AVG(total_messages) as avg_messages
            FROM conversation_sessions 
            WHERE user_id = ?
        ''', (user_id,))
        
        session_stats = cursor.fetchone()
        
        conn.close()
        
        return {
            'user_id': user_id,
            'first_interaction': user[2],
            'last_interaction': user[3],
            'total_conversations': user[4],
            'favorite_emotion': user[5],
            'favorite_fragrance': user[6],
            'emotion_stats': emotion_stats,
            'total_sessions': session_stats[0] if session_stats else 0,
            'avg_messages_per_session': session_stats[1] if session_stats and session_stats[1] else 0
        }
    
    def get_personalized_suggestion(self, user_id: str, emotion: str) -> Optional[str]:
        """Lấy gợi ý cá nhân hóa dựa trên lịch sử"""
        # Lấy nến thơm user đã dùng và thích cho cảm xúc này
        preferences = self.get_user_preferences(user_id)
        
        for pref in preferences:
            if pref['emotion'] == emotion and pref['rating'] >= 3:
                return pref['fragrance_name']
        
        return None

# Test function
def test_user_database():
    """Test user database functionality"""
    db = UserDatabase('test_chatbot.db')
    
    # Test user creation
    user_data = db.get_or_create_user("test_user_123")
    print(f"✅ Created user: {user_data['user_id']}")
    
    # Test preference saving
    db.save_user_preference("test_user_123", "positive", "Nến Hương Cam Quýt", 4)
    db.save_user_preference("test_user_123", "negative", "Nến Hương Oải Hương", 5)
    print("✅ Saved preferences")
    
    # Test getting preferences
    preferences = db.get_user_preferences("test_user_123")
    print(f"✅ User preferences: {len(preferences)} items")
    
    # Test getting favorites
    favorite_emotion = db.get_favorite_emotion("test_user_123")
    favorite_fragrance = db.get_favorite_fragrance("test_user_123", "positive")
    print(f"✅ Favorite emotion: {favorite_emotion}")
    print(f"✅ Favorite fragrance for positive: {favorite_fragrance}")
    
    # Test user stats
    stats = db.get_user_stats("test_user_123")
    print(f"✅ User stats: {stats['total_conversations']} conversations")

if __name__ == "__main__":
    test_user_database() 