#A simple setup script for the auto-pruner
Write-Output "Installing Auto-Pruner, please wait..."

#Create folder in Program Files
Write-Output "Creating application directory..."
$destinationDir = "$env:ProgramFiles\Pruner\"
New-Item -Path $destinationDir -ItemType Directory -Force

#Move application
Write-Output "Installing application..."
$application = "dist\prune.exe"
Copy-Item -Path $application -Destination "$destinationDir"

#Create shortcut on the desktop
Write-Output "Creating desktop shortcut..."
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut("$env:USERPROFILE\Desktop\prune.lnk")
$shortcut.TargetPath = "$destinationDir\prune.exe"
$shortcut.WorkingDirectory = "$destinationDir"
$shortcut.Save()

#Set up task scheduler task
Write-Output "Setting up task..."
$Action = New-ScheduledTaskAction -Execute "$destinationDir\prune.exe" ` -WorkingDirectory "$destinationDir"

$Trigger = New-ScheduledTaskTrigger -Daily -At 8:00AM #Define when the task will run

$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest #Run as SYSTEM with highest privileges

#Register the task in Task Scheduler
Register-ScheduledTask `
    -TaskName "Daily Auto-Prune" `
    -Action $Action `
    -Trigger $Trigger `
    -Principal $Principal `
    -Description "Automatically prune from user-selected directory."

Write-Output "Auto-Prune installed successfully!"
Write-Host "Press any key to continue..." -NoNewline
$null = [Console]::ReadKey($true)