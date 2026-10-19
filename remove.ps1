#A simple removal script for the auto-pruner
Write-Output "Removing Auto-Pruner, please wait..."

#Removing folder from Program Files
Write-Output "Removing application directory..."
$destinationDir = "$env:ProgramFiles\Pruner\"
Remove-Item -Path "$destinationDir" -Recurse -Force

#Remove desktop shortcut
Write-Output "Removing desktop shortcut..."
Remove-Item -Path "$env:USERPROFILE\Desktop\prune.lnk"

#Remove Task Scheduler task
Write-Output "Removing daily task..."
Get-ScheduledTask -TaskName "Daily Auto-Prune" -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false

Write-Output "Auto-Prune removed from system successfully!"
Write-Host "Press any key to continue..." -NoNewline
$null = [Console]::ReadKey($true)