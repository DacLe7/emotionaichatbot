#!/usr/bin/env python3
"""
Test Full Personalization Flow
Kiểm tra toàn bộ luồng personalization từ emotion detection đến fragrance suggestion
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
TEST_USER_ID = "test_user_full_flow"

def test_full_personalization_flow():
    """Test toàn bộ flow personalization"""
    print("🧪 Test Full Personalization Flow")
    print("=" * 50)
    
    # Test 1: Bắt đầu conversation mới
    print("\n1. Bắt đầu conversation mới...")
    response = requests.post(f"{BASE_URL}/api/chat", json={
        "message": "xin chào",
        "user_id": TEST_USER_ID
    })
    
    if response.status_code != 200:
        print(f"❌ Lỗi: {response.status_code}")
        return
    
    data = response.json()
    print(f"✅ State: {data['state']}")
    print(f"✅ Response: {data['response'][:100]}...")
    
    # Test 2: Chia sẻ cảm xúc positive
    print("\n2. Chia sẻ cảm xúc positive...")
    response = requests.post(f"{BASE_URL}/api/chat", json={
        "message": "tôi rất vui hôm nay",
        "user_id": TEST_USER_ID
    })
    
    if response.status_code != 200:
        print(f"❌ Lỗi: {response.status_code}")
        return
    
    data = response.json()
    print(f"✅ State: {data['state']}")
    print(f"✅ Emotion: {data.get('sentiment', 'N/A')}")
    print(f"✅ Confidence: {data.get('confidence', 'N/A')}")
    print(f"✅ Response: {data['response'][:100]}...")
    
    # Test 3: Đồng ý nhận gợi ý
    print("\n3. Đồng ý nhận gợi ý...")
    response = requests.post(f"{BASE_URL}/api/chat", json={
        "message": "có",
        "user_id": TEST_USER_ID
    })
    
    if response.status_code != 200:
        print(f"❌ Lỗi: {response.status_code}")
        return
    
    data = response.json()
    print(f"✅ State: {data['state']}")
    print(f"✅ Response: {data['response'][:100]}...")
    
    # Kiểm tra fragrance recommendation
    if 'fragrance_recommendation' in data:
        fragrance = data['fragrance_recommendation']
        print(f"✅ Fragrance: {fragrance['fragrance']['name']}")
        print(f"✅ Personalized: {fragrance.get('personalized', False)}")
    else:
        print("❌ Không có fragrance recommendation")
    
    # Test 4: Chia sẻ cảm xúc negative
    print("\n4. Chia sẻ cảm xúc negative...")
    response = requests.post(f"{BASE_URL}/api/chat", json={
        "message": "tôi đang stress lắm",
        "user_id": TEST_USER_ID
    })
    
    if response.status_code != 200:
        print(f"❌ Lỗi: {response.status_code}")
        return
    
    data = response.json()
    print(f"✅ State: {data['state']}")
    print(f"✅ Emotion: {data.get('sentiment', 'N/A')}")
    print(f"✅ Confidence: {data.get('confidence', 'N/A')}")
    
    # Test 5: Đồng ý nhận gợi ý lần 2
    print("\n5. Đồng ý nhận gợi ý lần 2...")
    response = requests.post(f"{BASE_URL}/api/chat", json={
        "message": "có",
        "user_id": TEST_USER_ID
    })
    
    if response.status_code != 200:
        print(f"❌ Lỗi: {response.status_code}")
        return
    
    data = response.json()
    print(f"✅ State: {data['state']}")
    
    if 'fragrance_recommendation' in data:
        fragrance = data['fragrance_recommendation']
        print(f"✅ Fragrance: {fragrance['fragrance']['name']}")
        print(f"✅ Personalized: {fragrance.get('personalized', False)}")
    
    # Test 6: Kiểm tra user preferences
    print("\n6. Kiểm tra user preferences...")
    response = requests.get(f"{BASE_URL}/api/user/{TEST_USER_ID}/preferences")
    
    if response.status_code == 200:
        data = response.json()
        preferences = data.get('preferences', [])
        print(f"✅ Preferences count: {len(preferences)}")
        for pref in preferences:
            print(f"   - {pref['emotion']}: {pref['fragrance_name']}")
    else:
        print(f"❌ Lỗi: {response.status_code}")
    
    # Test 7: Kiểm tra user stats
    print("\n7. Kiểm tra user stats...")
    response = requests.get(f"{BASE_URL}/api/user/{TEST_USER_ID}/stats")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Total conversations: {data.get('total_conversations', 0)}")
        print(f"✅ Total messages: {data.get('total_messages', 0)}")
        print(f"✅ Favorite emotion: {data.get('favorite_emotion', 'N/A')}")
        print(f"✅ Favorite fragrance: {data.get('favorite_fragrance', 'N/A')}")
    else:
        print(f"❌ Lỗi: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("✅ Test hoàn thành!")

def test_personalization_repeat():
    """Test personalization khi user quay lại"""
    print("\n🔄 Test Personalization Repeat")
    print("=" * 40)
    
    # Test với user đã có preferences
    print("\n1. Chia sẻ cảm xúc positive (lần 2)...")
    response = requests.post(f"{BASE_URL}/api/chat", json={
        "message": "tôi vui lắm",
        "user_id": TEST_USER_ID
    })
    
    if response.status_code != 200:
        print(f"❌ Lỗi: {response.status_code}")
        return
    
    data = response.json()
    print(f"✅ State: {data['state']}")
    print(f"✅ Emotion: {data.get('sentiment', 'N/A')}")
    
    # Đồng ý nhận gợi ý
    print("\n2. Đồng ý nhận gợi ý...")
    response = requests.post(f"{BASE_URL}/api/chat", json={
        "message": "có",
        "user_id": TEST_USER_ID
    })
    
    if response.status_code != 200:
        print(f"❌ Lỗi: {response.status_code}")
        return
    
    data = response.json()
    print(f"✅ State: {data['state']}")
    
    if 'fragrance_recommendation' in data:
        fragrance = data['fragrance_recommendation']
        print(f"✅ Fragrance: {fragrance['fragrance']['name']}")
        print(f"✅ Personalized: {fragrance.get('personalized', False)}")
        if fragrance.get('personalized'):
            print(f"✅ Reason: {fragrance.get('reason', 'N/A')}")
    else:
        print("❌ Không có fragrance recommendation")
    
    print("\n" + "=" * 40)
    print("✅ Test repeat hoàn thành!")

def test_state_transitions():
    """Test các chuyển đổi state"""
    print("\n🔄 Test State Transitions")
    print("=" * 40)
    
    # Tạo user mới cho test
    test_user = f"test_user_transitions_{int(time.time())}"
    
    states_expected = [
        ("xin chào", "small_talk"),
        ("tôi buồn", "emotion_detected"),
        ("có", "suggest_fragrance"),
        ("tiếp tục", "ask_feeling"),
        ("tôi vui", "emotion_detected"),
        ("có", "suggest_fragrance"),
        ("tạm biệt", "end_session")
    ]
    
    for i, (message, expected_state) in enumerate(states_expected, 1):
        print(f"\n{i}. Message: '{message}' -> Expected: {expected_state}")
        
        response = requests.post(f"{BASE_URL}/api/chat", json={
            "message": message,
            "user_id": test_user
        })
        
        if response.status_code != 200:
            print(f"❌ Lỗi: {response.status_code}")
            continue
        
        data = response.json()
        actual_state = data['state']
        
        if actual_state == expected_state:
            print(f"✅ State: {actual_state}")
        else:
            print(f"❌ Expected: {expected_state}, Got: {actual_state}")
        
        print(f"   Response: {data['response'][:50]}...")

if __name__ == "__main__":
    try:
        # Test toàn bộ flow
        test_full_personalization_flow()
        
        # Test personalization repeat
        test_personalization_repeat()
        
        # Test state transitions
        test_state_transitions()
        
    except requests.exceptions.ConnectionError:
        print("❌ Không thể kết nối đến server. Hãy đảm bảo app đang chạy.")
    except Exception as e:
        print(f"❌ Lỗi: {e}") 