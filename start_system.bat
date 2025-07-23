@echo off
echo ========================================
echo    نظام الإدارة المتكامل
echo    Integrated Management System
echo ========================================
echo.
echo تشغيل النظام... | Starting system...
echo.

REM Try different Python commands
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Python found, installing requirements...
    python -m pip install streamlit pandas numpy plotly openpyxl pillow python-dateutil requests
    echo.
    echo Starting Streamlit...
    python -m streamlit run odoo_like_system.py
) else (
    py --version >nul 2>&1
    if %errorlevel% == 0 (
        echo Python found with 'py' command, installing requirements...
        py -m pip install streamlit pandas numpy plotly openpyxl pillow python-dateutil requests
        echo.
        echo Starting Streamlit...
        py -m streamlit run odoo_like_system.py
    ) else (
        echo Python not found! Please install Python first.
        echo يرجى تثبيت Python أولاً
        pause
    )
)

pause
