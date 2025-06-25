# Hướng dẫn Deploy EmotionAI lên Render

## Bước 1: Chuẩn bị Repository

1. **Push code lên GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Đảm bảo các file cần thiết:**
   - ✅ `Dockerfile` - Cấu hình Docker
   - ✅ `requirements.txt` - Dependencies
   - ✅ `api/app.py` - Flask app
   - ✅ `.gitignore` - Bảo vệ thông tin nhạy cảm

## Bước 2: Tạo Web Service trên Render

1. **Đăng nhập Render Dashboard**
2. **Click "New +" → "Web Service"**
3. **Connect GitHub repository**
4. **Cấu hình service:**
   - **Name:** `emotionai-chatbot`
   - **Environment:** `Docker`
   - **Branch:** `main`
   - **Root Directory:** `/` (để trống)

## Bước 3: Cấu hình Environment Variables

Thêm biến môi trường trong Render Dashboard:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://emotionaichatbot_db111_user:Veqwo5l28i84Ea4q1lwxolnR4GWD4JjM@dpg-d1ddo0ali9vc73aehmhg-a.oregon-postgres.render.com/emotionaichatbot_db111` |

## Bước 4: Deploy

1. **Click "Create Web Service"**
2. **Chờ build và deploy hoàn tất**
3. **Kiểm tra logs nếu có lỗi**

## Bước 5: Test API

Sau khi deploy thành công, test các API:

```bash
# Test fragrance APIs
curl https://your-app-name.onrender.com/api/fragrances

# Test chat API
curl -X POST https://your-app-name.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tôi cảm thấy buồn", "user_id": "test_user"}'
```

## Troubleshooting

### Lỗi thường gặp:

1. **Build failed:**
   - Kiểm tra `requirements.txt` có đầy đủ dependencies
   - Kiểm tra `Dockerfile` syntax

2. **Database connection failed:**
   - Kiểm tra `DATABASE_URL` environment variable
   - Đảm bảo PostgreSQL service đang chạy

3. **Import errors:**
   - Đảm bảo tất cả `__init__.py` files có mặt
   - Kiểm tra import paths trong code

### Logs:
- Xem logs trong Render Dashboard → Logs tab
- Kiểm tra build logs và runtime logs

## Bảo mật

⚠️ **QUAN TRỌNG:** 
- Không commit file `.env` lên GitHub
- Sử dụng environment variables trên Render
- Đảm bảo `.gitignore` có `.env` 