# Script para iniciar o sistema de controle financeiro

Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host "   Controle Financeiro Familiar" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

# Verificar se está na pasta correta
if (-not (Test-Path "app\app.py")) {
    Write-Host "Erro: Arquivo app.py não encontrado!" -ForegroundColor Red
    Write-Host "Execute este script da pasta raiz do projeto." -ForegroundColor Red
    Read-Host "Pressione Enter para fechar"
    exit 1
}

# Instalar dependências se necessário
Write-Host "Verificando dependências..." -ForegroundColor Yellow
pip install -r requirements.txt | Out-Null

# Iniciar o servidor
Write-Host ""
Write-Host "Iniciando servidor..." -ForegroundColor Cyan
Write-Host ""

Set-Location app
python app.py

Read-Host "Pressione Enter para fechar"
