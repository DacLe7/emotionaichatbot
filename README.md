# EmotionAI Chatbot

## Mục tiêu
Chatbot nhận diện cảm xúc và ý định người dùng, gợi ý nến thơm phù hợp, cá nhân hóa trải nghiệm, lưu lịch sử, phân tích log và hỗ trợ dashboard hiện đại.

---

## 1. Cấu trúc thư mục

```
.
├── api/                  # Flask backend, demo script
│   ├── app.py            # Flask app chính
│   └── demo.py           # Script demo
├── detectors/            # Module nhận diện cảm xúc, ý định
│   └── ImprovedEmotionDetector.py
├── state_machine/        # State machine hội thoại
│   └── conversation_state_machine.py
├── db/                   # Database, truy vấn, migration
│   └── user_database.py
├── utils/                # Tiện ích, mapping, logging, phân tích
│   ├── fragrance_mapping.py
│   └── log_analyzer.py
├── tests/                # Toàn bộ test script, debug script
│   ├── test_improved_emotion_detection.py
│   ├── test_full_personalization_flow.py
│   ├── test_logging_system.py
│   ├── test_personalization.py
│   ├── test_api.py
│   ├── test_emotion_detection.py
│   ├── debug_emotion_detection.py
│   └── debug_personalization.py
├── logs/                 # Log hệ thống
├── templates/            # Giao diện frontend (nếu có)
├── requirements.txt      # Thư viện Python cần cài
├── setup.py              # Cài đặt package (nếu cần)
├── README.md             # Tài liệu này
├── QUICK_START.md        # Hướng dẫn nhanh
├── PRESENTATION.md       # Slide thuyết trình
├── SYSTEM_AUDIT.md       # Báo cáo kiểm thử, audit
└── chatbot.db            # File database SQLite
```

---

## 2. Hướng dẫn cài đặt

```bash
# 1. Cài Python >=3.8
# 2. Cài các thư viện cần thiết
pip install -r requirements.txt
```

---

## 3. Chạy hệ thống

```bash
# Chạy Flask backend
cd api
python app.py
```
- Truy cập giao diện: http://localhost:5000
- Có thể chạy demo script: `python demo.py`

---

## 4. Chạy test

```bash
cd tests
python test_improved_emotion_detection.py
python test_full_personalization_flow.py
python test_logging_system.py
# ...
```

---

## 5. Các module chính

