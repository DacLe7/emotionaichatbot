#!/usr/bin/env python3
"""
Debug Emotion Detection
Kiểm tra chi tiết các trường hợp bị sai
"""

from ImprovedEmotionDetector import ImprovedEmotionDetector

def debug_specific_cases():
    """Debug các trường hợp cụ thể bị sai"""
    detector = ImprovedEmotionDetector()
    
    print("🔍 Debug Specific Cases")
    print("=" * 50)
    
    # Test "không biết"
    print("\n1. Testing 'không biết':")
    message = "không biết"
    intent, intent_conf = detector.detect_intent(message)
    emotion, emotion_conf = detector.detect_emotion(message)
    result = detector.analyze_message(message)
    print(f"   Message: '{message}'")
    print(f"   Intent: {intent} ({intent_conf:.2f})")
    print(f"   Emotion: {emotion} ({emotion_conf:.2f})")
    print(f"   Result: {result}")
    
    # Test "stre..."
    print("\n2. Testing 'stre...':")
    message = "stre..."
    intent, intent_conf = detector.detect_intent(message)
    emotion, emotion_conf = detector.detect_emotion(message)
    result = detector.analyze_message(message)
    print(f"   Message: '{message}'")
    print(f"   Intent: {intent} ({intent_conf:.2f})")
    print(f"   Emotion: {emotion} ({emotion_conf:.2f})")
    print(f"   Result: {result}")
    
    # Test "vậy"
    print("\n3. Testing 'vậy':")
    message = "vậy"
    intent, intent_conf = detector.detect_intent(message)
    emotion, emotion_conf = detector.detect_emotion(message)
    result = detector.analyze_message(message)
    print(f"   Message: '{message}'")
    print(f"   Intent: {intent} ({intent_conf:.2f})")
    print(f"   Emotion: {emotion} ({emotion_conf:.2f})")
    print(f"   Result: {result}")
    
    # Test "tôi vui và muốn tiếp tục"
    print("\n4. Testing 'tôi vui và muốn tiếp tục':")
    message = "tôi vui và muốn tiếp tục"
    intent, intent_conf = detector.detect_intent(message)
    emotion, emotion_conf = detector.detect_emotion(message)
    result = detector.analyze_message(message)
    print(f"   Message: '{message}'")
    print(f"   Intent: {intent} ({intent_conf:.2f})")
    print(f"   Emotion: {emotion} ({emotion_conf:.2f})")
    print(f"   Result: {result}")
    
    # Test "tôi vui"
    print("\n5. Testing 'tôi vui':")
    message = "tôi vui"
    intent, intent_conf = detector.detect_intent(message)
    emotion, emotion_conf = detector.detect_emotion(message)
    result = detector.analyze_message(message)
    print(f"   Message: '{message}'")
    print(f"   Intent: {intent} ({intent_conf:.2f})")
    print(f"   Emotion: {emotion} ({emotion_conf:.2f})")
    print(f"   Result: {result}")
    
    # Test "tôi buồn"
    print("\n6. Testing 'tôi buồn':")
    message = "tôi buồn"
    intent, intent_conf = detector.detect_intent(message)
    emotion, emotion_conf = detector.detect_emotion(message)
    result = detector.analyze_message(message)
    print(f"   Message: '{message}'")
    print(f"   Intent: {intent} ({intent_conf:.2f})")
    print(f"   Emotion: {emotion} ({emotion_conf:.2f})")
    print(f"   Result: {result}")
    
    # Test "tôi stress"
    print("\n7. Testing 'tôi stress':")
    message = "tôi stress"
    intent, intent_conf = detector.detect_intent(message)
    emotion, emotion_conf = detector.detect_emotion(message)
    result = detector.analyze_message(message)
    print(f"   Message: '{message}'")
    print(f"   Intent: {intent} ({intent_conf:.2f})")
    print(f"   Emotion: {emotion} ({emotion_conf:.2f})")
    print(f"   Result: {result}")

if __name__ == "__main__":
    debug_specific_cases() 