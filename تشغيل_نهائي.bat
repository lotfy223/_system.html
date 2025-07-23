@echo off
chcp 65001 >nul
color 0A
title 🏆 أكاديمية التميز الدولية - التشغيل النهائي
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🏆 أكاديمية التميز الدولية                             ║
echo ║                Excellence International Academy                             ║
echo ║                        التشغيل النهائي الذكي                              ║
echo ║                      Smart Final Launch System                             ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo 🚀 بدء التشغيل الذكي للنظام...
echo 🚀 Starting smart system launch...
echo.

REM Check if files exist
if not exist "excellence_academy_enhanced.html" (
    if not exist "excellence_academy_offline.html" (
        echo ❌ لم يتم العثور على ملفات النظام
        echo ❌ System files not found
        echo.
        echo تأكد من وجود أحد الملفات التالية:
        echo Make sure one of these files exists:
        echo - excellence_academy_enhanced.html
        echo - excellence_academy_offline.html
        echo.
        pause
        exit /b 1
    )
)

echo 🔍 اختيار أفضل نسخة متاحة...
echo 🔍 Selecting best available version...
echo.

REM Prefer enhanced version if available
if exist "excellence_academy_enhanced.html" (
    set "system_file=excellence_academy_enhanced.html"
    set "system_name=النظام المحسن مع تحليل الملفات"
    set "system_name_en=Enhanced System with File Analysis"
    echo ✅ تم اختيار النظام المحسن
    echo ✅ Enhanced system selected
) else (
    set "system_file=excellence_academy_offline.html"
    set "system_name=النظام المحمول"
    set "system_name_en=Portable System"
    echo ✅ تم اختيار النظام المحمول
    echo ✅ Portable system selected
)

echo.
echo 🌐 محاولة فتح %system_name%...
echo 🌐 Attempting to open %system_name_en%...
echo.

REM Method 1: Default Windows file association
echo 📂 الطريقة الأولى: الفتح الافتراضي...
echo 📂 Method 1: Default opening...
start "" "%system_file%" >nul 2>&1
if %errorlevel% equ 0 (
    timeout /t 2 >nul
    echo ✅ تم فتح النظام بنجاح!
    echo ✅ System opened successfully!
    goto :success
)

REM Method 2: Using rundll32
echo 🔄 الطريقة الثانية: rundll32...
echo 🔄 Method 2: rundll32...
rundll32 url.dll,FileProtocolHandler "%~dp0%system_file%" >nul 2>&1
if %errorlevel% equ 0 (
    timeout /t 2 >nul
    echo ✅ تم فتح النظام بنجاح!
    echo ✅ System opened successfully!
    goto :success
)

REM Method 3: PowerShell
echo 🔄 الطريقة الثالثة: PowerShell...
echo 🔄 Method 3: PowerShell...
powershell -WindowStyle Hidden -Command "Start-Process '%~dp0%system_file%'" >nul 2>&1
if %errorlevel% equ 0 (
    timeout /t 2 >nul
    echo ✅ تم فتح النظام بنجاح!
    echo ✅ System opened successfully!
    goto :success
)

REM Method 4: Browser detection
echo 🔍 الطريقة الرابعة: البحث عن متصفح...
echo 🔍 Method 4: Browser detection...

REM Chrome detection
for %%i in (
    "%ProgramFiles%\Google\Chrome\Application\chrome.exe"
    "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
    "%LocalAppData%\Google\Chrome\Application\chrome.exe"
    "%UserProfile%\AppData\Local\Google\Chrome\Application\chrome.exe"
) do (
    if exist "%%i" (
        echo ✅ تم العثور على Google Chrome
        echo ✅ Found Google Chrome
        start "" "%%i" "%~dp0%system_file%"
        goto :success
    )
)

REM Edge detection
for %%i in (
    "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
    "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
) do (
    if exist "%%i" (
        echo ✅ تم العثور على Microsoft Edge
        echo ✅ Found Microsoft Edge
        start "" "%%i" "%~dp0%system_file%"
        goto :success
    )
)

REM Firefox detection
for %%i in (
    "%ProgramFiles%\Mozilla Firefox\firefox.exe"
    "%ProgramFiles(x86)%\Mozilla Firefox\firefox.exe"
) do (
    if exist "%%i" (
        echo ✅ تم العثور على Mozilla Firefox
        echo ✅ Found Mozilla Firefox
        start "" "%%i" "%~dp0%system_file%"
        goto :success
    )
)

REM Internet Explorer (last resort)
for %%i in (
    "%ProgramFiles%\Internet Explorer\iexplore.exe"
    "%ProgramFiles(x86)%\Internet Explorer\iexplore.exe"
) do (
    if exist "%%i" (
        echo ⚠️ تم العثور على Internet Explorer (قديم)
        echo ⚠️ Found Internet Explorer (legacy)
        start "" "%%i" "%~dp0%system_file%"
        goto :success
    )
)

