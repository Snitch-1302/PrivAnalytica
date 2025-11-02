@echo off
echo Starting Encrypted Analytics-as-a-Service System...
echo.

echo Starting Backend Server...
start "Backend Server" cmd /k "python start_backend.py"

echo Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo Starting Frontend Server...
start "Frontend Server" cmd /k "python start_frontend.py"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause > nul
