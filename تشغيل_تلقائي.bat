@echo off
chcp 65001 >nul
color 0B
title 🏆 أكاديمية التميز - تشغيل تلقائي
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                🏆 أكاديمية التميز الدولية                   ║
echo ║            Excellence International Academy                   ║
echo ║                    تشغيل تلقائي ذكي                         ║
echo ║                 Smart Auto Launch                            ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo 🔍 البحث عن أفضل طريقة لتشغيل النظام...
echo 🔍 Finding best way to run the system...
echo.

REM Method 1: Try Windows default file association
echo 📂 المحاولة الأولى: فتح بالطريقة الافتراضية...
echo 📂 First attempt: Opening with default method...
start "" "excellence_academy_enhanced.html" 2>nul
if %errorlevel% equ 0 (
    echo ✅ تم فتح النظام بنجاح!
    echo ✅ System opened successfully!
    goto :success
)

REM Method 2: Try with rundll32
echo 🔄 المحاولة الثانية: استخدام rundll32...
echo 🔄 Second attempt: Using rundll32...
rundll32 url.dll,FileProtocolHandler "%~dp0excellence_academy_enhanced.html" 2>nul
if %errorlevel% equ 0 (
    echo ✅ تم فتح النظام بنجاح!
    echo ✅ System opened successfully!
    goto :success
)

REM Method 3: Try PowerShell
echo 🔄 المحاولة الثالثة: استخدام PowerShell...
echo 🔄 Third attempt: Using PowerShell...
powershell -command "Start-Process '%~dp0excellence_academy_enhanced.html'" 2>nul
if %errorlevel% equ 0 (
    echo ✅ تم فتح النظام بنجاح!
    echo ✅ System opened successfully!
    goto :success
)

REM Method 4: Manual browser detection
echo 🔍 المحاولة الرابعة: البحث عن متصفح يدوياً...
echo 🔍 Fourth attempt: Manual browser detection...

REM Check for Chrome
for %%i in (
    "%ProgramFiles%\Google\Chrome\Application\chrome.exe"
    "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
    "%LocalAppData%\Google\Chrome\Application\chrome.exe"
) do (
    if exist "%%i" (
        echo ✅ تم العثور على Chrome
        echo ✅ Found Chrome
        "%%i" "%~dp0excellence_academy_enhanced.html"
        goto :success
    )
)

REM Check for Edge
for %%i in (
    "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
    "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
) do (
    if exist "%%i" (
        echo ✅ تم العثور على Edge
        echo ✅ Found Edge
        "%%i" "%~dp0excellence_academy_enhanced.html"
        goto :success
    )
)

REM Check for Firefox
for %%i in (
    "%ProgramFiles%\Mozilla Firefox\firefox.exe"
    "%ProgramFiles(x86)%\Mozilla Firefox\firefox.exe"
) do (
    if exist "%%i" (
        echo ✅ تم العثور على Firefox
        echo ✅ Found Firefox
        "%%i" "%~dp0excellence_academy_enhanced.html"
        goto :success
    )
)

REM Method 5: Try Internet Explorer as last resort
if exist "%ProgramFiles%\Internet Explorer\iexplore.exe" (
    echo ⚠️ استخدام Internet Explorer (قديم)
    echo ⚠️ Using Internet Explorer (legacy)
    "%ProgramFiles%\Internet Explorer\iexplore.exe" "%~dp0excellence_academy_enhanced.html"
    goto :success
)

if exist "%ProgramFiles(x86)%\Internet Explorer\iexplore.exe" (
    echo ⚠️ استخدام Internet Explorer (قديم)
    echo ⚠️ Using Internet Explorer (legacy)
    "%ProgramFiles(x86)%\Internet Explorer\iexplore.exe" "%~dp0excellence_academy_enhanced.html"
    goto :success
)

REM If all methods fail
echo.
echo ❌ لم يتم العثور على متصفح مناسب
echo ❌ No suitable browser found
echo.
echo 📋 تعليمات التشغيل اليدوي:
echo 📋 Manual launch instructions:
echo.
echo 1️⃣ انقر بالزر الأيمن على الملف: excellence_academy_enhanced.html
echo    Right-click on file: excellence_academy_enhanced.html
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
goto :end

:success
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    ✅ تم تشغيل النظام بنجاح                   ║
echo ║                    ✅ System Started Successfully              ║
echo ╚════════════════════════════════════════════════════════════════╝
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
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    🚀 ميزات النظام الجديدة                   ║
echo ║                    🚀 New System Features                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 🔍 تحليل الصور بالذكاء الاصطناعي
echo    AI-Powered Image Analysis
echo.
echo 📄 استخراج النصوص من PDF
echo    PDF Text Extraction
echo.
echo 📝 تحليل المستندات النصية
echo    Document Text Analysis
echo.
echo 🤖 تقنيات OCR متقدمة
echo    Advanced OCR Technologies
echo.
echo 💾 حفظ تلقائي للنتائج
echo    Auto-save Results
echo.
echo 🌐 دعم العربية والإنجليزية
echo    Arabic & English Support
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    📚 كيفية الاستخدام                        ║
echo ║                    📚 How to Use                              ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 1️⃣ سجل الدخول بالبيانات المعروضة أعلاه
echo    Login with credentials shown above
echo.
echo 2️⃣ انتقل لتبويب "تحليل الملفات" لتجربة الميزات الجديدة
echo    Go to "File Analysis" tab to try new features
echo.
echo 3️⃣ اسحب الصور أو ملفات PDF لتحليلها
echo    Drag images or PDF files to analyze them
echo.
echo 4️⃣ اعرض النتائج واستخرج النصوص
echo    View results and extract texts
echo.
echo 5️⃣ أضف طلاب جدد مع ملفاتهم في تبويب "الطلاب"
echo    Add new students with their files in "Students" tab
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    💡 نصائح للاستخدام الأمثل                 ║
echo ║                    💡 Tips for Best Usage                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 🌐 تأكد من الاتصال بالإنترنت لتحميل مكتبات التحليل
echo    Ensure internet connection to load analysis libraries
echo.
echo 📸 استخدم صور واضحة عالية الجودة للحصول على أفضل نتائج OCR
echo    Use clear, high-quality images for best OCR results
echo.
echo 📄 ملفات PDF النصية تعطي نتائج أفضل من الصور الممسوحة
echo    Text-based PDFs give better results than scanned images
echo.
echo 💾 البيانات تُحفظ تلقائياً كل 30 ثانية
echo    Data auto-saves every 30 seconds
echo.
echo 🔄 أعد تحميل الصفحة إذا واجهت أي مشكلة
echo    Refresh page if you encounter any issues
echo.

:end
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                🏆 أكاديمية التميز الدولية                   ║
echo ║            Excellence International Academy                   ║
echo ║                نحو مستقبل أفضل مع التكنولوجيا                ║
echo ║            Towards a Better Future with Technology           ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo استمتع بالنظام المتطور!
echo Enjoy the advanced system!
echo.
pause
