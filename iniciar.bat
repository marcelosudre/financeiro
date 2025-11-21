@echo off
REM Script para iniciar o sistema de controle financeiro
REM Executar este arquivo para abrir a aplicação

echo.
echo ===============================================
echo   Controle Financeiro Familiar
echo ===============================================
echo.

REM Verificar se está na pasta correta
if not exist "app\app.py" (
    echo Erro: Arquivo app.py não encontrado!
    echo Execute este script da pasta raiz do projeto.
    pause
    exit /b 1
)

REM Instalar dependências se necessário
echo Verificando dependências...
pip install -r requirements.txt > nul 2>&1

REM Iniciar o servidor
echo.
echo Iniciando servidor...
echo.
cd app
python app.py

pause
