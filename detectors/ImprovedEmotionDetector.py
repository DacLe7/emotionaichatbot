import re
from typing import Dict, Tuple

def simple_fuzzy_match(word: str, text: str, max_dist: int = 1) -> bool:
    """Fuzzy match đơn giản: cho phép sai lệch 1 ký tự cho từ ngắn, hoặc match đầu từ cho từ dài."""
    word = word.lower()
    text = text.lower()
    if word in text:
        return True
    # Fuzzy: cho phép thiếu 1 ký tự ở cuối hoặc đầu (cho từ >=4 ký tự)
    if len(word) >= 4:
        if word[:-1] in text or word[1:] in text:
            return True
    # Fuzzy: cho phép sai 1 ký tự (Levenshtein distance = 1)
    if len(word) >= 4:
        for i in range(len(word)):
            w = word[:i] + word[i+1:]
            if w in text:
                return True
    # Fuzzy: cho phép thiếu ký tự cuối (ví dụ: "stre..." -> "stress")
    if len(word) >= 3:
        if word in text or text.startswith(word):
            return True
    return False

class ImprovedEmotionDetector:
    def __init__(self):
        # Từ khóa cảm xúc (cải thiện với nhiều biến thể hơn)
        self.emotion_keywords = {
            "positive": [
                "vui", "vui ve", "vui lam", "hanh phuc", "hạnh phúc", "phấn khích", "tu hao", "biết ơn", "yêu đời",
                "năng động", "tuyệt vời", "thích", "rất vui", "cực vui", "siêu vui", "sung sướng", "thỏa mãn",
                "tốt", "hay", "đẹp", "thú vị", "tuyệt", "hoàn hảo", "xuất sắc", "ấn tượng"
            ],
            "negative": [
                "buồn", "buon", "mệt", "chán", "lo lắng", "tức", "hờn", "stress", "căng thẳng", "sợ hãi", "cô đơn", "tuyệt vọng",
                "khó khăn", "mất mát", "rất buồn", "xấu", "tệ", "khó chịu", "bực mình", "vất vả", "mệt mỏi",
                "bồn chồn", "hồi hộp", "sợ"
            ],
            "neutral": [
                "bình thường", "ổn định", "không biết", "không chắc", "bình yên", "tĩnh lặng", "ổn", "tạm được", "không sao"
            ]
        }
        
        # Từ khóa intent (tách riêng khỏi emotion, cải thiện)
        self.intent_keywords = {
            "agreement": [
                "có", "co", "được", "duoc", "ok", "okay", "yes", "y", "tiếp tục", "tiep tuc",
                "muốn", "muon", "thích", "thich", "đồng ý", "dong y", "tán thành", "tan thanh",
                "chắc chắn", "chac chan", "tất nhiên", "tat nhien", "dĩ nhiên", "di nhien"
            ],
            "disagreement": [
                "không", "khong", "no", "không muốn", "khong muon", "không thích", "khong thich",
                "không đồng ý", "khong dong y", "không phải", "khong phai", "không phải vậy", "khong phai vay",
                "không đúng", "khong dung", "sai rồi", "sai roi", "không phải thế", "khong phai the"
            ],
            "end": [
                "tạm biệt", "tam biet", "bye", "goodbye", "kết thúc", "ket thuc", "thôi", "thoi",
                "dừng lại", "dung lai", "ngừng", "ngung", "kết thúc", "ket thuc", "chấm dứt", "cham dut"
            ],
            "restart": [
                "bắt đầu lại", "bat dau lai", "restart", "bắt đầu", "bat dau", "mới", "moi", "lại từ đầu", "lai tu dau",
                "làm lại", "lam lai", "thử lại", "thu lai", "bắt đầu mới", "bat dau moi"
            ],
            "question": [
                "gì", "gi", "sao", "thế nào", "the nao", "làm sao", "lam sao", "cách", "cach",
                "thế", "the", "vậy", "vay", "sao vậy", "sao vay", "tại sao", "tai sao",
                "như thế nào", "nhu the nao", "làm thế nào", "lam the nao"
            ]
        }
    
    def detect_intent(self, message: str) -> Tuple[str, float]:
        """Phát hiện intent của tin nhắn (tách riêng khỏi emotion)"""
        message_lower = message.lower()
        message_clean = re.sub(r'[^\w\s]', ' ', message_lower)
        
        # Xử lý trường hợp đặc biệt
        if "không biết" in message_clean:
            return "none", 0.0  # Không phải intent, mà là neutral emotion
        
        # Xử lý "vậy" - ưu tiên question thay vì agreement
        if message_clean.strip() == "vậy":
            return "question", 0.5
        
        # Xử lý câu bắt đầu bằng "tôi" - không phải intent end
        if message_clean.strip().startswith("tôi"):
            # Kiểm tra xem có từ khóa intent khác không
            intent_scores = {}
            for intent_type, keywords in self.intent_keywords.items():
                score = 0
                for keyword in keywords:
                    if simple_fuzzy_match(keyword, message_clean):
                        score += 1
                intent_scores[intent_type] = score
            
            max_score = max(intent_scores.values())
            if max_score == 0:
                return "none", 0.0
            
            detected_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(max_score / 2.0, 1.0)
            return detected_intent, confidence
        
        intent_scores = {}
        for intent_type, keywords in self.intent_keywords.items():
            score = 0
            for keyword in keywords:
                if simple_fuzzy_match(keyword, message_clean):
                    # Loại trừ trường hợp "tôi" khớp với "thôi"
                    if keyword in ["thôi", "thoi"] and "tôi" in message_clean:
                        continue
                    score += 1
            intent_scores[intent_type] = score
        
        max_score = max(intent_scores.values())
        if max_score == 0:
            return "none", 0.0
        
        detected_intent = max(intent_scores, key=intent_scores.get)
        confidence = min(max_score / 2.0, 1.0)
        
        return detected_intent, confidence
    
    def detect_emotion(self, message: str) -> Tuple[str, float]:
        """Phát hiện cảm xúc từ tin nhắn (cải thiện)"""
        message_lower = message.lower()
        message_clean = re.sub(r'[^\w\s]', ' ', message_lower)
        tokens = message_clean.split()
        
        # Xử lý trường hợp đặc biệt
        if "stre" in message_clean or message_clean.startswith("stre"):
            return "negative", 0.5  # "stre..." -> stress -> negative
        
        # Xử lý "không biết" - ưu tiên neutral
        if "không biết" in message_clean:
            return "neutral", 0.5
        
        # Đếm từ khóa cho mỗi loại cảm xúc
        emotion_scores = {"positive": 0, "negative": 0, "neutral": 0}
        
        for emotion_type, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if simple_fuzzy_match(keyword, message_clean):
                    emotion_scores[emotion_type] += 1
        
        # Xác định cảm xúc chính
        max_score = max(emotion_scores.values())
        if max_score == 0:
            return "neutral", 0.0
        
        detected_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = min(max_score / 3.0, 1.0)
        
        return detected_emotion, confidence
    
    def analyze_message(self, message: str) -> Dict:
        """Phân tích toàn diện tin nhắn: intent + emotion"""
        intent, intent_confidence = self.detect_intent(message)
        emotion, emotion_confidence = self.detect_emotion(message)
        
        # Logic ưu tiên cải thiện
        # Ưu tiên emotion khi câu bắt đầu bằng "tôi" và có emotion rõ ràng
        if message.lower().strip().startswith("tôi") and emotion_confidence > 0.3:
            return {
                "type": "emotion",
                "emotion": emotion,
                "confidence": emotion_confidence,
                "intent": intent,
                "intent_confidence": intent_confidence,
                "emotion_confidence": emotion_confidence
            }
        
        # Nếu có cả intent và emotion rõ ràng, ưu tiên intent cho các trường hợp đặc biệt
        if intent_confidence > 0.3 and intent in ["restart", "disagreement", "agreement"]:
            # Nếu câu có cả emotion rõ ràng và intent agreement, ưu tiên emotion
            if intent == "agreement" and emotion_confidence > 0.3 and "vui" in message.lower():
                return {
                    "type": "emotion",
                    "emotion": emotion,
                    "confidence": emotion_confidence,
                    "intent": intent,
                    "intent_confidence": intent_confidence,
                    "emotion_confidence": emotion_confidence
                }
            return {
                "type": "intent",
                "intent": intent,
                "confidence": intent_confidence,
                "emotion": emotion,
                "emotion_confidence": emotion_confidence,
                "intent_confidence": intent_confidence
            }
        elif intent_confidence > 0.3 and intent == "question":
            # Ưu tiên question intent
            return {
                "type": "intent",
                "intent": intent,
                "confidence": intent_confidence,
                "emotion": emotion,
                "emotion_confidence": emotion_confidence,
                "intent_confidence": intent_confidence
            }
        elif intent_confidence > 0.3 and intent == "end":
            # Chỉ ưu tiên end khi không có emotion rõ ràng
            if emotion_confidence < 0.3:
                return {
                    "type": "intent",
                    "intent": intent,
                    "confidence": intent_confidence,
                    "emotion": emotion,
                    "emotion_confidence": emotion_confidence,
                    "intent_confidence": intent_confidence
                }
        elif emotion_confidence > 0.3:
            return {
                "type": "emotion",
                "emotion": emotion,
                "confidence": emotion_confidence,
                "intent": intent,
                "intent_confidence": intent_confidence,
                "emotion_confidence": emotion_confidence
            }
        
        # Default case: unknown
        return {
            "type": "unknown",
            "intent": intent,
            "intent_confidence": intent_confidence,
            "emotion": emotion,
            "emotion_confidence": emotion_confidence
        } 