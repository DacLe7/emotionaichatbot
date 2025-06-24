#!/usr/bin/env python3
"""
Test Improved Emotion Detection
Kiểm tra logic cải thiện phân loại cảm xúc và intent detection
"""

import re
from typing import Dict, List, Tuple, Optional
from ImprovedEmotionDetector import ImprovedEmotionDetector

def test_improved_detection():
    """Test logic cải thiện"""
    detector = ImprovedEmotionDetector()
    
    test_cases = [
        # (message, expected_type, expected_value)
        ("ok", "intent", "agreement"),
        ("có", "intent", "agreement"),
        ("tiếp tục", "intent", "agreement"),
        ("không", "intent", "disagreement"),
        ("tạm biệt", "intent", "end"),
        ("bắt đầu lại", "intent", "restart"),
        ("thế tôi dùng sao", "intent", "question"),
        ("tôi vui", "emotion", "positive"),
        ("tôi buồn", "emotion", "negative"),
        ("tôi stress", "emotion", "negative"),
        ("bình thường", "emotion", "neutral"),
        ("không biết", "emotion", "neutral"),
        ("ok...", "intent", "agreement"),
        ("stre...", "emotion", "negative"),  # stress viết tắt
        ("....", "unknown", None),
        ("thế", "intent", "question"),
        ("vậy", "intent", "question"),
        ("tôi vui và muốn tiếp tục", "emotion", "positive"),  # emotion quan trọng hơn
        ("ok tôi buồn", "intent", "agreement"),  # intent quan trọng hơn
        ("không tôi không muốn", "intent", "disagreement"),
    ]
    
    print("🧪 Test Improved Emotion & Intent Detection")
    print("=" * 60)
    
    correct = 0
    total = len(test_cases)
    results = []
    
    for message, expected_type, expected_value in test_cases:
        result = detector.analyze_message(message)
        actual_type = result["type"]
        actual_intent = result["intent"]
        actual_emotion = result["emotion"]
        
        if expected_type == "intent":
            match = (actual_type == "intent" and actual_intent == expected_value)
        elif expected_type == "emotion":
            match = (actual_type == "emotion" and actual_emotion == expected_value)
        elif expected_type == "unknown":
            match = (actual_type == "unknown")
        else:
            match = False
        
        if match:
            status = "✅"
            correct += 1
        else:
            status = "❌"
        results.append((status, message, actual_type, actual_intent, actual_emotion, expected_type, expected_value, result))
    
    # In kết quả chi tiết sau khi chạy hết
    for status, message, actual_type, actual_intent, actual_emotion, expected_type, expected_value, result in results:
        print(f"{status} '{message}' -> type: {actual_type}, intent: {actual_intent}, emotion: {actual_emotion} (expected: {expected_type}, {expected_value})")
        print(f"   Intent: {result['intent']} ({result['intent_confidence']:.2f}) | Emotion: {result['emotion']} ({result['emotion_confidence']:.2f})")
        print()
    
    accuracy = (correct / total) * 100
    print(f"📊 Accuracy: {correct}/{total} ({accuracy:.1f}%)")
    
    if accuracy >= 90:
        print("✅ Test passed! Logic cải thiện hoạt động tốt.")
        return True
    else:
        print("❌ Test failed! Cần cải thiện thêm.")
        return False

def test_specific_cases():
    """Test các trường hợp cụ thể từ log"""
    detector = ImprovedEmotionDetector()
    
    print("\n🔍 Test Specific Cases from Logs")
    print("=" * 40)
    
    specific_cases = [
        ("ok...", "agreement"),
        ("thế tôi dùng sao...", "question"),
        ("....", "unknown"),
        ("stre...", "negative"),
        ("stress...", "negative"),
        ("có...", "agreement"),
    ]
    
    for message, expected_intent in specific_cases:
        result = detector.analyze_message(message)
        intent = result["intent"]
        
        if intent == expected_intent:
            status = "✅"
        else:
            status = "❌"
        
        print(f"{status} '{message}' -> {intent} (expected: {expected_intent})")

if __name__ == "__main__":
    # Test logic cải thiện
    success = test_improved_detection()
    
    if success:
        # Test các trường hợp cụ thể
        test_specific_cases()
        
        print("\n" + "=" * 60)
        print("✅ Logic cải thiện sẵn sàng để áp dụng vào dự án!")
    else:
        print("\n❌ Cần cải thiện logic trước khi áp dụng.") 