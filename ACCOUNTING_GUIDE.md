# دليل نظام المحاسبة الشامل | Complete Accounting System Guide

## 🎯 نظرة عامة | Overview

نظام محاسبي شامل يدعم جميع العمليات المحاسبية الأساسية مع دعم كامل لـ Excel، مصمم خصيصاً للشركات الصغيرة والمتوسطة.

A comprehensive accounting system that supports all basic accounting operations with full Excel support, designed specifically for small and medium enterprises.

## ✨ الميزات الرئيسية | Key Features

### 🏠 لوحة التحكم | Dashboard
- **المؤشرات المالية الرئيسية** | Key Financial Metrics
- **الرسوم البيانية التفاعلية** | Interactive Charts  
- **ملخص الحالة المالية** | Financial Status Summary

### 📊 شجرة الحسابات | Chart of Accounts
- **إدارة الحسابات** | Account Management
- **تصنيف الحسابات** | Account Classification:
  - الأصول المتداولة | Current Assets
  - الأصول الثابتة | Fixed Assets
  - الخصوم المتداولة | Current Liabilities
  - الخصوم طويلة الأجل | Long-term Liabilities
  - رأس المال | Equity
  - الإيرادات | Revenue
  - المصروفات | Expenses

### 📝 القيود المحاسبية | Journal Entries
- **إدخال القيود** | Entry Input
- **التوازن التلقائي** | Automatic Balancing
- **تتبع المراجع** | Reference Tracking
- **تحديث الأرصدة** | Balance Updates

### 🧾 إدارة الفواتير | Invoice Management
- **إنشاء الفواتير** | Invoice Creation
- **تتبع الحالة** | Status Tracking
- **حساب الإجماليات** | Total Calculations
- **تقارير العملاء** | Customer Reports

### 💸 إدارة المصروفات | Expense Management
- **تصنيف المصروفات** | Expense Categories
- **طرق الدفع** | Payment Methods
- **التحليل الإحصائي** | Statistical Analysis
- **الرسوم البيانية** | Charts & Graphs

### 📈 التقارير المحاسبية | Financial Reports
- **ميزان المراجعة** | Trial Balance
- **قائمة الدخل** | Income Statement
- **الميزانية العمومية** | Balance Sheet
- **قائمة التدفق النقدي** | Cash Flow Statement

### 📋 وظائف Excel المتقدمة | Advanced Excel Functions
- **حاسبة تفاعلية** | Interactive Calculator
- **الدوال المحاسبية** | Accounting Functions:
  - SUM (المجموع)
  - AVERAGE (المتوسط)
  - COUNT (العدد)
  - MAX/MIN (الحد الأقصى/الأدنى)
  - STDEV (الانحراف المعياري)

## 🚀 طرق التشغيل | Running Methods

### الطريقة الأولى: HTML التجريبي | Method 1: HTML Demo
**الأسرع والأسهل | Fastest & Easiest**

1. **افتح الملف** | **Open File**
   ```
   double-click: accounting_demo.html
   ```

2. **الميزات المتاحة** | **Available Features**
   - ✅ واجهة ثنائية اللغة | Bilingual Interface
   - ✅ حاسبة Excel تفاعلية | Interactive Excel Calculator
   - ✅ نماذج إدخال البيانات | Data Entry Forms
   - ✅ عرض التقارير | Report Display
   - ✅ تصميم متجاوب | Responsive Design

### الطريقة الثانية: Streamlit الكامل | Method 2: Full Streamlit
**للاستخدام المتقدم | For Advanced Usage**

1. **تثبيت المتطلبات** | **Install Requirements**
   ```bash
   pip install -r accounting_requirements.txt
   ```

2. **تشغيل النظام** | **Run System**
   ```bash
   streamlit run accounting_system.py
   ```

3. **الميزات الإضافية** | **Additional Features**
   - ✅ معالجة البيانات الحقيقية | Real Data Processing
   - ✅ استيراد/تصدير Excel | Excel Import/Export
   - ✅ إنشاء ملفات PDF | PDF Generation
   - ✅ النسخ الاحتياطي | Backup System
   - ✅ قوالب Excel جاهزة | Ready Excel Templates

## 📚 دليل الاستخدام | User Guide

### البدء السريع | Quick Start

1. **اختر اللغة** | **Select Language**
   - العربية أو English
   - التبديل متاح في أي وقت

2. **إعداد الحسابات** | **Setup Accounts**
   - انتقل إلى "شجرة الحسابات"
   - أضف الحسابات الأساسية
   - حدد الأرصدة الافتتاحية

