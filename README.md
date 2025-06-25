# EmotionAI Chatbot 🧠💬

Một chatbot thông minh phân tích cảm xúc và gợi ý nến thơm phù hợp dựa trên tâm trạng của người dùng.

## 🌟 Tính năng

- **Phân tích cảm xúc**: Sử dụng TextBlob và NLTK để phân tích sentiment
- **Gợi ý nến thơm**: Dựa trên cảm xúc và lịch sử người dùng
- **Cá nhân hóa**: Học từ sở thích của người dùng
- **API RESTful**: Đầy đủ endpoints cho frontend và mobile
- **Database**: PostgreSQL cho fragrance data, SQLite cho user data
- **Logging**: Hệ thống logging chi tiết

## 🏗️ Cấu trúc Project

```
2406/
├── api/
│   └── app.py              # Flask application
├── db/
│   ├── postgres_database.py # PostgreSQL operations
│   └── user_database.py    # SQLite user operations
├── utils/
│   └── fragrance_mapping.py # Fragrance mapping logic
├── state_machine/
│   └── conversation_state_machine.py # Conversation flow
├── templates/
│   └── index.html          # Web interface
├── scripts/
│   └── test_fragrance_api.py # API testing
├── tests/                  # Test files
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Quick Start

### Local Development

1. **Clone repository:**
   ```bash
   git clone <your-repo-url>
   cd 2406
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables:**
   ```bash
   # Windows PowerShell
   $env:DATABASE_URL="postgresql://username:password@host:port/dbname"
   
   # Linux/Mac
   export DATABASE_URL="postgresql://username:password@host:port/dbname"
   ```

4. **Run application:**
   ```bash
   python -m api.app
   ```

5. **Test APIs:**
   ```bash
   python scripts/test_fragrance_api.py
   ```

### Deploy to Render

Xem file `DEPLOYMENT.md` để biết hướng dẫn chi tiết.

## 📡 API Endpoints

### Fragrance APIs
- `GET /api/fragrances` - Lấy tất cả fragrances
- `POST /api/fragrance/add` - Thêm fragrance mới
- `GET /api/fragrance/{emotion}` - Lấy fragrance theo cảm xúc

### Chat APIs
- `POST /api/chat` - Gửi tin nhắn và nhận phản hồi
- `POST /api/conversation/end` - Kết thúc cuộc trò chuyện

### Analytics APIs
- `GET /api/analytics` - Thống kê tổng quan
- `GET /api/user/{user_id}/stats` - Thống kê user
- `GET /api/user/{user_id}/preferences` - Sở thích user

## 🛠️ Technologies

- **Backend**: Flask, Python 3.10
- **Database**: PostgreSQL (fragrances), SQLite (users)
- **AI/ML**: TextBlob, NLTK, scikit-learn
- **Deployment**: Docker, Render
- **Testing**: Python requests

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `PORT`: Application port (Render sets automatically)

### Database Setup
1. Tạo PostgreSQL database trên Render
2. Set `DATABASE_URL` environment variable
3. Tables sẽ được tạo tự động

## 📊 Testing

```bash
# Test local
python scripts/test_fragrance_api.py

# Test production
python scripts/test_fragrance_api.py prod
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

Nếu gặp vấn đề, hãy:
1. Kiểm tra logs trong `logs/emotionai.log`
2. Xem troubleshooting trong `DEPLOYMENT.md`
3. Tạo issue trên GitHub

---

**Made with ❤️ by EmotionAI Team**