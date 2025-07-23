# Installation Guide | دليل التثبيت

## 🚀 Quick Start (HTML Demo) | البدء السريع (النسخة التجريبية)

**The easiest way to see the platform in action:**

1. **Open the demo** | **افتح النسخة التجريبية**
   - Simply double-click `demo.html` 
   - Or right-click → "Open with" → your web browser
   - أو انقر بالزر الأيمن ← "فتح باستخدام" ← متصفح الويب

2. **Features available in demo** | **الميزات المتاحة في النسخة التجريبية**
   - ✅ Bilingual interface (Arabic/English) | واجهة ثنائية اللغة
   - ✅ All 7 visualization code examples | جميع أمثلة الكود للتصورات السبعة
   - ✅ Image upload functionality | وظيفة رفع الصور
   - ✅ Responsive design | تصميم متجاوب
   - ✅ Orange theme with Arabic fonts | تصميم برتقالي مع خطوط عربية

## 🐍 Full Interactive Version (Streamlit) | النسخة التفاعلية الكاملة

**For real data visualizations and interactive features:**

### Prerequisites | المتطلبات المسبقة

- **Python 3.8 or higher** | **Python 3.8 أو أحدث**
- **pip package manager** | **مدير الحزم pip**

### Step-by-Step Installation | خطوات التثبيت

#### 1. Check Python Installation | تحقق من تثبيت Python

```bash
# Check if Python is installed
python --version
# or
python3 --version

# Check if pip is available
pip --version
# or
python -m pip --version
```

#### 2. Install Python (if needed) | ثبت Python (إذا لزم الأمر)

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation
- تأكد من تحديد "Add Python to PATH" أثناء التثبيت

**macOS:**
```bash
# Using Homebrew
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### 3. Install Dependencies | ثبت المتطلبات

```bash
# Navigate to project folder
cd "path/to/your/project/folder"

# Install required packages
pip install -r requirements.txt

# Alternative if pip doesn't work
python -m pip install -r requirements.txt
```

#### 4. Run the Application | شغل التطبيق

```bash
# Start the Streamlit app
streamlit run app.py

# Alternative command
python -m streamlit run app.py
```

#### 5. Access the Application | الوصول للتطبيق

- The app will automatically open in your browser
- If not, go to: `http://localhost:8501`
- سيفتح التطبيق تلقائياً في متصفحك
- إذا لم يحدث ذلك، اذهب إلى: `http://localhost:8501`

## 📦 What's Included | ما هو مُتضمن

### Files | الملفات

- **`app.py`** - Main Streamlit application | التطبيق الرئيسي
- **`demo.html`** - Standalone HTML demo | النسخة التجريبية المستقلة
- **`requirements.txt`** - Python dependencies | متطلبات Python
- **`README.md`** - Project documentation | توثيق المشروع
- **`INSTALLATION_GUIDE.md`** - This file | هذا الملف

### Features Comparison | مقارنة الميزات

| Feature | HTML Demo | Streamlit App |
|---------|-----------|---------------|
| Bilingual Interface | ✅ | ✅ |
| Code Examples | ✅ | ✅ |
| Real Data Visualizations | ❌ | ✅ |
| Interactive Charts | ❌ | ✅ |
| Data Upload | ❌ | ✅ |
| Live Code Execution | ❌ | ✅ |
| Image Upload | ✅ | ✅ |

## 🛠️ Troubleshooting | استكشاف الأخطاء

### Common Issues | المشاكل الشائعة

#### Python not found | Python غير موجود
```bash
# Error: 'python' is not recognized
# Solution: Try these alternatives
py --version
python3 --version
```

#### Permission errors | أخطاء الصلاحيات
```bash
# On Windows, try:
python -m pip install --user -r requirements.txt

# On macOS/Linux, try:
pip3 install --user -r requirements.txt
```

#### Port already in use | المنفذ مُستخدم بالفعل
```bash
# Run on different port
streamlit run app.py --server.port 8502
```

#### Module not found errors | أخطاء عدم وجود الوحدات
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Getting Help | الحصول على المساعدة

1. **Check the error message carefully** | **اقرأ رسالة الخطأ بعناية**
2. **Ensure Python 3.8+ is installed** | **تأكد من تثبيت Python 3.8+**
3. **Try running commands with `python -m`** | **جرب تشغيل الأوامر مع `python -m`**
4. **Check internet connection for package downloads** | **تحقق من الاتصال بالإنترنت لتحميل الحزم**

## 🎯 Next Steps | الخطوات التالية

After successful installation:

1. **Explore all visualizations** | **استكشف جميع التصورات**
2. **Try switching languages** | **جرب تبديل اللغات**
3. **Upload your own images** | **ارفع صورك الخاصة**
4. **Modify the code to add new features** | **عدل الكود لإضافة ميزات جديدة**

## 📞 Support | الدعم

- **Email**: contact@datascience-edu.com
- **Issues**: Create an issue in the repository
- **Documentation**: Check README.md for detailed information

---

**Happy Learning! | تعلم سعيد!** 🎓📊
