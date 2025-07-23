# دليل نظام المحاسبة المدرسية | School Accounting System Guide

## 🏫 نظرة عامة | Overview

نظام محاسبي متكامل مصمم خصيصاً للمدارس الأهلية والحكومية، يوفر إدارة شاملة للعمليات المالية والإدارية.

A comprehensive accounting system designed specifically for private and public schools, providing complete management of financial and administrative operations.

## ✨ الميزات الرئيسية | Key Features

### 🏠 لوحة التحكم | Dashboard
- **مؤشرات مالية فورية** | Real-time Financial Metrics
- **رسوم بيانية تفاعلية** | Interactive Charts
- **إجراءات سريعة** | Quick Actions
- **ملخص شامل للحالة المالية** | Comprehensive Financial Status Summary

### 📊 شجرة الحسابات المدرسية | School Chart of Accounts
**الحسابات المعدة مسبقاً:**
- **الأصول المتداولة**: النقدية، البنك، رسوم مستحقة القبض
- **الأصول الثابتة**: أثاث وتجهيزات مدرسية، أجهزة كمبيوتر وتقنية
- **الخصوم المتداولة**: رواتب مستحقة الدفع، مصروفات مستحقة الدفع
- **رأس المال**: رأس المال الأساسي
- **الإيرادات**: رسوم دراسية، رسوم أنشطة، رسوم نقل
- **المصروفات**: رواتب المعلمين، رواتب الإداريين، مصروفات تشغيلية

### 📝 القيود المحاسبية المحسنة | Enhanced Journal Entries
- **تحقق تلقائي من التوازن** | Automatic Balance Validation
- **منع الأخطاء الشائعة** | Common Error Prevention
- **ترقيم تلقائي للقيود** | Automatic Entry Numbering
- **تحديث فوري للأرصدة** | Real-time Balance Updates

### 👥 إدارة الطلاب | Student Management
- **تسجيل بيانات الطلاب** | Student Data Registration
- **تتبع الرسوم الدراسية** | School Fee Tracking
- **حالات الدفع المختلفة** | Various Payment Statuses
- **تقارير تحصيل الرسوم** | Fee Collection Reports

### 👨‍🏫 إدارة المعلمين | Teacher Management
- **ملفات المعلمين الشاملة** | Comprehensive Teacher Profiles
- **إدارة الرواتب** | Salary Management
- **تتبع التخصصات** | Specialization Tracking
- **تقارير الرواتب** | Salary Reports

### 💸 إدارة المصروفات المدرسية | School Expense Management
**فئات المصروفات المتخصصة:**
- مصروفات كهرباء وماء
- مصروفات صيانة
- مصروفات قرطاسية ومواد تعليمية
- مصروفات نقل وانتقالات
- مصروفات أمن ونظافة
- مصروفات اتصالات وإنترنت
- مصروفات تدريب المعلمين
- مصروفات أنشطة طلابية

### 📈 التقارير المدرسية المتخصصة | Specialized School Reports
1. **ميزان المراجعة** | Trial Balance
2. **تقرير الرسوم المدرسية** | School Fees Report
3. **تقرير الرواتب** | Salary Report
4. **تقرير المصروفات** | Expenses Report
5. **قائمة الدخل** | Income Statement
6. **الميزانية العمومية** | Balance Sheet

### 📋 وظائف Excel المتقدمة | Advanced Excel Functions
- **حاسبة تفاعلية** | Interactive Calculator
- **دوال إحصائية** | Statistical Functions
- **حسابات مدرسية متخصصة** | Specialized School Calculations
- **قوالب Excel جاهزة** | Ready Excel Templates

## 🚀 التشغيل | Getting Started

### المتطلبات | Requirements
```bash
Python 3.8+
pip install -r school_requirements.txt
```

### التشغيل | Running
```bash
streamlit run school_accounting.py
```

### الوصول | Access
- افتح المتصفح على: `http://localhost:8501`
- اختر اللغة (العربية/English)
- ابدأ الاستخدام فوراً

## 📚 دليل الاستخدام التفصيلي | Detailed User Guide

### البدء السريع | Quick Start

#### 1. إعداد المدرسة الأولي | Initial School Setup
1. **انتقل إلى الإعدادات** | Go to Settings
2. **أدخل معلومات المدرسة** | Enter School Information
3. **احفظ الإعدادات** | Save Settings

#### 2. إضافة الطلاب | Adding Students
```
رقم الطالب: S001
اسم الطالب: أحمد محمد علي
الصف: الأول الابتدائي
الرسوم السنوية: 8000 ريال
المبلغ المدفوع: 4000 ريال
```

#### 3. إضافة المعلمين | Adding Teachers
```
رقم المعلم: T001
اسم المعلم: محمد أحمد السعد
التخصص: الرياضيات
الراتب الشهري: 8000 ريال
```

#### 4. تسجيل دفع رسوم | Recording Fee Payment
1. **اختر الطالب** | Select Student
2. **أدخل مبلغ الدفع** | Enter Payment Amount
3. **حدد تاريخ الدفع** | Set Payment Date
4. **اضغط "تسجيل الدفع"** | Click "Record Payment"

