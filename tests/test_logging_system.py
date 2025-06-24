#!/usr/bin/env python3
"""
Test Logging System
Kiểm tra hệ thống logging hoạt động đúng
"""

import requests
import time
import os
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
TEST_USER_ID = "test_user_logging"

def test_logging_system():
    """Test toàn bộ logging system"""
    print("🧪 Test Logging System")
    print("=" * 50)
    
    # Test 1: Kiểm tra log file được tạo
    print("\n1. Kiểm tra log file...")
    if os.path.exists('logs/emotionai.log'):
        print("✅ Log file đã được tạo: logs/emotionai.log")
        
        # Đọc log file
        with open('logs/emotionai.log', 'r', encoding='utf-8') as f:
            log_content = f.read()
            log_lines = log_content.split('\n')
            print(f"✅ Log file có {len(log_lines)} dòng")
            
            # Kiểm tra các log entry quan trọng
            if "🚀 EmotionAI Chatbot khởi động thành công" in log_content:
                print("✅ Startup log entry found")
            else:
                print("❌ Startup log entry not found")
    else:
        print("❌ Log file chưa được tạo")
    
    # Test 2: Test API calls và logging
    print("\n2. Test API calls và logging...")
    
    # Gửi một số API calls
    test_messages = [
        "xin chào",
        "tôi buồn lắm",
        "có",
        "tiếp tục",
        "tôi vui",
        "có",
        "tạm biệt"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"   {i}. Sending: '{message}'")
        response = requests.post(f"{BASE_URL}/api/chat", json={
            "message": message,
            "user_id": TEST_USER_ID
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"      ✅ Response: {data['state']}")
        else:
            print(f"      ❌ Error: {response.status_code}")
        
        time.sleep(0.5)  # Delay nhỏ để log được ghi
    
    # Test 3: Test analytics API
    print("\n3. Test analytics API...")
    response = requests.get(f"{BASE_URL}/api/analytics")
    if response.status_code == 200:
        print("✅ Analytics API working")
    else:
        print(f"❌ Analytics API error: {response.status_code}")
    
    # Test 4: Test user preferences API
    print("\n4. Test user preferences API...")
    response = requests.get(f"{BASE_URL}/api/user/{TEST_USER_ID}/preferences")
    if response.status_code == 200:
        print("✅ User preferences API working")
    else:
        print(f"❌ User preferences API error: {response.status_code}")
    
    # Test 5: Kiểm tra log entries mới
    print("\n5. Kiểm tra log entries mới...")
    time.sleep(1)  # Đợi log được ghi
    
    if os.path.exists('logs/emotionai.log'):
        with open('logs/emotionai.log', 'r', encoding='utf-8') as f:
            log_content = f.read()
            
            # Đếm các loại log entries
            api_calls = log_content.count("💬 API call")
            state_transitions = log_content.count("🔄 State transition")
            emotion_detected = log_content.count("🎯 Emotion detected")
            fragrance_suggested = log_content.count("🕯️ Fragrance suggested")
            
            print(f"✅ API calls logged: {api_calls}")
            print(f"✅ State transitions logged: {state_transitions}")
            print(f"✅ Emotions detected logged: {emotion_detected}")
            print(f"✅ Fragrances suggested logged: {fragrance_suggested}")
            
            # Hiển thị một số log entries mẫu
            print("\n📋 Sample log entries:")
            lines = log_content.split('\n')
            recent_lines = [line for line in lines[-20:] if line.strip()]
            for line in recent_lines[-5:]:
                print(f"   {line}")
    
    print("\n" + "=" * 50)
    print("✅ Logging system test hoàn thành!")

def test_error_logging():
    """Test error logging"""
    print("\n🧪 Test Error Logging")
    print("=" * 30)
    
    # Test 1: Empty message
    print("\n1. Test empty message...")
    response = requests.post(f"{BASE_URL}/api/chat", json={
        "message": "",
        "user_id": TEST_USER_ID
    })
    
    if response.status_code == 400:
        print("✅ Empty message error handled correctly")
    else:
        print(f"❌ Unexpected response: {response.status_code}")
    
    # Test 2: Invalid JSON
    print("\n2. Test invalid JSON...")
    try:
        response = requests.post(f"{BASE_URL}/api/chat", data="invalid json")
        print(f"✅ Invalid JSON handled: {response.status_code}")
    except Exception as e:
        print(f"✅ Exception caught: {type(e).__name__}")
    
    print("\n" + "=" * 30)
    print("✅ Error logging test hoàn thành!")

if __name__ == "__main__":
    try:
        # Test logging system
        test_logging_system()
        
        # Test error logging
        test_error_logging()
        
    except requests.exceptions.ConnectionError:
        print("❌ Không thể kết nối đến server. Hãy đảm bảo app đang chạy.")
    except Exception as e:
        print(f"❌ Lỗi: {e}") 