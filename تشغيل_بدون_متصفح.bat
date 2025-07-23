@echo off
chcp 65001 >nul
color 0E
title 🏆 أكاديمية التميز الدولية - تشغيل بدون متصفح
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🏆 أكاديمية التميز الدولية                             ║
echo ║                Excellence International Academy                             ║
echo ║                        تشغيل بدون متصفح منفصل                             ║
echo ║                    Running without Separate Browser                        ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo 🔍 البحث عن متصفح متاح...
echo 🔍 Searching for available browser...
echo.

REM Try different browsers in order of preference
set "found_browser="

REM Check for Chrome
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    set "found_browser=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
    echo ✅ تم العثور على Google Chrome
    echo ✅ Found Google Chrome
    goto :run_browser
)

if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
    set "found_browser=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
    echo ✅ تم العثور على Google Chrome
    echo ✅ Found Google Chrome
    goto :run_browser
)

REM Check for Edge
if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" (
    set "found_browser=%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
    echo ✅ تم العثور على Microsoft Edge
    echo ✅ Found Microsoft Edge
    goto :run_browser
)

if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
    set "found_browser=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
    echo ✅ تم العثور على Microsoft Edge
    echo ✅ Found Microsoft Edge
    goto :run_browser
)

REM Check for Firefox
if exist "%ProgramFiles%\Mozilla Firefox\firefox.exe" (
    set "found_browser=%ProgramFiles%\Mozilla Firefox\firefox.exe"
    echo ✅ تم العثور على Mozilla Firefox
    echo ✅ Found Mozilla Firefox
    goto :run_browser
)

if exist "%ProgramFiles(x86)%\Mozilla Firefox\firefox.exe" (
    set "found_browser=%ProgramFiles(x86)%\Mozilla Firefox\firefox.exe"
    echo ✅ تم العثور على Mozilla Firefox
    echo ✅ Found Mozilla Firefox
    goto :run_browser
)

REM Check for Internet Explorer (fallback)
if exist "%ProgramFiles%\Internet Explorer\iexplore.exe" (
    set "found_browser=%ProgramFiles%\Internet Explorer\iexplore.exe"
    echo ⚠️ تم العثور على Internet Explorer (قديم)
    echo ⚠️ Found Internet Explorer (legacy)
    goto :run_browser
)

if exist "%ProgramFiles(x86)%\Internet Explorer\iexplore.exe" (
    set "found_browser=%ProgramFiles(x86)%\Internet Explorer\iexplore.exe"
    echo ⚠️ تم العثور على Internet Explorer (قديم)
    echo ⚠️ Found Internet Explorer (legacy)
    goto :run_browser
)

REM Try Windows default browser
echo 🔄 محاولة فتح المتصفح الافتراضي...
echo 🔄 Trying to open default browser...
start "" "excellence_academy_enhanced.html"
goto :show_instructions

:run_browser
echo.
echo 🚀 تشغيل النظام باستخدام المتصفح المتاح...
echo 🚀 Starting system with available browser...
echo.

REM Get full path to HTML file
set "html_file=%~dp0excellence_academy_enhanced.html"

REM Start browser with the HTML file
"%found_browser%" "%html_file%"

