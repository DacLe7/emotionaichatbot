"""
Debug Personalization - Tìm vấn đề personalization logic
"""

import requests
import json

def debug_personalization():
    """Debug personalization step by step"""
    
    base_url = "http://localhost:5000"
    user_id = "debug_user_123"
    
    print("🔍 Debug Personalization Step by Step")
    print("=" * 50)
    
    # Step 1: Send positive emotion
    print("\n1️⃣ Step 1: Gửi positive emotion")
    response1 = requests.post(f"{base_url}/api/chat", json={
        "message": "Tôi vui lắm",
        "user_id": user_id
    })
    
    if response1.status_code == 200:
        data1 = response1.json()
        print(f"   Response: {data1['response'][:80]}...")
        print(f"   State: {data1['state']}")
        print(f"   Sentiment: {data1['sentiment']}")
        print(f"   Confidence: {data1['confidence']}")
        
        if data1['state'] == 'emotion_detected':
            print("   ✅ State đúng: emotion_detected")
        else:
            print(f"   ❌ State sai: {data1['state']} (expected: emotion_detected)")
    
    # Step 2: Send "Có" to get fragrance
    print("\n2️⃣ Step 2: Gửi 'Có' để nhận fragrance")
    response2 = requests.post(f"{base_url}/api/chat", json={
        "message": "Có",
        "user_id": user_id
    })
    
    if response2.status_code == 200:
        data2 = response2.json()
        print(f"   Response: {data2['response'][:80]}...")
        print(f"   State: {data2['state']}")
        
        if data2['state'] == 'suggest_fragrance':
            print("   ✅ State đúng: suggest_fragrance")
            
            if 'fragrance_recommendation' in data2:
                fragrance = data2['fragrance_recommendation']['fragrance']['name']
                print(f"   ✅ Có fragrance: {fragrance}")
                print(f"   Personalized: {data2['fragrance_recommendation'].get('personalized', False)}")
            else:
                print("   ❌ Không có fragrance_recommendation")
        else:
            print(f"   ❌ State sai: {data2['state']} (expected: suggest_fragrance)")
    
    # Step 3: Check user preferences
    print("\n3️⃣ Step 3: Kiểm tra user preferences")
    response_prefs = requests.get(f"{base_url}/api/user/{user_id}/preferences")
    
    if response_prefs.status_code == 200:
        prefs_data = response_prefs.json()
        preferences = prefs_data.get('preferences', [])
        print(f"   Số preferences: {len(preferences)}")
        
        if len(preferences) > 0:
            print("   ✅ Có preferences được lưu")
            for pref in preferences:
                print(f"   - {pref['emotion']}: {pref['fragrance_name']}")
        else:
            print("   ❌ Không có preferences được lưu")
    
    # Step 4: Test with same user again
    print("\n4️⃣ Step 4: Test với cùng user")
    response3 = requests.post(f"{base_url}/api/chat", json={
        "message": "Tôi vui",
        "user_id": user_id
    })
    
    if response3.status_code == 200:
        data3 = response3.json()
        print(f"   Response: {data3['response'][:80]}...")
        print(f"   State: {data3['state']}")
        
        if data3['state'] == 'emotion_detected':
            print("   ✅ State đúng: emotion_detected")
        else:
            print(f"   ❌ State sai: {data3['state']}")

if __name__ == "__main__":
    debug_personalization() 