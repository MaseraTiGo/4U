@ECHO OFF
powershell.exe -command "Get-Childitem -path '.\' -Recurse | foreach-object { $_.LastWriteTime = '06/21/2019 14:23:36'; $_.CreationTime = Get-Date }" 
PAUSE