- **api/app.py**: Flask backend, API chat, logging, analytics
- **detectors/ImprovedEmotionDetector.py**: Nhận diện cảm xúc & ý định (logic chính)
- **state_machine/conversation_state_machine.py**: Quản lý luồng hội thoại, trạng thái
- **db/user_database.py**: Quản lý user, lưu lịch sử, cá nhân hóa
- **utils/fragrance_mapping.py**: Mapping cảm xúc → nến thơm
- **utils/log_analyzer.py**: Phân tích log, thống kê
- **tests/**: Toàn bộ test tự động, debug, kiểm thử flow

---

## 6. Ghi chú
- Nếu gặp lỗi database, hãy xóa file `chatbot.db` và khởi động lại app.
- Log hệ thống lưu ở `logs/`.
- Có thể mở rộng thêm module mới dễ dàng nhờ cấu trúc rõ ràng.

---

## 7. Liên hệ & đóng góp
- Đóng góp code, ý tưởng, bug report: tạo issue hoặc pull request trên repo.
- Mọi thắc mắc vui lòng liên hệ nhóm phát triển.

## 📋 Mô Tả Dự Án

EmotionAI Chatbot là một ứng dụng AI được phát triển cho môn học Khởi nghiệp, có khả năng nhận diện và phân tích cảm xúc của người dùng thông qua cuộc trò chuyện. Chatbot sử dụng công nghệ Natural Language Processing (NLP) để hiểu và phản hồi phù hợp với trạng thái cảm xúc của người dùng.

## ✨ Tính Năng Chính

### 🤖 Chatbot Thông Minh
- **Phân tích cảm xúc**: Tự động nhận diện cảm xúc tích cực, tiêu cực hoặc trung tính
- **Phản hồi thông minh**: Tạo phản hồi phù hợp dựa trên cảm xúc được phát hiện
- **Giao diện thân thiện**: UI/UX hiện đại và dễ sử dụng

### 📊 Dashboard Analytics
- **Thống kê tổng quan**: Số lượng tin nhắn, phân bố cảm xúc
- **Độ tin cậy**: Hiển thị mức độ chính xác của phân tích cảm xúc
- **Lịch sử chat**: Theo dõi các cuộc trò chuyện gần đây

### 💾 Lưu Trữ Dữ Liệu
- **Database SQLite**: Lưu trữ toàn bộ lịch sử trò chuyện
- **Phân tích xu hướng**: Theo dõi sự thay đổi cảm xúc theo thời gian

## 🛠️ Công Nghệ Sử Dụng

### Backend
- **Flask**: Web framework Python
- **TextBlob**: Thư viện phân tích cảm xúc
- **NLTK**: Natural Language Toolkit
- **SQLite**: Database nhẹ và hiệu quả

### Frontend
- **HTML5/CSS3**: Giao diện responsive
- **JavaScript**: Xử lý tương tác người dùng
- **Font Awesome**: Icons đẹp mắt

## 🚀 Cài Đặt và Chạy

### Yêu Cầu Hệ Thống
- Python 3.7+
- pip (Python package manager)

### Bước 1: Clone Repository
```bash
git clone <repository-url>
cd emotionai-chatbot
```

### Bước 2: Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy Ứng Dụng
```bash
python app.py
```

### Bước 4: Truy Cập
Mở trình duyệt và truy cập: `http://localhost:5000`

## 📁 Cấu Trúc Dự Án

```
emotionai-chatbot/
├── app.py                 # Backend Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Frontend interface
├── chatbot.db            # SQLite database (tự động tạo)
└── README.md             # Documentation
```

## 🔧 API Endpoints

### POST /api/chat
Gửi tin nhắn và nhận phản hồi từ chatbot

**Request:**
```json
{
    "message": "Tôi cảm thấy rất vui hôm nay!",
    "user_id": "user_123"
}
```

**Response:**
```json
{
    "response": "Tôi rất vui khi thấy bạn đang cảm thấy tích cực! 😊",
    "sentiment": "positive",
    "confidence": 0.85,
    "timestamp": "2024-01-15T10:30:00"
}
```

### GET /api/analytics
Lấy thống kê và phân tích dữ liệu

**Response:**
```json
{
    "total_messages": 150,
    "sentiment_stats": [
        {
            "sentiment": "positive",
            "count": 80,
            "avg_confidence": 0.75
        }
    ],
    "recent_messages": [...]
}
```

## 🧠 Thuật Toán Phân Tích Cảm Xúc

### TextBlob Sentiment Analysis
- **Polarity**: Đo lường mức độ tích cực/tiêu cực (-1 đến 1)
- **Subjectivity**: Đo lường tính chủ quan của văn bản

### Phân Loại Cảm Xúc
- **Positive** (polarity > 0.1): Cảm xúc tích cực
- **Negative** (polarity < -0.1): Cảm xúc tiêu cực  
- **Neutral** (-0.1 ≤ polarity ≤ 0.1): Cảm xúc trung tính

## 📈 Kế Hoạch Phát Triển

### Phase 1 (Hiện tại)
- ✅ Chatbot cơ bản với phân tích cảm xúc
- ✅ Giao diện web responsive
- ✅ Dashboard analytics

### Phase 2 (Tương lai)
- 🔄 Tích hợp machine learning nâng cao
- 🔄 Hỗ trợ đa ngôn ngữ
- 🔄 Tích hợp với social media
- 🔄 Mobile app

### Phase 3 (Mở rộng)
- 🔄 AI counseling features
- 🔄 Emotion tracking over time
- 🔄 Integration with health apps

## 🤝 Đóng Góp

Dự án này được phát triển cho mục đích học tập. Mọi đóng góp đều được chào đón!

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 👥 Team

- **Developer**: [Tên của bạn]
- **Course**: Khởi nghiệp
- **Institution**: [Tên trường]

## 📞 Liên Hệ

- Email: [your.email@example.com]
- GitHub: [your-github-username]

---

**Lưu ý**: Đây là dự án demo cho môn học. Trong môi trường production, cần bổ sung thêm các biện pháp bảo mật và tối ưu hóa hiệu suất.

## Hướng dẫn chuẩn bị và deploy lên Render

### 1. Chuẩn bị trước khi đẩy lên GitHub
- Đảm bảo đã có các file sau ở thư mục gốc:
  - `requirements.txt` (đã có)
  - `Procfile` (đã tạo)
  - Thư mục `api/` chứa `app.py`
  - Thư mục `templates/` chứa `index.html`
  - Các thư mục code khác (`db/`, `utils/`, ...)

### 2. Đẩy code lên GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<ten-github-cua-ban>/<ten-repo>.git
git push -u origin main
```

### 3. Deploy lên Render
1. Đăng nhập [https://render.com](https://render.com)
2. Chọn **New Web Service** > Kết nối GitHub > Chọn repo vừa push
3. Build Command: *(để trống, Render sẽ tự động)*
4. Start Command: `gunicorn api.app:app`
5. Nhấn **Create Web Service** và chờ build xong
6. Lấy link public gửi cho bạn bè test!

### 4. Lưu ý
- Nếu app cần lưu dữ liệu lâu dài, nên dùng database cloud (PostgreSQL, MongoDB, ...)
- Nếu gặp lỗi, kiểm tra log trên Render để sửa.

---
Chúc bạn deploy thành công! 