#!/bin/bash

echo "🚀 Starting deployment process..."

# Kiểm tra git status
echo "📋 Checking git status..."
git status

# Add tất cả files
echo "📁 Adding files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Deploy to Render - $(date)"

# Push lên GitHub
echo "📤 Pushing to GitHub..."
git push origin main

echo "✅ Code pushed to GitHub successfully!"
echo ""
echo "📝 Next steps:"
echo "1. Go to Render Dashboard: https://dashboard.render.com"
echo "2. Create new Web Service"
echo "3. Connect your GitHub repository"
echo "4. Set environment variable DATABASE_URL"
echo "5. Deploy!"
echo ""
echo "🔗 Your app will be available at: https://your-app-name.onrender.com" 