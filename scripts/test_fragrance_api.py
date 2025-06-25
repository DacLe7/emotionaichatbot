import requests
import json
import sys

# Chọn URL để test
if len(sys.argv) > 1 and sys.argv[1] == "prod":
    BASE_URL = "https://emotionaichatbot.onrender.com"
    print("🧪 Testing PRODUCTION environment")
else:
    BASE_URL = "http://127.0.0.1:5000"
    print("🧪 Testing LOCAL environment")

print(f"📍 Base URL: {BASE_URL}")

print("\n==> GET /api/fragrances")
r = requests.get(f"{BASE_URL}/api/fragrances")
print(r.status_code, json.dumps(r.json(), ensure_ascii=False, indent=2))

print("\n==> POST /api/fragrance/add")
payload = {
    "name": "Nến Hương Quế Ấm Áp",
    "description": "Tạo cảm giác ấm cúng, dễ chịu",
    "emotion": "positive",
    "image_url": "https://link-to-image.com/cinnamon-candle.jpg"
}
r = requests.post(f"{BASE_URL}/api/fragrance/add", json=payload)
print(r.status_code)
try:
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))
except Exception as e:
    print("Không parse được JSON:", e)
    print("Response text:", r.text)

print("\n==> GET /api/fragrance/positive?confidence=0.8")
r = requests.get(f"{BASE_URL}/api/fragrance/positive?confidence=0.8")
print(r.status_code, json.dumps(r.json(), ensure_ascii=False, indent=2))

print("\n==> GET /api/fragrance/negative?confidence=0.8")
r = requests.get(f"{BASE_URL}/api/fragrance/negative?confidence=0.8")
print(r.status_code, json.dumps(r.json(), ensure_ascii=False, indent=2))

print("\n==> GET /api/fragrance/neutral?confidence=0.8")
r = requests.get(f"{BASE_URL}/api/fragrance/neutral?confidence=0.8")
print(r.status_code, json.dumps(r.json(), ensure_ascii=False, indent=2))

print("\n==> POST /api/chat")
chat_payload = {
    "message": "Tôi cảm thấy buồn và stress",
    "user_id": "test_user_123"
}
r = requests.post(f"{BASE_URL}/api/chat", json=chat_payload)
print(r.status_code)
try:
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))
except Exception as e:
    print("Không parse được JSON:", e)
    print("Response text:", r.text)

print("\n✅ Test completed!") 