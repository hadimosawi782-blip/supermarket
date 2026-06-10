@echo off
title نصب پیش‌نیازهای ویندوز 7
echo =====================================
echo    نصب Visual C++ Redistributable
echo =====================================
echo.
echo در حال دانلود و نصب...
echo.

:: دانلود و نصب VC++ 2015-2022
powershell -Command "Invoke-WebRequest -Uri 'https://aka.ms/vs/17/release/vc_redist.x64.exe' -OutFile 'vc_redist.exe'"

if exist vc_redist.exe (
    echo ✅ فایل دانلود شد
    echo در حال نصب...
    vc_redist.exe /quiet /norestart
    echo ✅ نصب انجام شد
    del vc_redist.exe
) else (
    echo ❌ خطا در دانلود
    echo لطفاً از لینک زیر دانلود و نصب کنید:
    echo https://aka.ms/vs/17/release/vc_redist.x64.exe
)

echo.
pause