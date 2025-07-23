#!/usr/bin/env python3
"""
نظام المحاسبة المدرسية - ملف التشغيل
School Accounting System - Run File
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("🔧 تثبيت المتطلبات... | Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "school_requirements.txt"])
        print("✅ تم تثبيت المتطلبات بنجاح | Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ خطأ في تثبيت المتطلبات | Error installing requirements: {e}")
        return False

def run_streamlit():
    """Run the Streamlit application"""
    print("🚀 تشغيل نظام المحاسبة المدرسية... | Starting School Accounting System...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "school_accounting.py"])
    except KeyboardInterrupt:
        print("\n👋 تم إيقاف النظام | System stopped")
    except Exception as e:
        print(f"❌ خطأ في تشغيل النظام | Error running system: {e}")

def main():
    """Main function"""
    print("=" * 60)
    print("🏫 نظام المحاسبة المدرسية | School Accounting System")
    print("=" * 60)
    
    # Check if school_accounting.py exists
    if not os.path.exists("school_accounting.py"):
        print("❌ ملف school_accounting.py غير موجود | school_accounting.py file not found")
        return
    
    # Check if requirements file exists
    if not os.path.exists("school_requirements.txt"):
        print("❌ ملف school_requirements.txt غير موجود | school_requirements.txt file not found")
        return
    
    # Install requirements
    if install_requirements():
        print("\n" + "=" * 60)
        print("🎯 النظام جاهز للتشغيل | System ready to run")
        print("🌐 سيتم فتح النظام في المتصفح تلقائياً | System will open in browser automatically")
        print("📍 العنوان: http://localhost:8501 | URL: http://localhost:8501")
        print("⏹️  للإيقاف اضغط Ctrl+C | To stop press Ctrl+C")
        print("=" * 60)
        
        # Run the system
        run_streamlit()
    else:
        print("❌ فشل في تثبيت المتطلبات | Failed to install requirements")

if __name__ == "__main__":
    main()
