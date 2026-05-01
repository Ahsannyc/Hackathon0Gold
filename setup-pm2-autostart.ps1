# PowerShell script to set up PM2 auto-resurrection on Windows startup
# Run as Administrator

$taskName = "PM2-Auto-Resurrect"
$scriptPath = "C:\Users\14loa\Desktop\IT\GIAIC\Q4 spec kit\Hackathon0Gold\pm2-resurrect.bat"
$taskDescription = "Automatically resurrect PM2 processes on system startup"

# Check if running as admin
$isAdmin = [Security.Principal.WindowsPrincipal]::new([Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator" -ForegroundColor Red
    exit 1
}

Write-Host "Setting up Windows Task Scheduler for PM2 auto-start..." -ForegroundColor Green

# Remove existing task if present
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Removing existing task '$taskName'..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create trigger for system startup
$trigger = New-ScheduledTaskTrigger -AtStartup

# Create action to run the batch script
$action = New-ScheduledTaskAction -Execute $scriptPath

# Create task settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

# Register the scheduled task
Register-ScheduledTask -TaskName $taskName `
    -Trigger $trigger `
    -Action $action `
    -Settings $settings `
    -Description $taskDescription `
    -RunLevel Highest `
    -Force

Write-Host "✅ Task created successfully!" -ForegroundColor Green
Write-Host "Task Name: $taskName" -ForegroundColor Cyan
Write-Host "Trigger: At System Startup" -ForegroundColor Cyan
Write-Host "Action: $scriptPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "All 5 watchers will now auto-start on system reboot:" -ForegroundColor Yellow
Write-Host "  - facebook-watcher" -ForegroundColor Green
Write-Host "  - gmail-watcher" -ForegroundColor Green
Write-Host "  - whatsapp-watcher" -ForegroundColor Green
Write-Host "  - linkedin-watcher" -ForegroundColor Green
Write-Host "  - instagram-watcher" -ForegroundColor Green
