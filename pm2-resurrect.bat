@echo off
REM PM2 Auto-Resurrect on Windows Startup
REM This script restores all PM2 processes saved in dump.pm2

echo [PM2] Starting auto-resurrect...
cd "C:\Users\14loa\Desktop\IT\GIAIC\Q4 spec kit\Hackathon0Gold"
pm2 resurrect
echo [PM2] Processes restored from dump.pm2
