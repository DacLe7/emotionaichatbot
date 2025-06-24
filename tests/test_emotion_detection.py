"""
Test Emotion Detection - Kiểm tra nhận diện cảm xúc với nhiều biến thể câu
"""
from conversation_state_machine import ConversationStateMachine

def test_emotion_detection():
    test_cases = [
        ("Tôi vui lắm", "positive"),
        ("Mình rất vui", "positive"),
        ("Cực kỳ buồn", "negative"),
        ("Hơi stress", "negative"),
        ("Tôi bình thường", "neutral"),
        ("Không biết", "neutral"),
        ("Tôi ổn", "neutral"),
        ("Tôi chán quá", "negative"),
        ("Tôi stress nhẹ", "negative"),
        ("Tôi hạnh phúc", "positive"),
        ("Tôi thích", "positive"),
        ("Tôi mệt", "negative"),
        ("Tôi buồn lắm", "negative"),
        ("Tôi rất buồn", "negative"),
        ("Tôi cực vui", "positive"),
        ("Tôi bình yên", "neutral"),
        ("Tôi không chắc", "neutral"),
        ("Tôi muốn", "neutral"),
        ("Tôi yêu đời", "positive"),
        ("Tôi tuyệt vọng", "negative")
    ]
    
    machine = ConversationStateMachine()
    print("🧪 Test Emotion Detection")
    print("=" * 40)
    for i, (text, expected) in enumerate(test_cases, 1):
        detected, conf = machine.detect_emotion(text)
        result = "✅" if detected == expected else "❌"
        print(f"{i:2d}. '{text}' => {detected} ({conf:.2f}) | Expected: {expected} {result}")

if __name__ == "__main__":
    test_emotion_detection() 