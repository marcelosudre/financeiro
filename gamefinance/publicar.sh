#!/bin/bash
# Script para publicar o GameFinance em um novo repositório

echo "════════════════════════════════════════════════════════════"
echo "  🎮 GameFinance - Script de Publicação 🎮"
echo "════════════════════════════════════════════════════════════"
echo ""

# Verificar se estamos na pasta correta
if [ ! -d "app" ]; then
    echo "❌ Erro: Execute este script de dentro da pasta gamefinance/"
    exit 1
fi

echo "✅ Pasta correta detectada!"
echo ""

# Verificar se já é um repositório git
if [ -d ".git" ]; then
    echo "⚠️  Já existe um repositório git aqui."
    echo "   Se quiser recomeçar, delete a pasta .git primeiro:"
    echo "   rm -rf .git"
    exit 1
fi

echo "📝 Iniciando novo repositório git..."
git init

echo "➕ Adicionando arquivos..."
git add .

echo "💾 Fazendo commit inicial..."
git commit -m "🎮 Initial commit - GameFinance: Sistema de controle financeiro gamer"

echo "🌿 Criando branch main..."
git branch -M main

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  ✅ Repositório Git Inicializado!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo ""
echo "1. Crie o repositório no GitHub:"
echo "   https://github.com/new"
echo "   Nome: gamefinance"
echo "   (NÃO marque nenhuma opção de inicialização)"
echo ""
echo "2. Execute estes comandos (substitua SEU_USUARIO):"
echo ""
echo "   git remote add origin https://github.com/SEU_USUARIO/gamefinance.git"
echo "   git push -u origin main"
echo ""
echo "════════════════════════════════════════════════════════════"
echo "  🎮 GameFinance pronto para publicar! 🏆"
echo "════════════════════════════════════════════════════════════"
