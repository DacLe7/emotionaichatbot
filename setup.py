#!/usr/bin/env python3
"""
Setup script cho EmotionAI Chatbot
Tự động cài đặt dependencies và khởi tạo dự án
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Kiểm tra phiên bản Python"""
    if sys.version_info < (3, 7):
        print("❌ Yêu cầu Python 3.7 trở lên!")
        print(f"   Phiên bản hiện tại: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_requirements():
    """Cài đặt requirements"""
    print("📦 Đang cài đặt dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Cài đặt dependencies thành công!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi cài đặt dependencies: {e}")
        return False

def download_nltk_data():
    """Download NLTK data cần thiết"""
    print("📚 Đang tải NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        print("✅ NLTK data đã sẵn sàng!")
        return True
    except Exception as e:
        print(f"❌ Lỗi tải NLTK data: {e}")
        return False

def test_imports():
    """Test import các thư viện"""
    print("🧪 Đang test imports...")
    try:
        import flask
        import textblob
        import nltk
        import pandas
        import numpy
        import sklearn
        print("✅ Tất cả imports thành công!")
        return True
    except ImportError as e:
        print(f"❌ Lỗi import: {e}")
        return False

def create_directories():
    """Tạo các thư mục cần thiết"""
    print("📁 Đang tạo thư mục...")
    try:
        Path("templates").mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
        print("✅ Thư mục đã sẵn sàng!")
        return True
    except Exception as e:
        print(f"❌ Lỗi tạo thư mục: {e}")
        return False

def run_tests():
    """Chạy test cơ bản"""
    print("🧪 Đang chạy tests...")
    try:
        # Test import app
        from app import app, analyze_sentiment
        print("✅ App import thành công!")
        
        # Test sentiment analysis
        sentiment, confidence = analyze_sentiment("Tôi rất vui!")
        print(f"✅ Sentiment analysis test: {sentiment} ({confidence:.2f})")
        
        return True
    except Exception as e:
        print(f"❌ Lỗi test: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 EmotionAI Chatbot Setup")
    print("=" * 40)
    
    # Kiểm tra Python version
    if not check_python_version():
        return False
    
    # Tạo thư mục
    if not create_directories():
        return False
    
    # Cài đặt requirements
    if not install_requirements():
        return False
    
    # Download NLTK data
    if not download_nltk_data():
        return False
    
    # Test imports
    if not test_imports():
        return False
    
    # Run tests
    if not run_tests():
        return False
    
    print("\n🎉 Setup hoàn thành!")
    print("\n📋 Hướng dẫn sử dụng:")
    print("   1. Chạy chatbot: python app.py")
    print("   2. Mở trình duyệt: http://localhost:5000")
    print("   3. Test demo: python demo.py")
    print("   4. Chế độ tương tác: python demo.py --interactive")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 