REM If all methods fail
echo.
echo ❌ فشل في فتح النظام تلقائياً
echo ❌ Failed to open system automatically
echo.
goto :manual_instructions

:success
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                          ✅ تم تشغيل النظام بنجاح                          ║
echo ║                          ✅ System Started Successfully                     ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo 🎯 النظام المفتوح: %system_name%
echo 🎯 Opened System: %system_name_en%
echo.
echo 🔐 بيانات تسجيل الدخول السريعة:
echo 🔐 Quick Login Credentials:
echo.
echo 👤 اسم المستخدم: admin
echo 👤 Username: admin
echo.
echo 🔑 كلمة المرور: 123456
echo 🔑 Password: 123456
echo.

if "%system_file%"=="excellence_academy_enhanced.html" (
    echo ╔══════════════════════════════════════════════════════════════════════════════╗
    echo ║                        🌟 ميزات النظام المحسن                              ║
    echo ║                        🌟 Enhanced System Features                         ║
    echo ╚══════════════════════════════════════════════════════════════════════════════╝
    echo.
    echo 🔍 تحليل الصور واستخراج النصوص (OCR)
    echo    Image Analysis & Text Extraction (OCR)
    echo.
    echo 📄 تحليل ملفات PDF واستخراج المحتوى
    echo    PDF Analysis & Content Extraction
    echo.
    echo 📝 تحليل المستندات النصية
    echo    Document Text Analysis
    echo.
    echo 🤖 ذكاء اصطناعي متقدم للتحليل
    echo    Advanced AI for Analysis
    echo.
    echo 💾 حفظ نتائج التحليل مع البيانات
    echo    Save Analysis Results with Data
    echo.
    echo 🌐 يحتاج اتصال إنترنت لتحميل مكتبات التحليل
    echo    Requires internet to load analysis libraries
) else (
    echo ╔══════════════════════════════════════════════════════════════════════════════╗
    echo ║                        🌟 ميزات النظام المحمول                             ║
    echo ║                        🌟 Portable System Features                         ║
    echo ╚══════════════════════════════════════════════════════════════════════════════╝
    echo.
    echo 💻 يعمل بدون إنترنت
    echo    Works without internet
    echo.
    echo 📱 متوافق مع جميع الأجهزة
    echo    Compatible with all devices
    echo.
    echo 💾 حفظ محلي للبيانات
    echo    Local data storage
    echo.
    echo 🔒 أمان كامل للبيانات
    echo    Complete data security
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                          📚 كيفية الاستخدام                                ║
echo ║                          📚 How to Use                                     ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo 1️⃣ سجل الدخول بالبيانات المعروضة أعلاه
echo    Login with credentials shown above
echo.
echo 2️⃣ استخدم التبويبات للتنقل بين الأقسام
echo    Use tabs to navigate between sections
echo.
echo 3️⃣ أضف الطلاب والمعلمين والفصول
echo    Add students, teachers, and classes
echo.

if "%system_file%"=="excellence_academy_enhanced.html" (
    echo 4️⃣ جرب ميزة تحليل الملفات الجديدة
    echo    Try the new file analysis feature
    echo.
    echo 5️⃣ اسحب الصور وملفات PDF لتحليلها
    echo    Drag images and PDF files to analyze them
)

echo.
goto :end

:manual_instructions
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                          📋 تعليمات التشغيل اليدوي                         ║
echo ║                          📋 Manual Launch Instructions                     ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo 🔧 طرق التشغيل اليدوي:
echo 🔧 Manual launch methods:
echo.
echo 1️⃣ انقر بالزر الأيمن على الملف: %system_file%
echo    Right-click on file: %system_file%
echo.
echo 2️⃣ اختر "فتح باستخدام" ← "اختيار تطبيق آخر"
echo    Choose "Open with" ← "Choose another app"
echo.
echo 3️⃣ اختر أي متصفح متاح (Chrome, Firefox, Edge, إلخ)
echo    Select any available browser (Chrome, Firefox, Edge, etc)
echo.
echo 4️⃣ أو اسحب الملف إلى نافذة متصفح مفتوحة
echo    Or drag the file to an open browser window
echo.
echo 5️⃣ أو انسخ مسار الملف إلى شريط عنوان المتصفح
echo    Or copy file path to browser address bar
echo.
echo 📁 مسار الملف الكامل:
echo 📁 Full file path:
echo %~dp0%system_file%
echo.

:end
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🏆 أكاديمية التميز الدولية                             ║
echo ║                Excellence International Academy                             ║
echo ║                        نحو مستقبل أفضل مع التكنولوجيا                      ║
echo ║                    Towards a Better Future with Technology                 ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo لإعادة تشغيل النظام، انقر نقراً مزدوجاً على هذا الملف
echo To restart system, double-click this file
echo.
pause
