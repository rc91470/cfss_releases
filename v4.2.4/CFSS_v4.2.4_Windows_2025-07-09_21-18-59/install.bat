@echo off 
REM CFSS Installation Script 
echo Installing CFSS v4.2.4... 
if not exist "C:\Program Files\CFSS" mkdir "C:\Program Files\CFSS" 
copy "CFSS_v4.2.4.exe" "C:\Program Files\CFSS\" 
copy "data\*.*" "C:\Program Files\CFSS\data\" 
copy "sounds\*.*" "C:\Program Files\CFSS\sounds\" 
echo CFSS installed successfully! 
echo You can run it from: C:\Program Files\CFSS\CFSS_v4.2.4.exe 
pause 