3. **إدخال القيود** | **Enter Transactions**
   - استخدم "القيود المحاسبية"
   - تأكد من التوازن (مدين = دائن)
   - أضف المراجع والأوصاف

4. **إنشاء التقارير** | **Generate Reports**
   - اختر نوع التقرير
   - حدد الفترة الزمنية
   - صدّر إلى Excel أو PDF

### العمليات المحاسبية الأساسية | Basic Accounting Operations

#### إضافة حساب جديد | Adding New Account
```
رقم الحساب: 1001
اسم الحساب: النقدية  
نوع الحساب: الأصول المتداولة
الرصيد الافتتاحي: 50000.00
```

#### إدخال قيد محاسبي | Journal Entry
```
التاريخ: 2024-01-01
رقم القيد: J001
الوصف: مبيعات نقدية
الحساب: النقدية (مدين 10000)
الحساب: إيرادات المبيعات (دائن 10000)
```

#### إنشاء فاتورة | Creating Invoice
```
رقم الفاتورة: INV001
العميل: شركة أ
الخدمة: استشارات محاسبية
الكمية: 10 ساعات
السعر: 200 ريال/ساعة
الإجمالي: 2000 ريال
```

## 🔧 وظائف Excel المدعومة | Supported Excel Functions

### العمليات الحسابية | Mathematical Operations
- **الجمع** | Addition: `+`
- **الطرح** | Subtraction: `-`
- **الضرب** | Multiplication: `×`
- **القسمة** | Division: `÷`

### الدوال الإحصائية | Statistical Functions
- **SUM()** - مجموع الأرقام
- **AVERAGE()** - المتوسط الحسابي
- **COUNT()** - عدد القيم
- **MAX()** - أكبر قيمة
- **MIN()** - أصغر قيمة
- **STDEV()** - الانحراف المعياري

### مثال عملي | Practical Example
```
الأرقام المدخلة:
100
200
300
400
500

النتائج:
SUM = 1,500.00
AVERAGE = 300.00
COUNT = 5
MAX = 500.00
MIN = 100.00
STDEV = 158.11
```

## 📊 التقارير المحاسبية | Financial Reports

### ميزان المراجعة | Trial Balance
- **الغرض**: التأكد من توازن الحسابات
- **المحتوى**: جميع الحسابات مع أرصدتها
- **التوازن**: مجموع المدين = مجموع الدائن

### قائمة الدخل | Income Statement
- **الإيرادات**: جميع حسابات الإيرادات
- **المصروفات**: جميع حسابات المصروفات  
- **صافي الدخل**: الإيرادات - المصروفات

### الميزانية العمومية | Balance Sheet
- **الأصول**: الأصول المتداولة + الثابتة
- **الخصوم**: الخصوم المتداولة + طويلة الأجل
- **رأس المال**: رأس المال + الأرباح المحتجزة
- **المعادلة**: الأصول = الخصوم + رأس المال

## 💾 إدارة البيانات | Data Management

### النسخ الاحتياطي | Backup
- **تلقائي**: حفظ دوري للبيانات
- **يدوي**: تصدير شامل لجميع البيانات
- **التنسيقات**: Excel, JSON, CSV

### الاستيراد والتصدير | Import/Export
- **Excel**: استيراد/تصدير كامل
- **CSV**: للتكامل مع أنظمة أخرى
- **PDF**: للتقارير والطباعة
- **قوالب جاهزة**: لسهولة البدء

## 🔒 الأمان والموثوقية | Security & Reliability

### حماية البيانات | Data Protection
- **التشفير**: حماية البيانات الحساسة
- **النسخ الاحتياطي**: حماية من فقدان البيانات
- **التحقق**: فحص صحة البيانات

### التدقيق | Auditing
- **سجل العمليات**: تتبع جميع التغييرات
- **المراجع**: ربط كل عملية بمرجعها
- **التواريخ**: طوابع زمنية دقيقة

## 🆘 الدعم والمساعدة | Support & Help

### المشاكل الشائعة | Common Issues

**المشكلة**: الميزان غير متوازن
**الحل**: تحقق من أن مجموع المدين = مجموع الدائن

**المشكلة**: خطأ في الحاسبة
**الحل**: اضغط "C" لمسح الحاسبة وابدأ من جديد

**المشكلة**: لا يمكن تصدير Excel
**الحل**: تأكد من وجود بيانات للتصدير

### التواصل | Contact
- **البريد الإلكتروني**: accounting-support@company.com
- **الهاتف**: +966-XX-XXX-XXXX
- **الموقع**: www.accounting-system.com

---

**نتمنى لك تجربة محاسبية ممتازة! | Wishing you an excellent accounting experience!** 📊✨
