"""
Test Personalization - Kiểm tra user profile và gợi ý cá nhân hóa
"""

import requests
import json
import time

def test_personalization():
    """Test user profile và personalization"""
    
    base_url = "http://localhost:5000"
    user_id = "test_user_personalization"
    
    print("🧪 Test Personalization")
    print("=" * 50)
    
    # Test 1: User mới - gửi positive emotion
    print("\n1. User mới - Gửi positive emotion:")
    response1 = requests.post(f"{base_url}/api/chat", json={
        "message": "Tôi vui lắm",
        "user_id": user_id
    })
    
    if response1.status_code == 200:
        data1 = response1.json()
        print(f"   Response: {data1['response'][:50]}...")
        print(f"   State: {data1['state']}")
        
        # Gửi "Có" để nhận fragrance recommendation
        response1_yes = requests.post(f"{base_url}/api/chat", json={
            "message": "Có",
            "user_id": user_id
        })
        
        if response1_yes.status_code == 200:
            data1_yes = response1_yes.json()
            if 'fragrance_recommendation' in data1_yes:
                fragrance1 = data1_yes['fragrance_recommendation']['fragrance']['name']
                print(f"   Fragrance 1: {fragrance1}")
                print(f"   Personalized: {data1_yes['fragrance_recommendation'].get('personalized', False)}")
            else:
                print("   Không có fragrance recommendation")
    
    # Test 2: Cùng user - gửi lại positive emotion
    print("\n2. Cùng user - Gửi lại positive emotion:")
    response2 = requests.post(f"{base_url}/api/chat", json={
        "message": "Tôi vui",
        "user_id": user_id
    })
    
    if response2.status_code == 200:
        data2 = response2.json()
        print(f"   Response: {data2['response'][:50]}...")
        print(f"   State: {data2['state']}")
        
        # Gửi "Có" để nhận fragrance recommendation
        response2_yes = requests.post(f"{base_url}/api/chat", json={
            "message": "Có",
            "user_id": user_id
        })
        
        if response2_yes.status_code == 200:
            data2_yes = response2_yes.json()
            if 'fragrance_recommendation' in data2_yes:
                fragrance2 = data2_yes['fragrance_recommendation']['fragrance']['name']
                print(f"   Fragrance 2: {fragrance2}")
                print(f"   Personalized: {data2_yes['fragrance_recommendation'].get('personalized', False)}")
                
                # So sánh
                if fragrance1 == fragrance2:
                    print(f"   ✅ Personalization hoạt động: {fragrance1}")
                else:
                    print(f"   ❌ Personalization không hoạt động: {fragrance1} vs {fragrance2}")
            else:
                print("   Không có fragrance recommendation")
    
    # Test 3: Kiểm tra user preferences API
    print("\n3. Kiểm tra User Preferences API:")
    response_prefs = requests.get(f"{base_url}/api/user/{user_id}/preferences")
    
    if response_prefs.status_code == 200:
        prefs_data = response_prefs.json()
        preferences = prefs_data.get('preferences', [])
        print(f"   Số preferences: {len(preferences)}")
        for pref in preferences:
            print(f"   - {pref['emotion']}: {pref['fragrance_name']} (rating: {pref['rating']})")
    else:
        print(f"   ❌ Lỗi API: {response_prefs.status_code}")
    
    # Test 4: Kiểm tra user stats API
    print("\n4. Kiểm tra User Stats API:")
    response_stats = requests.get(f"{base_url}/api/user/{user_id}/stats")
    
    if response_stats.status_code == 200:
        stats_data = response_stats.json()
        print(f"   Total conversations: {stats_data.get('total_conversations', 0)}")
        print(f"   Favorite emotion: {stats_data.get('favorite_emotion', 'None')}")
        print(f"   Favorite fragrance: {stats_data.get('favorite_fragrance', 'None')}")
    else:
        print(f"   ❌ Lỗi API: {response_stats.status_code}")

if __name__ == "__main__":
    test_personalization() 