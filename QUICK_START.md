# 🚀 Hướng Dẫn Nhanh - EmotionAI Chatbot

## ⚡ Chạy Demo Trong 3 Bước

### Bước 1: Cài đặt Dependencies
```bash
pip install -r requirements.txt
```

### Bước 2: Chạy Chatbot
```bash
python app.py
```

### Bước 3: Mở Trình Duyệt
Truy cập: **http://localhost:5000**

---

## 🧪 Test Nhanh

### Test Demo Script
```bash
python demo.py
```

### Chế độ tương tác
```bash
python demo.py --interactive
```

---

## 📱 Tính Năng Demo

### 🤖 Chatbot Thông Minh
- **Nhận diện cảm xúc**: Tự động phân tích cảm xúc tích cực/tiêu cực/trung tính
- **Phản hồi thông minh**: Tạo phản hồi phù hợp với cảm xúc
- **Giao diện đẹp**: UI/UX hiện đại và responsive

### 📊 Dashboard Analytics
- **Thống kê real-time**: Số tin nhắn, phân bố cảm xúc
- **Độ tin cậy**: Hiển thị mức độ chính xác phân tích
- **Lịch sử chat**: Theo dõi cuộc trò chuyện gần đây

### 💾 Lưu Trữ Dữ Liệu
- **SQLite Database**: Tự động lưu toàn bộ lịch sử
- **Phân tích xu hướng**: Theo dõi thay đổi cảm xúc

---

## 🎯 Tin Nhắn Mẫu Để Test

### Cảm xúc tích cực 😊
- "Tôi cảm thấy rất vui và hạnh phúc hôm nay!"
- "Cuộc sống thật tuyệt vời, tôi rất biết ơn."
- "Tôi rất phấn khích về dự án mới!"

### Cảm xúc tiêu cực 😔
- "Tôi đang cảm thấy buồn và chán nản."
- "Mọi thứ thật khó khăn, tôi không biết phải làm gì."
- "Tôi lo lắng về kỳ thi sắp tới."

### Cảm xúc trung tính 😐
- "Hôm nay là một ngày bình thường."
- "Tôi không chắc chắn về cảm xúc của mình."

---

## 🔧 Troubleshooting

### Lỗi Import
```bash
# Cài đặt lại dependencies
pip install --upgrade -r requirements.txt
```

### Lỗi Port
```bash
# Thay đổi port trong app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Lỗi Database
```bash
# Xóa file database cũ
rm chatbot.db
# Chạy lại app.py
```

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. Python version >= 3.7
2. Tất cả dependencies đã cài đặt
3. Port 5000 không bị chiếm
4. Firewall không chặn kết nối

---

**🎉 Chúc bạn demo thành công!** 