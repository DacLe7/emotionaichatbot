#!/usr/bin/env python3
"""
Demo script để test EmotionAI Chatbot với gợi ý nến thơm
Chạy script này để thử nghiệm chatbot với các tin nhắn mẫu
"""

import requests
import json
import time
from datetime import datetime

# URL của chatbot API
BASE_URL = "http://localhost:5000"

def test_chatbot():
    """Test chatbot với các tin nhắn mẫu"""
    
    # Danh sách tin nhắn mẫu để test
    test_messages = [
        "Tôi cảm thấy rất vui và hạnh phúc hôm nay!",
        "Cuộc sống thật tuyệt vời, tôi rất biết ơn.",
        "Tôi đang cảm thấy buồn và chán nản.",
        "Mọi thứ thật khó khăn, tôi không biết phải làm gì.",
        "Hôm nay là một ngày bình thường.",
        "Tôi không chắc chắn về cảm xúc của mình.",
        "Tôi rất phấn khích về dự án mới!",
        "Tôi lo lắng về kỳ thi sắp tới.",
        "Tôi yêu cuộc sống này!",
        "Tôi cảm thấy cô đơn và mất mát."
    ]
    
    print("🤖 EmotionAI Chatbot Demo - Với Gợi Ý Nến Thơm")
    print("=" * 60)
    print(f"Thời gian bắt đầu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test từng tin nhắn
    for i, message in enumerate(test_messages, 1):
        print(f"📝 Test {i}: {message}")
        
        try:
            # Gửi tin nhắn đến chatbot
            response = requests.post(f"{BASE_URL}/api/chat", 
                                   json={"message": message, "user_id": "demo_user"})
            
            if response.status_code == 200:
                data = response.json()
                
                # Hiển thị kết quả
                sentiment_emoji = {
                    "positive": "😊",
                    "negative": "😔", 
                    "neutral": "😐"
                }
                
                print(f"   🤖 Bot: {data['response']}")
                print(f"   🎭 Cảm xúc: {sentiment_emoji.get(data['sentiment'], '❓')} {data['sentiment']}")
                print(f"   📊 Độ tin cậy: {data['confidence']:.1%}")
                
                # Hiển thị gợi ý nến thơm
                if 'fragrance_recommendation' in data and data['fragrance_recommendation']:
                    fragrance = data['fragrance_recommendation']['fragrance']
                    print(f"   🕯️ Gợi ý nến: {fragrance['emoji']} {fragrance['name']}")
                    print(f"   🌺 Hương thơm: {fragrance['scent']}")
                    print(f"   ✨ Lợi ích: {fragrance['benefit']}")
                    print(f"   💡 Lý do: {fragrance['reason']}")
                
                print()
                
            else:
                print(f"   ❌ Lỗi: {response.status_code} - {response.text}")
                print()
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Không thể kết nối đến server. Hãy đảm bảo chatbot đang chạy!")
            print()
            break
        except Exception as e:
            print(f"   ❌ Lỗi: {str(e)}")
            print()
        
        # Delay giữa các tin nhắn
        time.sleep(1)
    
    # Test analytics
    print("📊 Testing Analytics API...")
    try:
        analytics_response = requests.get(f"{BASE_URL}/api/analytics")
        if analytics_response.status_code == 200:
            analytics_data = analytics_response.json()
            print(f"   📈 Tổng tin nhắn: {analytics_data['total_messages']}")
            print("   📊 Thống kê cảm xúc:")
            for stat in analytics_data['sentiment_stats']:
                print(f"      - {stat['sentiment']}: {stat['count']} tin nhắn")
        else:
            print(f"   ❌ Lỗi analytics: {analytics_response.status_code}")
    except Exception as e:
        print(f"   ❌ Lỗi analytics: {str(e)}")
    
    # Test fragrance API
    print("\n🕯️ Testing Fragrance API...")
    try:
        fragrance_response = requests.get(f"{BASE_URL}/api/fragrances")
        if fragrance_response.status_code == 200:
            fragrance_data = fragrance_response.json()
            print("   📋 Danh sách nến thơm theo cảm xúc:")
            for emotion, data in fragrance_data['fragrances'].items():
                print(f"      - {emotion}: {len(data['fragrances'])} loại nến")
        else:
            print(f"   ❌ Lỗi fragrance API: {fragrance_response.status_code}")
    except Exception as e:
        print(f"   ❌ Lỗi fragrance API: {str(e)}")
    
    print()
    print("✅ Demo hoàn thành!")
    print(f"Thời gian kết thúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def interactive_mode():
    """Chế độ tương tác với chatbot"""
    print("🤖 EmotionAI Chatbot - Chế độ tương tác với Gợi Ý Nến Thơm")
    print("=" * 60)
    print("Nhập 'quit' để thoát")
    print()
    
    while True:
        try:
            message = input("👤 Bạn: ").strip()
            
            if message.lower() in ['quit', 'exit', 'q']:
                print("👋 Tạm biệt!")
                break
            
            if not message:
                continue
            
            # Gửi tin nhắn
            response = requests.post(f"{BASE_URL}/api/chat", 
                                   json={"message": message, "user_id": "interactive_user"})
            
            if response.status_code == 200:
                data = response.json()
                sentiment_emoji = {
                    "positive": "😊",
                    "negative": "😔", 
                    "neutral": "😐"
                }
                
                print(f"🤖 Bot: {data['response']}")
                print(f"🎭 Cảm xúc: {sentiment_emoji.get(data['sentiment'], '❓')} {data['sentiment']} ({data['confidence']:.1%})")
                
                # Hiển thị gợi ý nến thơm
                if 'fragrance_recommendation' in data and data['fragrance_recommendation']:
                    fragrance = data['fragrance_recommendation']['fragrance']
                    print(f"🕯️ Gợi ý nến: {fragrance['emoji']} {fragrance['name']}")
                    print(f"🌺 Hương thơm: {fragrance['scent']}")
                    print(f"✨ Lợi ích: {fragrance['benefit']}")
                    print(f"💡 Lý do: {fragrance['reason']}")
                
                print()
            else:
                print(f"❌ Lỗi: {response.status_code}")
                print()
                
        except requests.exceptions.ConnectionError:
            print("❌ Không thể kết nối đến server. Hãy đảm bảo chatbot đang chạy!")
            break
        except KeyboardInterrupt:
            print("\n👋 Tạm biệt!")
            break
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
            print()

def test_fragrance_mapping():
    """Test riêng logic mapping nến thơm"""
    print("🧪 Test Fragrance Mapping Logic")
    print("=" * 40)
    
    try:
        from fragrance_mapping import FragranceMapper
        
        mapper = FragranceMapper()
        test_emotions = ["positive", "negative", "neutral"]
        
        for emotion in test_emotions:
            print(f"\n🎭 Cảm xúc: {emotion}")
            recommendation = mapper.get_fragrance_recommendation(emotion, 0.8)
            fragrance = recommendation['fragrance']
            
            print(f"🕯️ Gợi ý: {fragrance['emoji']} {fragrance['name']}")
            print(f"🌺 Hương: {fragrance['scent']}")
            print(f"✨ Lợi ích: {fragrance['benefit']}")
            print(f"💡 Lý do: {fragrance['reason']}")
            
    except ImportError:
        print("❌ Không thể import fragrance_mapping module")
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive":
            interactive_mode()
        elif sys.argv[1] == "--fragrance-test":
            test_fragrance_mapping()
        else:
            print("Usage:")
            print("  python demo.py              # Demo tự động")
            print("  python demo.py --interactive # Chế độ tương tác")
            print("  python demo.py --fragrance-test # Test logic mapping")
    else:
        test_chatbot() 