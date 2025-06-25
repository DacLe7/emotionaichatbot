from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import json
import logging
import os
from datetime import datetime
from textblob import TextBlob
import nltk
import uuid
from dotenv import load_dotenv
from utils.fragrance_mapping import FragranceMapper
from state_machine.conversation_state_machine import ConversationStateMachine
from db.user_database import UserDatabase
from db.postgres_database import PostgresDatabase

# Load environment variables from .env file
load_dotenv()

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Setup logging
def setup_logging():
    """Thiết lập hệ thống logging"""
    # Tạo thư mục logs nếu chưa có
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Cấu hình logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # Log ra file
            logging.FileHandler('logs/emotionai.log', encoding='utf-8'),
            # Log ra console
            logging.StreamHandler()
        ]
    )
    
    # Tạo logger cho từng module
    app_logger = logging.getLogger('emotionai.app')
    api_logger = logging.getLogger('emotionai.api')
    state_logger = logging.getLogger('emotionai.state_machine')
    db_logger = logging.getLogger('emotionai.database')
    
    return app_logger, api_logger, state_logger, db_logger

# Khởi tạo logging
app_logger, api_logger, state_logger, db_logger = setup_logging()

app = Flask(__name__, template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')))
CORS(app)

# Initialize components
fragrance_db = PostgresDatabase()
user_db = UserDatabase()

# Store active conversations (in production, use Redis or database)
active_conversations = {}

# Database initialization
def init_db():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            session_id TEXT,
            message TEXT,
            response TEXT,
            sentiment TEXT,
            confidence REAL,
            fragrance_recommendation TEXT,
            conversation_state TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

app_logger.info("🚀 EmotionAI Chatbot khởi động thành công")

def get_or_create_conversation(user_id: str):
    """Lấy hoặc tạo conversation mới cho user"""
    if user_id not in active_conversations:
        # Tạo session mới
        session_id = str(uuid.uuid4())
        user_db.create_session(user_id, session_id)
        
        # Tạo state machine mới
        state_machine = ConversationStateMachine()
        state_machine.reset_conversation(user_id)
        
        active_conversations[user_id] = {
            'session_id': session_id,
            'state_machine': state_machine,
            'emotions_discussed': [],
            'fragrances_suggested': []
        }
        
        app_logger.info(f"🆕 Tạo conversation mới cho user: {user_id}, session: {session_id}")
    else:
        app_logger.debug(f"📝 Sử dụng conversation hiện có cho user: {user_id}")
    
    return active_conversations[user_id]

def analyze_sentiment(text):
    """Phân tích cảm xúc của văn bản"""
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            sentiment = "positive"
            confidence = abs(polarity)
        elif polarity < -0.1:
            sentiment = "negative"
            confidence = abs(polarity)
        else:
            sentiment = "neutral"
            confidence = 1 - abs(polarity)
        
        app_logger.debug(f"🔍 TextBlob analysis: '{text[:50]}...' -> {sentiment} ({confidence:.3f})")
        return sentiment, confidence
        
    except Exception as e:
        app_logger.error(f"❌ Lỗi phân tích sentiment: {e}")
        return "neutral", 0.0

def get_fragrance_recommendation(sentiment, confidence, user_id=None):
    """Lấy gợi ý nến thơm dựa trên cảm xúc và lịch sử user"""
    # Kiểm tra gợi ý cá nhân hóa trước
    if user_id:
        personalized_fragrance = user_db.get_personalized_suggestion(user_id, sentiment)
        if personalized_fragrance:
            emotion_fragrances = fragrance_db.get_fragrances(sentiment)
            for fragrance in emotion_fragrances:
                if isinstance(fragrance, dict) and fragrance.get('name') == personalized_fragrance:
                    return {
                        'fragrance': fragrance,
                        'emotion_name': sentiment,
                        'reason': f"Bạn đã thích mùi này trước đó cho cảm xúc {sentiment}",
                        'personalized': True
                    }
    # Nếu không có gợi ý cá nhân hóa, dùng logic mặc định
    emotion_fragrances = fragrance_db.get_fragrances(sentiment)
    import random
    if emotion_fragrances:
        selected_fragrance = random.choice(emotion_fragrances)
        return {
            'fragrance': selected_fragrance,
            'emotion_name': sentiment,
            'reason': f"Gợi ý dựa trên cảm xúc {sentiment}",
            'personalized': False
        }
    else:
        return None

def save_conversation(user_id, session_id, message, response, sentiment, confidence, fragrance_rec=None, conversation_state=None):
    """Lưu cuộc trò chuyện vào database"""
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    
    # Convert fragrance recommendation to JSON string if it exists
    fragrance_json = json.dumps(fragrance_rec) if fragrance_rec else None
    
    cursor.execute('''
        INSERT INTO conversations (user_id, session_id, message, response, sentiment, confidence, fragrance_recommendation, conversation_state)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, session_id, message, response, sentiment, confidence, fragrance_json, conversation_state))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        user_id = data.get('user_id', 'anonymous')
        
        api_logger.info(f"💬 API call - User: {user_id}, Message: '{message[:50]}...'")
        
        if not message.strip():
            api_logger.warning(f"⚠️ Empty message from user: {user_id}")
            return jsonify({'error': 'Tin nhắn không được để trống'}), 400
        
        # Lấy hoặc tạo conversation cho user
        conversation = get_or_create_conversation(user_id)
        state_machine = conversation['state_machine']
        session_id = conversation['session_id']
        
        # Log state trước khi xử lý
        previous_state = state_machine.get_current_state()
        api_logger.debug(f"🔄 State transition - User: {user_id}, From: {previous_state}")
        
        # Xử lý tin nhắn qua state machine
        state_response = state_machine.process_message(message)
        bot_response = state_response['response']
        current_state = state_response['state']
        suggestions = state_response.get('suggestions', [])
        
        # Log state transition
        if previous_state != current_state:
            api_logger.info(f"🔄 State changed - User: {user_id}, {previous_state} -> {current_state}")
        
        # Phân tích cảm xúc (backup cho state machine)
        sentiment, confidence = analyze_sentiment(message)
        
        # Lấy emotion từ state machine nếu có
        detected_emotion, emotion_confidence = state_machine.get_detected_emotion()
        if detected_emotion:
            sentiment = detected_emotion
            confidence = emotion_confidence
            api_logger.info(f"🎯 Emotion detected - User: {user_id}, Emotion: {sentiment}, Confidence: {confidence:.3f}")
        
        # Lấy gợi ý nến thơm nếu user đồng ý nhận gợi ý
        fragrance_recommendation = None
        if current_state == 'suggest_fragrance' and detected_emotion:
            fragrance_recommendation = get_fragrance_recommendation(detected_emotion, emotion_confidence, user_id)
            
            # Lưu preference nếu có gợi ý nến thơm
            if fragrance_recommendation and detected_emotion:
                fragrance_name = fragrance_recommendation['fragrance']['name']
                user_db.save_user_preference(user_id, detected_emotion, fragrance_name)
                conversation['fragrances_suggested'].append(fragrance_name)
                
                api_logger.info(f"🕯️ Fragrance suggested - User: {user_id}, Emotion: {detected_emotion}, Fragrance: {fragrance_name}")
        
        # Cập nhật danh sách emotions discussed
        if 'emotion' in state_response:
            conversation['emotions_discussed'].append(state_response['emotion'])
        
        # Lưu vào database
        save_conversation(
            user_id, session_id, message, bot_response, 
            sentiment, confidence, fragrance_recommendation, current_state
        )
        
        # Chuẩn bị response
        response_data = {
            'response': bot_response,
            'state': current_state,
            'suggestions': suggestions,
            'sentiment': sentiment,
            'confidence': round(confidence, 3),
            'timestamp': datetime.now().isoformat()
        }
        
        # Thêm fragrance recommendation nếu có
        if fragrance_recommendation:
            response_data['fragrance_recommendation'] = fragrance_recommendation
        
        # Thêm thông tin user nếu là user mới
        if current_state == 'greeting':
            user_data = user_db.get_or_create_user(user_id)
            response_data['user_info'] = {
                'is_new_user': user_data['total_conversations'] == 1,
                'total_conversations': user_data['total_conversations']
            }
        
        api_logger.info(f"✅ API response - User: {user_id}, State: {current_state}, Sentiment: {sentiment}")
        return jsonify(response_data)
        
    except Exception as e:
        api_logger.error(f"❌ API error - User: {user_id}, Error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Lấy thống kê cảm xúc"""
    try:
        api_logger.info("📊 Analytics request received")
        
        conn = sqlite3.connect('chatbot.db')
        cursor = conn.cursor()
        
        # Thống kê tổng quan
        cursor.execute('SELECT COUNT(*) FROM conversations')
        total_messages = cursor.fetchone()[0]
        
        # Thống kê theo cảm xúc
        cursor.execute('''
            SELECT sentiment, COUNT(*) as count, AVG(confidence) as avg_confidence
            FROM conversations 
            GROUP BY sentiment
        ''')
        sentiment_stats = cursor.fetchall()
        
        # Tin nhắn gần đây với gợi ý nến thơm
        cursor.execute('''
            SELECT message, sentiment, confidence, fragrance_recommendation, timestamp
            FROM conversations 
            ORDER BY timestamp DESC 
            LIMIT 10
        ''')
        recent_messages = cursor.fetchall()
        
        conn.close()
        
        # Process recent messages to include fragrance data
        processed_recent_messages = []
        for row in recent_messages:
            fragrance_data = json.loads(row[3]) if row[3] else None
            processed_recent_messages.append({
                'message': row[0],
                'sentiment': row[1],
                'confidence': round(row[2], 3),
                'fragrance': fragrance_data['fragrance']['name'] if fragrance_data else None,
                'timestamp': row[4]
            })
        
        api_logger.info(f"📊 Analytics response - Total messages: {total_messages}, Sentiment types: {len(sentiment_stats)}")
        return jsonify({
            'total_messages': total_messages,
            'sentiment_stats': [
                {
                    'sentiment': row[0],
                    'count': row[1],
                    'avg_confidence': round(row[2], 3)
                } for row in sentiment_stats
            ],
            'recent_messages': processed_recent_messages
        })
        
    except Exception as e:
        api_logger.error(f"❌ Analytics error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/<user_id>/stats', methods=['GET'])
def get_user_stats(user_id):
    """Lấy thống kê của user cụ thể"""
    try:
        api_logger.info(f"👤 User stats request - User: {user_id}")
        stats = user_db.get_user_stats(user_id)
        api_logger.info(f"✅ User stats response - User: {user_id}, Conversations: {stats.get('total_conversations', 0)}")
        return jsonify(stats)
    except Exception as e:
        api_logger.error(f"❌ User stats error - User: {user_id}, Error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/<user_id>/preferences', methods=['GET'])
def get_user_preferences(user_id):
    """Lấy sở thích của user"""
    try:
        api_logger.info(f"💝 User preferences request - User: {user_id}")
        preferences = user_db.get_user_preferences(user_id)
        api_logger.info(f"✅ User preferences response - User: {user_id}, Preferences: {len(preferences)}")
        return jsonify({'preferences': preferences})
    except Exception as e:
        api_logger.error(f"❌ User preferences error - User: {user_id}, Error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/fragrances', methods=['GET'])
def get_fragrances():
    """Lấy tất cả thông tin nến thơm"""
    try:
        all_fragrances = fragrance_db.get_fragrances()
        return jsonify({'fragrances': all_fragrances})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fragrance/<emotion>', methods=['GET'])
def get_fragrance_by_emotion(emotion):
    """Lấy gợi ý nến thơm cho cảm xúc cụ thể"""
    try:
        confidence = float(request.args.get('confidence', 0.5))
        user_id = request.args.get('user_id')
        
        recommendation = get_fragrance_recommendation(emotion, confidence, user_id)
        return jsonify(recommendation)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversation/end', methods=['POST'])
def end_conversation():
    """Kết thúc cuộc trò chuyện"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if user_id in active_conversations:
            conversation = active_conversations[user_id]
            session_id = conversation['session_id']
            
            # Kết thúc session
            user_db.end_session(
                session_id,
                conversation['emotions_discussed'],
                conversation['fragrances_suggested']
            )
            
            # Xóa khỏi active conversations
            del active_conversations[user_id]
            
            return jsonify({'message': 'Conversation ended successfully'})
        else:
            return jsonify({'error': 'No active conversation found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Lấy log entries gần đây"""
    try:
        api_logger.debug("📋 Logs request received")
        
        # Đọc log file
        log_file_path = 'logs/emotionai.log'
        if not os.path.exists(log_file_path):
            return jsonify({'logs': [], 'message': 'Log file not found'})
        
        with open(log_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Parse log entries (lấy 20 entries gần nhất)
        log_entries = []
        for line in lines[-20:]:  # Lấy 20 dòng cuối
            line = line.strip()
            if line:
                # Parse log format: timestamp - logger - level - message
                try:
                    parts = line.split(' - ', 3)
                    if len(parts) >= 4:
                        timestamp, logger, level, message = parts
                        log_entries.append({
                            'timestamp': timestamp,
                            'logger': logger,
                            'level': level,
                            'message': message
                        })
                except Exception as e:
                    # Nếu không parse được, thêm nguyên dòng
                    log_entries.append({
                        'timestamp': datetime.now().isoformat(),
                        'logger': 'unknown',
                        'level': 'INFO',
                        'message': line
                    })
        
        # Đảo ngược để hiển thị mới nhất trước
        log_entries.reverse()
        
        api_logger.debug(f"📋 Returning {len(log_entries)} log entries")
        return jsonify({'logs': log_entries})
        
    except Exception as e:
        api_logger.error(f"❌ Error reading logs: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/fragrance/add', methods=['POST'])
def add_fragrance():
    """Thêm fragrance mới vào database (admin)"""
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        emotion = data.get('emotion')
        image_url = data.get('image_url')
        if not all([name, emotion]):
            return jsonify({'error': 'Thiếu tên hoặc cảm xúc'}), 400
        new_fragrance = fragrance_db.add_fragrance(name, description, emotion, image_url)
        return jsonify({'fragrance': new_fragrance}), 201
    except Exception as e:
        import traceback
        api_logger.error(f"❌ Error in add_fragrance: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 