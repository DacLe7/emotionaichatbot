"""
Conversation State Machine - Quản lý luồng hội thoại chatbot
File này chứa logic chuyển đổi giữa các trạng thái hội thoại
"""

import re
import logging
from enum import Enum
from typing import Dict, List, Tuple, Optional

# Setup logger cho state machine
state_logger = logging.getLogger('emotionai.state_machine')

class ConversationState(Enum):
    """Các trạng thái hội thoại"""
    GREETING = "greeting"
    SMALL_TALK = "small_talk"
    EMOTION_DETECTED = "emotion_detected"
    UNKNOWN_CONTEXT = "unknown_context"
    ASK_FEELING = "ask_feeling"
    SUGGEST_FRAGRANCE = "suggest_fragrance"
    END_SESSION = "end_session"

class ConversationStateMachine:
    def __init__(self):
        # Từ khóa cảm xúc (có dấu và không dấu)
        self.emotion_keywords = {
            "positive": [
                "vui", "vui ve", "vui lắm", "vui lam", "hanh phuc", "hạnh phúc", "phấn khích", "phan khich", 
                "tự hào", "tu hao", "biết ơn", "biet on", "yêu đời", "yeu doi",
                "năng động", "nang dong", "tuyệt vời", "tuyet voi", "thích", "thich",
                "rất vui", "rat vui", "cực vui", "cuc vui", "siêu vui", "sieu vui"
            ],
            "negative": [
                "buồn", "buon", "buồn lắm", "buon lam", "mệt", "met", "chán", "chan", "lo lắng", "lo lang",
                "tức", "tuc", "hờn", "hon", "stress", "căng thẳng", "cang thang",
                "sợ hãi", "so hai", "cô đơn", "co don", "tuyệt vọng", "tuyet vong",
                "khó khăn", "kho khan", "mất mát", "mat mat", "rất buồn", "rat buon"
            ],
            "neutral": [
                "bình thường", "binh thuong", "ổn định", "on dinh", 
                "không biết", "khong biet", "không chắc", "khong chac",
                "bình yên", "binh yen", "tĩnh lặng", "tinh lang", "ok", "ổn", "on"
            ]
        }
        
        # Từ khóa đồng ý/từ chối
        self.agreement_keywords = ["có", "co", "ok", "okay", "muốn", "muon", "thích", "thich", "được", "duoc", "yes", "y", "tiếp tục", "tiep tuc"]
        self.disagreement_keywords = ["không", "khong", "no", "không muốn", "khong muon", "không thích", "khong thich"]
        
        # Từ khóa kết thúc
        self.end_keywords = ["tạm biệt", "tam biet", "bye", "goodbye", "kết thúc", "ket thuc", "thôi", "thoi"]
        
        # Khởi tạo state
        self.current_state = ConversationState.GREETING
        self.user_id = None
        self.detected_emotion = None
        self.confidence = 0.0
        
    def reset_conversation(self, user_id: str):
        """Reset cuộc trò chuyện cho user mới"""
        self.current_state = ConversationState.GREETING
        self.user_id = user_id
        self.detected_emotion = None
        self.confidence = 0.0
    
    def detect_emotion(self, message: str) -> Tuple[str, float]:
        """Phát hiện cảm xúc từ tin nhắn (tokenize, loại bỏ dấu câu, so khớp từ)"""
        message_lower = message.lower()
        # Loại bỏ dấu câu
        message_clean = re.sub(r'[^\w\s]', ' ', message_lower)
        tokens = message_clean.split()
        
        # Đếm từ khóa cho mỗi loại cảm xúc
        emotion_scores = {"positive": 0, "negative": 0, "neutral": 0}
        for emotion_type, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                # So khớp từng từ hoặc cụm từ
                keyword_tokens = keyword.split()
                if len(keyword_tokens) == 1:
                    if keyword in tokens:
                        emotion_scores[emotion_type] += 1
                else:
                    # So khớp cụm từ
                    if keyword in message_clean:
                        emotion_scores[emotion_type] += 1
        
        # Xác định cảm xúc chính
        max_score = max(emotion_scores.values())
        if max_score == 0:
            state_logger.debug(f"🔍 No emotion detected in: '{message[:50]}...'")
            return "neutral", 0.0
        
        # Tìm cảm xúc có điểm cao nhất
        detected_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = min(max_score / 3.0, 1.0)  # Normalize confidence
        
        state_logger.info(f"🎯 Emotion detected: '{message[:50]}...' -> {detected_emotion} (confidence: {confidence:.3f})")
        return detected_emotion, confidence
    
    def detect_agreement(self, message: str) -> bool:
        """Phát hiện user có đồng ý không"""
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.agreement_keywords)
    
    def detect_disagreement(self, message: str) -> bool:
        """Phát hiện user có từ chối không"""
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.disagreement_keywords)
    
    def detect_end_intent(self, message: str) -> bool:
        """Phát hiện user muốn kết thúc"""
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.end_keywords)
    
    def detect_restart_intent(self, message: str) -> bool:
        """Phát hiện user muốn bắt đầu lại"""
        message_lower = message.lower()
        restart_keywords = ["bắt đầu lại", "restart", "bắt đầu", "mới", "lại từ đầu"]
        return any(keyword in message_lower for keyword in restart_keywords)
    
    def process_message(self, message: str) -> Dict:
        """Xử lý tin nhắn và trả về phản hồi phù hợp"""
        
        previous_state = self.current_state.value
        state_logger.debug(f"🔄 Processing message: '{message[:50]}...' in state: {previous_state}")
        
        # Kiểm tra intent bắt đầu lại
        if self.detect_restart_intent(message):
            state_logger.info(f"🔄 Restart intent detected, resetting conversation for user: {self.user_id}")
            self.reset_conversation(self.user_id)
            return self._handle_greeting_state(message)
        
        # Kiểm tra intent kết thúc
        if self.detect_end_intent(message):
            state_logger.info(f"🔄 End intent detected, ending session for user: {self.user_id}")
            self.current_state = ConversationState.END_SESSION
            return self._get_end_response()
        
        # Xử lý theo state hiện tại
        if self.current_state == ConversationState.GREETING:
            result = self._handle_greeting_state(message)
        elif self.current_state == ConversationState.SMALL_TALK:
            result = self._handle_small_talk_state(message)
        elif self.current_state == ConversationState.EMOTION_DETECTED:
            result = self._handle_emotion_detected_state(message)
        elif self.current_state == ConversationState.UNKNOWN_CONTEXT:
            result = self._handle_unknown_context_state(message)
        elif self.current_state == ConversationState.ASK_FEELING:
            result = self._handle_ask_feeling_state(message)
        elif self.current_state == ConversationState.SUGGEST_FRAGRANCE:
            result = self._handle_suggest_fragrance_state(message)
        else:  # END_SESSION
            result = self._get_end_response()
        
        # Log state transition nếu có thay đổi
        if previous_state != self.current_state.value:
            state_logger.info(f"🔄 State transition: {previous_state} -> {self.current_state.value}")
        
        return result
    
    def _handle_greeting_state(self, message: str) -> Dict:
        """Xử lý state GREETING"""
        self.current_state = ConversationState.SMALL_TALK
        return {
            "response": "Chào bạn! Tôi là EmotionAI – chatbot gợi ý mùi nến theo cảm xúc 💜\n\nBạn có thể chia sẻ cảm xúc hiện tại của mình không?",
            "state": self.current_state.value,
            "suggestions": ["😊 Tôi vui", "😔 Tôi buồn", "😰 Tôi stress", "🤔 Không biết"]
        }
    
    def _handle_small_talk_state(self, message: str) -> Dict:
        """Xử lý state SMALL_TALK"""
        # Phát hiện cảm xúc
        emotion, confidence = self.detect_emotion(message)
        
        if confidence > 0.3:  # Có phát hiện cảm xúc rõ ràng
            self.detected_emotion = emotion
            self.confidence = confidence
            self.current_state = ConversationState.EMOTION_DETECTED
            return self._get_emotion_detected_response(emotion)
        else:
            # Không hiểu rõ, chuyển sang UNKNOWN_CONTEXT
            self.current_state = ConversationState.UNKNOWN_CONTEXT
            return {
                "response": "Xin lỗi, mình chưa rõ phần này 😅\n\nNhưng mình có thể tư vấn mùi nến phù hợp với cảm xúc của bạn.\nBạn có muốn thử không?",
                "state": self.current_state.value,
                "suggestions": ["Có", "Không", "🤔 Không biết"]
            }
    
    def _handle_emotion_detected_state(self, message: str) -> Dict:
        """Xử lý state EMOTION_DETECTED"""
        if self.detect_agreement(message):
            self.current_state = ConversationState.SUGGEST_FRAGRANCE
            return self._get_fragrance_suggestion()
        else:
            self.current_state = ConversationState.SMALL_TALK
            return {
                "response": "Không sao đâu! Bạn có thể chia sẻ bất cứ điều gì khác với mình 😊",
                "state": self.current_state.value,
                "suggestions": ["😊 Tôi vui", "😔 Tôi buồn", "😰 Tôi stress"]
            }
    
    def _handle_unknown_context_state(self, message: str) -> Dict:
        """Xử lý state UNKNOWN_CONTEXT"""
        if self.detect_agreement(message):
            self.current_state = ConversationState.ASK_FEELING
            return {
                "response": "Bạn có thể chia sẻ cảm xúc hiện tại của mình không?\nVí dụ: 'tôi đang stress', 'hôm nay rất vui'...",
                "state": self.current_state.value,
                "suggestions": ["😊 Tôi vui", "😔 Tôi buồn", "😰 Tôi stress", "🤔 Không biết"]
            }
        else:
            self.current_state = ConversationState.SMALL_TALK
            return {
                "response": "Không sao! Bạn có thể nói chuyện bình thường với mình 😊",
                "state": self.current_state.value,
                "suggestions": ["😊 Tôi vui", "😔 Tôi buồn", "😰 Tôi stress"]
            }
    
    def _handle_ask_feeling_state(self, message: str) -> Dict:
        """Xử lý state ASK_FEELING"""
        # Phát hiện cảm xúc
        emotion, confidence = self.detect_emotion(message)
        
        if confidence > 0.2:  # Có phát hiện cảm xúc
            self.detected_emotion = emotion
            self.confidence = confidence
            self.current_state = ConversationState.EMOTION_DETECTED
            return self._get_emotion_detected_response(emotion)
        else:
            self.current_state = ConversationState.SMALL_TALK
            return {
                "response": "Không sao! Bạn có thể chia sẻ khi nào cảm thấy thoải mái hơn 😊",
                "state": self.current_state.value,
                "suggestions": ["😊 Tôi vui", "😔 Tôi buồn", "😰 Tôi stress"]
            }
    
    def _handle_suggest_fragrance_state(self, message: str) -> Dict:
        """Xử lý state SUGGEST_FRAGRANCE"""
        if self.detect_agreement(message):
            self.current_state = ConversationState.ASK_FEELING
            return {
                "response": "Tuyệt! Bạn có thể chia sẻ cảm xúc khác hoặc muốn tư vấn thêm không?",
                "state": self.current_state.value,
                "suggestions": ["😊 Tôi vui", "😔 Tôi buồn", "😰 Tôi stress", "Tạm biệt"]
            }
        else:
            self.current_state = ConversationState.SMALL_TALK
            return {
                "response": "Không sao! Bạn có thể chia sẻ bất cứ điều gì khác với mình 😊",
                "state": self.current_state.value,
                "suggestions": ["😊 Tôi vui", "😔 Tôi buồn", "😰 Tôi stress"]
            }
    
    def _get_emotion_detected_response(self, emotion: str) -> Dict:
        """Tạo phản hồi khi phát hiện cảm xúc"""
        emotion_names = {
            "positive": "vui vẻ, tích cực",
            "negative": "buồn, tiêu cực", 
            "neutral": "bình thường, cân bằng"
        }
        
        return {
            "response": f"Cảm xúc bạn đang chia sẻ là {emotion_names.get(emotion, emotion)}, mình rất đồng cảm ❤️\n\nBạn có muốn mình gợi ý mùi nến phù hợp với cảm xúc đó không?",
            "state": self.current_state.value,
            "emotion": emotion,
            "confidence": self.confidence,
            "suggestions": ["Có", "Không", "Tạm biệt"]
        }
    
    def _get_fragrance_suggestion(self) -> Dict:
        """Tạo gợi ý nến thơm"""
        return {
            "response": "Mình sẽ gợi ý mùi nến phù hợp với cảm xúc của bạn! 🕯️",
            "state": self.current_state.value,
            "emotion": self.detected_emotion,
            "confidence": self.confidence,
            "suggestions": ["Tiếp tục", "Tạm biệt"]
        }
    
    def _get_end_response(self) -> Dict:
        """Tạo phản hồi kết thúc"""
        return {
            "response": "Cảm ơn bạn đã trò chuyện cùng EmotionAI.\nNếu cần thêm tư vấn, mình luôn sẵn sàng 🌿",
            "state": self.current_state.value,
            "suggestions": ["Bắt đầu lại"]
        }
    
    def get_current_state(self) -> str:
        """Lấy state hiện tại"""
        return self.current_state.value
    
    def get_detected_emotion(self) -> Tuple[str, float]:
        """Lấy cảm xúc đã phát hiện"""
        return self.detected_emotion, self.confidence

# Test function
def test_state_machine():
    """Test state machine"""
    machine = ConversationStateMachine()
    machine.reset_conversation("test_user")
    
    test_messages = [
        "xin chào",
        "tôi buồn",
        "có",
        "tiếp tục",
        "tôi vui",
        "có",
        "tạm biệt"
    ]
    
    print("🧪 Test State Machine")
    print("=" * 40)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. User: {message}")
        result = machine.process_message(message)
        print(f"   State: {result['state']}")
        print(f"   Bot: {result['response'][:50]}...")
        if 'emotion' in result:
            print(f"   Emotion: {result['emotion']} ({result['confidence']:.2f})")

if __name__ == "__main__":
    test_state_machine() 