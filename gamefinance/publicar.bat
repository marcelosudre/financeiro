@echo off
REM Script para publicar o GameFinance em um novo repositório

echo ================================================================
echo   GameFinance - Script de Publicacao
echo ================================================================
echo.

REM Verificar se estamos na pasta correta
if not exist "app" (
    echo Erro: Execute este script de dentro da pasta gamefinance/
    pause
    exit /b 1
)

echo Pasta correta detectada!
echo.

REM Verificar se já é um repositório git
if exist ".git" (
    echo Ja existe um repositorio git aqui.
    echo Se quiser recomecar, delete a pasta .git primeiro
    pause
    exit /b 1
)

echo Iniciando novo repositorio git...
git init

echo Adicionando arquivos...
git add .

echo Fazendo commit inicial...
git commit -m "Initial commit - GameFinance: Sistema de controle financeiro gamer"

echo Criando branch main...
git branch -M main

echo.
echo ================================================================
echo   Repositorio Git Inicializado!
echo ================================================================
echo.
echo PROXIMOS PASSOS:
echo.
echo 1. Crie o repositorio no GitHub:
echo    https://github.com/new
echo    Nome: gamefinance
echo    (NAO marque nenhuma opcao de inicializacao)
echo.
echo 2. Execute estes comandos (substitua SEU_USUARIO):
echo.
echo    git remote add origin https://github.com/SEU_USUARIO/gamefinance.git
echo    git push -u origin main
echo.
echo ================================================================
echo   GameFinance pronto para publicar!
echo ================================================================
echo.
pause
