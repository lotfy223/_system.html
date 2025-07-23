@echo off
color 0A
title Excellence Academy Server
echo.
echo ========================================
echo    🏆 أكاديمية التميز الدولية
echo    Excellence International Academy
echo    🌐 خادم النظام المحلي
echo ========================================
echo.

echo 🚀 تشغيل الخادم المحلي...
echo 🚀 Starting Local Server...
echo.

REM Try different methods to start a local server
echo 📡 محاولة تشغيل خادم Python...
echo 📡 Trying Python server...

python -m http.server 8080 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python غير متوفر، جاري المحاولة بطريقة أخرى...
    echo ❌ Python not available, trying alternative...
    
    REM Try with Node.js if available
    echo 📡 محاولة تشغيل خادم Node.js...
    echo 📡 Trying Node.js server...
    
    echo const http = require('http'); > temp_server.js
    echo const fs = require('fs'); >> temp_server.js
    echo const path = require('path'); >> temp_server.js
    echo const server = http.createServer((req, res) => { >> temp_server.js
    echo   let filePath = '.' + req.url; >> temp_server.js
    echo   if (filePath === './') filePath = './excellence_academy_system.html'; >> temp_server.js
    echo   const extname = path.extname(filePath); >> temp_server.js
    echo   let contentType = 'text/html'; >> temp_server.js
    echo   if (extname === '.js') contentType = 'text/javascript'; >> temp_server.js
    echo   if (extname === '.css') contentType = 'text/css'; >> temp_server.js
    echo   fs.readFile(filePath, (err, content) => { >> temp_server.js
    echo     if (err) { res.writeHead(404); res.end('File not found'); return; } >> temp_server.js
    echo     res.writeHead(200, { 'Content-Type': contentType }); >> temp_server.js
    echo     res.end(content, 'utf-8'); >> temp_server.js
    echo   }); >> temp_server.js
    echo }); >> temp_server.js
    echo server.listen(8080, () => console.log('Server running on http://localhost:8080')); >> temp_server.js
    
    node temp_server.js 2>nul
    if %errorlevel% neq 0 (
        echo ❌ Node.js غير متوفر، فتح الملف مباشرة...
        echo ❌ Node.js not available, opening file directly...
        
        REM Open file directly in browser
        start "" "excellence_academy_system.html"
        
        echo.
        echo ✅ تم فتح النظام مباشرة في المتصفح!
        echo ✅ System opened directly in browser!
        echo.
        echo 🌐 النظام يعمل الآن محلياً
        echo 🌐 System is now running locally
        echo.
        goto :show_info
    ) else (
        echo ✅ تم تشغيل خادم Node.js بنجاح!
        echo ✅ Node.js server started successfully!
        echo.
        echo 🌐 النظام متاح على: http://localhost:8080
        echo 🌐 System available at: http://localhost:8080
        echo.
        start "" "http://localhost:8080"
        goto :show_info
    )
) else (
    echo ✅ تم تشغيل خادم Python بنجاح!
    echo ✅ Python server started successfully!
    echo.
    echo 🌐 النظام متاح على: http://localhost:8080
    echo 🌐 System available at: http://localhost:8080
    echo.
    start "" "http://localhost:8080"
    goto :show_info
)

:show_info
echo ========================================
echo 🔐 بيانات تسجيل الدخول:
echo 🔐 Login Credentials:
echo ========================================
echo.
echo 👤 اسم المستخدم: excellence_admin
echo 👤 Username: excellence_admin
echo.
echo 🔑 كلمة المرور: Excellence@2024
echo 🔑 Password: Excellence@2024
echo.
echo ========================================
echo 🎯 ميزات النظام المتاحة:
echo 🎯 Available System Features:
echo ========================================
echo.
echo ✨ دعم كامل للعربية والإنجليزية
echo ✨ رفع الصور والملفات لكل قسم
echo ✨ حفظ البيانات لمدة سنة كاملة
echo ✨ رسوم بيانية تفاعلية متقدمة
echo ✨ تصدير Excel و PDF احترافي
echo ✨ نسخ احتياطي تلقائي للبيانات
echo ✨ تصميم احترافي متجاوب
echo.
echo ========================================
echo 📱 متوافق مع جميع الأجهزة:
echo 📱 Compatible with All Devices:
echo ========================================
echo.
echo 💻 أجهزة الكمبيوتر
echo 📱 الهواتف الذكية
echo 📟 الأجهزة اللوحية
echo 🌐 جميع المتصفحات
echo.
echo ========================================
echo 🔄 لإيقاف الخادم:
echo 🔄 To Stop Server:
echo ========================================
echo.
echo اضغط Ctrl+C في هذه النافذة
echo Press Ctrl+C in this window
echo.
echo أو أغلق هذه النافذة مباشرة
echo Or close this window directly
echo.
echo ========================================
echo 🏆 أكاديمية التميز الدولية
echo 🏆 Excellence International Academy
echo ========================================
echo.
echo النظام يعمل الآن! استمتع بالإدارة المتميزة
echo System is running! Enjoy excellent management
echo.

REM Keep the window open
if exist temp_server.js (
    echo 📡 خادم Node.js يعمل... اتركه مفتوحاً
    echo 📡 Node.js server running... keep it open
    echo.
    node temp_server.js
) else (
    echo 📁 النظام مفتوح مباشرة في المتصفح
    echo 📁 System opened directly in browser
    echo.
    pause
)

REM Cleanup
if exist temp_server.js del temp_server.js