:show_instructions
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                          ✅ تم تشغيل النظام بنجاح                          ║
echo ║                          ✅ System Started Successfully                     ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo 🔐 بيانات تسجيل الدخول:
echo 🔐 Login Credentials:
echo.
echo 👤 اسم المستخدم: admin
echo 👤 Username: admin
echo.
echo 🔑 كلمة المرور: 123456
echo 🔑 Password: 123456
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                          🌟 ميزات النظام المحسن                            ║
echo ║                          🌟 Enhanced System Features                       ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo 🔍 تحليل الصور واستخراج النصوص
echo    Image Analysis & Text Extraction
echo.
echo 📄 تحليل ملفات PDF وكشف المحتوى
echo    PDF Analysis & Content Detection
echo.
echo 📝 تحليل المستندات النصية
echo    Document Text Analysis
echo.
echo 🤖 ذكاء اصطناعي متقدم للتحليل
echo    Advanced AI for Analysis
echo.
echo 💾 حفظ تلقائي للبيانات والنتائج
echo    Auto-save Data & Results
echo.
echo 🌐 دعم كامل للعربية والإنجليزية
echo    Full Arabic & English Support
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                          📚 أقسام النظام                                   ║
echo ║                          📚 System Sections                                ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo 1️⃣  📊 نظرة عامة - إحصائيات ورسوم بيانية
echo     Overview - Statistics & Charts
echo.
echo 2️⃣  👨‍🎓 إدارة الطلاب - مع رفع وتحليل الملفات
echo     Student Management - with File Upload & Analysis
echo.
echo 3️⃣  🔍 تحليل الملفات - ميزة جديدة متقدمة!
echo     File Analysis - New Advanced Feature!
echo     ├── 📸 تحليل الصور (OCR)
echo     ├── 📄 تحليل PDF
echo     └── 📝 تحليل المستندات
echo.
echo 4️⃣  👨‍🏫 إدارة المعلمين (قيد التطوير)
echo     Teacher Management (Under Development)
echo.
echo 5️⃣  🚪 إدارة الفصول (قيد التطوير)
echo     Class Management (Under Development)
echo.
echo 6️⃣  📈 التقارير (قيد التطوير)
echo     Reports (Under Development)
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                          🔧 تعليمات الاستخدام                             ║
echo ║                          🔧 Usage Instructions                             ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo 🔐 تسجيل الدخول:
echo    البيانات معبأة مسبقاً، انقر "تسجيل الدخول"
echo    Credentials pre-filled, click "Login"
echo.
echo 🌐 تغيير اللغة:
echo    زر اللغة في الزاوية العلوية
echo    Language button in top corner
echo.
echo 🔍 تحليل الملفات:
echo    انتقل لتبويب "تحليل الملفات" واسحب الملفات
echo    Go to "File Analysis" tab and drag files
echo.
echo 👨‍🎓 إضافة طالب:
echo    املأ النموذج واسحب ملفات الطالب للتحليل
echo    Fill form and drag student files for analysis
echo.
echo 📊 مراقبة الإحصائيات:
echo    تحديث تلقائي في تبويب "نظرة عامة"
echo    Auto-update in "Overview" tab
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                          📁 أنواع الملفات المدعومة                         ║
echo ║                          📁 Supported File Types                           ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo 🖼️ الصور: JPG, PNG, GIF, BMP, WEBP
echo    Images: JPG, PNG, GIF, BMP, WEBP
echo.
echo 📄 ملفات PDF: جميع الإصدارات
echo    PDF Files: All versions
echo.
echo 📝 المستندات: DOC, DOCX, TXT, RTF
echo    Documents: DOC, DOCX, TXT, RTF
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                          ⚠️ ملاحظات مهمة                                  ║
echo ║                          ⚠️ Important Notes                                ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo 🌐 يحتاج اتصال إنترنت لتحميل مكتبات التحليل (مرة واحدة)
echo    Needs internet to load analysis libraries (once)
echo.
echo 💾 البيانات تُحفظ محلياً في المتصفح
echo    Data is saved locally in browser
echo.
echo 🔒 لا يتم إرسال أي بيانات لخوادم خارجية
echo    No data sent to external servers
echo.
echo 📱 يعمل على جميع الأجهزة والمتصفحات
echo    Works on all devices and browsers
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                          🆘 حل المشاكل                                     ║
echo ║                          🆘 Troubleshooting                                ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo ❌ إذا لم يفتح النظام:
echo    If system doesn't open:
echo.
echo 1️⃣ انقر بالزر الأيمن على الملف excellence_academy_enhanced.html
echo    Right-click on excellence_academy_enhanced.html
echo.
echo 2️⃣ اختر "فتح باستخدام" ثم اختر أي متصفح متاح
echo    Choose "Open with" then select any available browser
echo.
echo 3️⃣ أو اسحب الملف إلى نافذة متصفح مفتوحة
echo    Or drag the file to an open browser window
echo.
echo ❌ إذا كان التحليل لا يعمل:
echo    If analysis doesn't work:
echo.
echo 1️⃣ تأكد من الاتصال بالإنترنت
echo    Make sure you have internet connection
echo.
echo 2️⃣ انتظر قليلاً لتحميل المكتبات
echo    Wait a bit for libraries to load
echo.
echo 3️⃣ جرب إعادة تحميل الصفحة
echo    Try refreshing the page
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🏆 أكاديمية التميز الدولية                             ║
echo ║                Excellence International Academy                             ║
echo ║                        نحو مستقبل أفضل مع التكنولوجيا                      ║
echo ║                    Towards a Better Future with Technology                 ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo النظام يعمل الآن! استمتع بالإدارة المتطورة
echo System is running! Enjoy advanced management
echo.
echo لإعادة تشغيل النظام، انقر نقراً مزدوجاً على هذا الملف
echo To restart system, double-click this file
echo.
pause
