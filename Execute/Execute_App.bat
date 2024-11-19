@echo off
echo Iniciando detección de EPP...
start powershell -NoExit -Command "python C:\Users\ASUS\Desktop\SafeSight_AI-master\Python_code\detectar_epp.py"
timeout /t 5 /nobreak >nul
echo Iniciando Streamlit para visualización en tiempo real...
start powershell -NoExit -Command "streamlit run C:\Users\ASUS\Desktop\SafeSight_AI-master\Python_code\App.py"
pause
