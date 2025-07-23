#!/usr/bin/env python3
"""
نظام الإدارة المتكامل - شبيه بـ Odoo
Integrated Management System - Odoo-like
"""

import subprocess
import sys
import os
import time

def print_banner():
    """Print system banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    🏢 نظام الإدارة المتكامل | Integrated Management System    ║
    ║                                                              ║
    ║    ✨ حلول أعمال شاملة مع تقنية ثلاثية الأبعاد ✨              ║
    ║    ✨ Comprehensive Business Solutions with 3D Technology ✨   ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def install_requirements():
    """Install required packages"""
    print("🔧 تثبيت المتطلبات... | Installing requirements...")
    print("=" * 60)
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "odoo_requirements.txt"])
        
        print("✅ تم تثبيت جميع المتطلبات بنجاح | All requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ خطأ في تثبيت المتطلبات | Error installing requirements: {e}")
        return False

def check_system_requirements():
    """Check system requirements"""
    print("🔍 فحص متطلبات النظام... | Checking system requirements...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ يتطلب Python 3.8 أو أحدث | Requires Python 3.8 or newer")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check if files exist
    required_files = ["odoo_like_system.py", "odoo_requirements.txt"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ الملف المطلوب غير موجود | Required file not found: {file}")
            return False
        print(f"✅ {file}")
    
    return True

def run_system():
    """Run the Odoo-like system"""
    print("\n🚀 تشغيل نظام الإدارة المتكامل... | Starting Integrated Management System...")
    print("=" * 60)
    print("🌐 سيتم فتح النظام في المتصفح تلقائياً | System will open in browser automatically")
    print("📍 العنوان: http://localhost:8501 | URL: http://localhost:8501")
    print("⏹️  للإيقاف اضغط Ctrl+C | To stop press Ctrl+C")
    print("=" * 60)
    
    try:
        # Add a small delay for better user experience
        time.sleep(2)
        
        # Run Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "odoo_like_system.py", 
                       "--server.port", "8501", "--server.address", "localhost"])
    except KeyboardInterrupt:
        print("\n👋 تم إيقاف النظام بنجاح | System stopped successfully")
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل النظام | Error running system: {e}")

def show_features():
    """Show system features"""
    features = """
    🎯 الميزات الرئيسية | Key Features:
    
    🏠 لوحة تحكم ثلاثية الأبعاد        | 3D Dashboard
    💰 نظام محاسبة متكامل             | Integrated Accounting
    📈 إدارة المبيعات                | Sales Management  
    👥 إدارة علاقات العملاء (CRM)     | Customer Relationship Management
    📦 إدارة المخزون                 | Inventory Management
    👨‍💼 إدارة الموارد البشرية          | Human Resources Management
    🛒 إدارة المشتريات               | Purchase Management
    📊 تقارير متقدمة ثلاثية الأبعاد    | Advanced 3D Reports
    
    ✨ تقنيات متقدمة:
    • رسوم بيانية ثلاثية الأبعاد عالية الجودة
    • واجهة مستخدم حديثة شبيهة بـ Odoo
    • دعم كامل للغة العربية والإنجليزية
    • تصدير التقارير بصيغ متعددة
    • تحليلات مالية متقدمة
    """
    print(features)

def main():
    """Main function"""
    print_banner()
    
    # Show features
    show_features()
    
    # Check system requirements
    if not check_system_requirements():
        print("\n❌ فشل في فحص متطلبات النظام | System requirements check failed")
        return
    
    print("\n" + "=" * 60)
    
    # Install requirements
    if install_requirements():
        print("\n" + "=" * 60)
        print("🎯 النظام جاهز للتشغيل | System ready to run")
        
        # Ask user if they want to continue
        try:
            input("\n📱 اضغط Enter للمتابعة أو Ctrl+C للإلغاء | Press Enter to continue or Ctrl+C to cancel...")
            run_system()
        except KeyboardInterrupt:
            print("\n👋 تم إلغاء التشغيل | Launch cancelled")
    else:
        print("\n❌ فشل في تثبيت المتطلبات | Failed to install requirements")
        print("💡 تأكد من اتصال الإنترنت وصلاحيات التثبيت | Check internet connection and installation permissions")

if __name__ == "__main__":
    main()