#### 5. دفع راتب معلم | Paying Teacher Salary
1. **اختر المعلم** | Select Teacher
2. **حدد الشهر** | Select Month
3. **اضغط "دفع الراتب"** | Click "Pay Salary"

### العمليات المحاسبية | Accounting Operations

#### إضافة قيد محاسبي | Adding Journal Entry
```
التاريخ: 2024-01-15
رقم القيد: J001 (تلقائي)
الوصف: دفع رسوم الطالب أحمد محمد
الحساب: النقدية (مدين 2000)
الحساب: رسوم دراسية (دائن 2000)
```

#### إضافة مصروف | Adding Expense
```
التاريخ: 2024-01-15
نوع المصروف: مصروفات كهرباء وماء
الوصف: فاتورة كهرباء يناير
المبلغ: 3500 ريال
طريقة الدفع: تحويل بنكي
```

## 🔧 الحسابات المدرسية المتخصصة | Specialized School Calculations

### 1. حساب نسبة التحصيل | Collection Rate Calculation
```
نسبة التحصيل = (الرسوم المحصلة ÷ إجمالي الرسوم) × 100
مثال: (150,000 ÷ 200,000) × 100 = 75%
```

### 2. حساب متوسط الراتب | Average Salary Calculation
```
متوسط الراتب = إجمالي الرواتب ÷ عدد المعلمين
مثال: 80,000 ÷ 10 = 8,000 ريال
```

### 3. حساب تكلفة الطالب | Cost Per Student Calculation
```
تكلفة الطالب = إجمالي المصروفات ÷ عدد الطلاب
مثال: 500,000 ÷ 200 = 2,500 ريال
```

## 📊 التقارير المالية | Financial Reports

### تقرير الرسوم المدرسية | School Fees Report
- **تحصيل الرسوم حسب الصف** | Fee Collection by Grade
- **نسب التحصيل** | Collection Rates
- **المبالغ المتبقية** | Outstanding Amounts
- **إحصائيات شاملة** | Comprehensive Statistics

### تقرير الرواتب | Salary Report
- **الرواتب حسب التخصص** | Salaries by Specialization
- **إجمالي الرواتب الشهرية** | Total Monthly Salaries
- **متوسط الرواتب** | Average Salaries
- **عدد المعلمين** | Number of Teachers

### تقرير المصروفات | Expenses Report
- **المصروفات حسب الفئة** | Expenses by Category
- **الاتجاهات الشهرية** | Monthly Trends
- **أكبر المصروفات** | Largest Expenses
- **نسب المصروفات** | Expense Ratios

## 💾 إدارة البيانات | Data Management

### النسخ الاحتياطي | Backup
- **نسخ احتياطي شامل** | Full Backup
- **تصدير Excel متعدد الأوراق** | Multi-sheet Excel Export
- **حفظ تلقائي** | Auto-save

### الاستيراد والتصدير | Import/Export
- **استيراد بيانات الطلاب** | Import Student Data
- **استيراد بيانات المعلمين** | Import Teacher Data
- **تصدير التقارير** | Export Reports
- **قوالب Excel جاهزة** | Ready Excel Templates

### القوالب المتاحة | Available Templates
1. **قالب بيانات الطلاب** | Student Data Template
2. **قالب بيانات المعلمين** | Teacher Data Template
3. **قالب المصروفات** | Expenses Template

## 🔒 الأمان والموثوقية | Security & Reliability

### حماية البيانات | Data Protection
- **تحقق من صحة البيانات** | Data Validation
- **منع الأخطاء المحاسبية** | Accounting Error Prevention
- **نسخ احتياطي آمن** | Secure Backup

### التدقيق | Auditing
- **سجل كامل للعمليات** | Complete Transaction Log
- **تتبع التغييرات** | Change Tracking
- **مراجع واضحة** | Clear References

## 🆘 الدعم والمساعدة | Support & Help

### المشاكل الشائعة وحلولها | Common Issues & Solutions

**المشكلة**: القيود غير متوازنة
**الحل**: تأكد من أن مجموع المدين = مجموع الدائن في كل قيد

**المشكلة**: خطأ في تصدير Excel
**الحل**: تأكد من وجود بيانات للتصدير وأن الملف غير مفتوح

**المشكلة**: لا يمكن إضافة طالب
**الحل**: تأكد من عدم تكرار رقم الطالب وملء جميع الحقول المطلوبة

### نصائح للاستخدام الأمثل | Best Practice Tips

1. **قم بعمل نسخة احتياطية يومياً** | Make daily backups
2. **راجع التقارير أسبوعياً** | Review reports weekly
3. **تأكد من توازن القيود** | Ensure journal entries balance
4. **استخدم أرقام مرجعية واضحة** | Use clear reference numbers
5. **احتفظ بالمستندات الداعمة** | Keep supporting documents

## 📞 التواصل | Contact

- **البريد الإلكتروني**: school-accounting@support.com
- **الهاتف**: +966-XX-XXX-XXXX
- **الموقع**: www.school-accounting-system.com

---

**نتمنى لك إدارة مالية ناجحة لمدرستك! | Wishing you successful financial management for your school!** 🏫✨
