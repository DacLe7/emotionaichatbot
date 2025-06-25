# 🚀 Deploy Checklist - EmotionAI

## ✅ Pre-deployment Checklist

### 1. Code Quality
- [x] Tất cả API endpoints hoạt động
- [x] Database connections thành công
- [x] Error handling đầy đủ
- [x] Logging system hoạt động

### 2. Files Ready
- [x] `Dockerfile` - Cấu hình Docker
- [x] `requirements.txt` - Dependencies đầy đủ
- [x] `api/app.py` - Flask app chính
- [x] `.gitignore` - Bảo vệ thông tin nhạy cảm
- [x] `README.md` - Documentation
- [x] `DEPLOYMENT.md` - Hướng dẫn deploy

### 3. Database Setup
- [x] PostgreSQL database trên Render
- [x] Connection string sẵn sàng
- [x] Tables sẽ được tạo tự động

### 4. Environment Variables
- [x] `DATABASE_URL` - PostgreSQL connection
- [x] `PORT` - Render sẽ set tự động

## 🎯 Deployment Steps

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Step 2: Create Render Web Service
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Configure:
   - **Name**: `emotionai-chatbot`
   - **Environment**: `Docker`
   - **Branch**: `main`

### Step 3: Set Environment Variables
Trong Render Dashboard → Environment:
```
DATABASE_URL = postgresql://emotionaichatbot_db111_user:Veqwo5l28i84Ea4q1lwxolnR4GWD4JjM@dpg-d1ddo0ali9vc73aehmhg-a.oregon-postgres.render.com/emotionaichatbot_db111
```

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait for build (5-10 minutes)
3. Check logs for any errors

## 🧪 Post-deployment Testing

### Test Production APIs
```bash
python scripts/test_fragrance_api.py prod
```

### Manual Testing
1. **Fragrance APIs:**
   - GET `/api/fragrances`
   - POST `/api/fragrance/add`
   - GET `/api/fragrance/positive`

2. **Chat API:**
   - POST `/api/chat` với message test

3. **Analytics:**
   - GET `/api/analytics`

## 🔍 Troubleshooting

### Common Issues:
1. **Build failed**: Check `requirements.txt` and `Dockerfile`
2. **Database connection failed**: Verify `DATABASE_URL`
3. **Import errors**: Check all `__init__.py` files
4. **Port binding**: Ensure `$PORT` environment variable

### Debug Commands:
```bash
# Check logs
docker logs <container_id>

# Test database connection
python -c "import psycopg2; print('DB OK')"

# Test app locally
python -m api.app
```

## 📊 Success Indicators

- ✅ Build completes without errors
- ✅ App starts successfully
- ✅ Database connection established
- ✅ All APIs return 200/201 status
- ✅ Logs show no critical errors

## 🎉 Deployment Complete!

Your app will be available at:
`https://your-app-name.onrender.com`

**Next steps:**
1. Test all APIs
2. Monitor logs for any issues
3. Set up monitoring/alerting if needed
4. Share the URL with users!

---

**Good luck with your deployment! 🚀** 