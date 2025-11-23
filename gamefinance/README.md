# 🎮 GameFinance - Controle Financeiro Gamer

Um aplicativo web épico e gamificado para gerenciar suas finanças pessoais como um verdadeiro gamer! Transforme o controle de gastos em uma quest empolgante com sistema de XP, Gold e conquistas. Design moderno com tema gamer em tons de roxo, ciano e verde neon.

## ✨ Features Épicas

### 🎮 Gerenciamento Financeiro Gamificado
- **Registrar Quests Financeiras**: Adicione seus gastos de Gold e ganhos de XP com categorias temáticas
- **Sistema de Conquistas**: Marque suas transações como concluídas (pagas) ou pendentes
- **Dashboard de Status do Jogador**:
  - Total de Gold gasto e XP ganho por mês
  - Fluxo de recursos (cashflow)
  - Saldo final (XP ganho - Gold gasto)
  - Análise por categoria de quest
- **Filtros de Batalha**: Filtre por tipo (gasto/ganho), status (pago/pendente) e mês
- **Relatório de Conquistas em PDF**: Gere relatórios épicos do seu progresso financeiro mensal
- **Importação de Save Game**: Importe transações anteriores do seu CSV de planejamento

### 🎒 Inventário de Compras
- **Múltiplas Quest Lists**: Crie listas para diferentes missões de compras
- **Sistema de Check**: Marque itens como conquistados
- **Gerenciamento de Items**: Adicione, remova e organize items do seu inventário

## 🎨 Design Gamer Épico
- Interface estilo gaming com tons de roxo (#6B46C1, #7C3AED), ciano neon (#00FFFF) e verde (#00FF41)
- Background dark mode inspirado em games (#0F0F23, #1A1A2E)
- Responsiva para desktop, tablet e mobile
- Animações e efeitos visuais tipo game UI
- Visual inspirado em RPGs e jogos de estratégia

## 🚀 Como Começar Sua Jornada

### 1. Instalação das Dependências (Level Up)

Abra o PowerShell ou terminal na pasta do projeto e execute:

```powershell
pip install -r requirements.txt
```

### 2. Importar Save Game Anterior (Opcional)

Se você tem um CSV de planejamento anterior, pode importar automaticamente:

```powershell
python importar_dados.py
```

Este script vai:
- Ler seu arquivo `PLANEJAMENTO FINANCEIRO.xlsx - 2025.csv`
- Categorizar automaticamente as transações
- Importar todas as quests financeiras para o banco de dados

### 3. Iniciar o Game (Rodar o Aplicativo)

Na pasta `app`, execute:

```powershell
python app.py
```

Você verá uma mensagem como:
```
 * Running on http://127.0.0.1:5000
```

### 4. Acessar no Navegador

Abra seu navegador e acesse: **http://127.0.0.1:5000**

## 📁 Estrutura do Projeto

```
gamefinance/
├── requirements.txt              # Dependências Python
├── importar_dados.py             # Script para importar CSV
├── README.md                     # Este arquivo
├── iniciar.bat                   # Script para iniciar (Windows)
├── iniciar.ps1                   # Script PowerShell (alternativa)
├── PLANEJAMENTO FINANCEIRO.xlsx - 2025.csv  # Seu CSV de dados (opcional)
└── app/
    ├── app.py                    # Aplicação Flask (backend + banco de dados)
    ├── financeiro.db             # Banco de dados (criado automaticamente)
    ├── static/                   # Arquivos estáticos (ícones, etc)
    └── templates/
        └── index.html            # Interface web (HTML + CSS + JavaScript)
```

## 💡 Como Usar Cada Feature

### 🎮 Adicionar Quest Financeira

1. Clique na aba **🎮 Financeiro Gamer**
2. Preencha o formulário "Adicionar Transação":
   - **Tipo**: Selecione "💰 Gasto de Gold" (Despesa) ou "⚡ XP Ganho" (Ganho)
   - **Descrição**: Nome da quest (ex: "Aluguel da Base", "Salário Mensal")
   - **Valor**: Quanto de gold gastou ou XP ganhou
   - **Categoria**: Selecione uma categoria temática (Moradia, Alimentação, etc)
   - **Data de Vencimento**: Prazo da quest
   - **Quest Completa?**: Marque se já completou (pagou/recebeu)
3. Clique em **Adicionar Transação**

### 📊 Ver Status do Jogador

No card "Status do Mês":
- Selecione o mês da campanha
- Visualize suas estatísticas calculadas automaticamente
- Veja a distribuição por categoria de quest
- Acompanhe seu saldo (XP ganho - Gold gasto)

### 📥 Exportar Relatório de Conquistas (PDF)

1. Selecione o mês desejado no card "Status do Mês"
2. Clique no botão **📥 Exportar PDF**
3. Um relatório épico será baixado com:
   - Resumo financeiro (gastos, ganhos, fluxo)
   - Lista completa de todas as quests
   - Tabelas formatadas por categoria

### 🔍 Filtrar Quests

Use os filtros na seção "Transações":
- **Tipo**: Todas, apenas Gastos de Gold ou apenas XP Ganho
- **Status**: Todas, apenas Pendentes ou apenas Concluídas
- **Mês**: Selecione o mês para visualizar

### ⚔️ Gerenciar Quests

Para cada transação/quest, você pode:
- **✅ Marcar Completa**: Clique se ainda não marcou como pago
- **↩️ Desfazer**: Clique se marcou errado como pago
- **🗑️ Deletar**: Remove a quest/transação

### 🎒 Criar Inventário de Compras

1. Clique na aba **🎒 Inventário**
2. Digite um título para sua quest (ex: "Compras do Mês", "Items do Mercado")
3. Clique em **Criar Lista**
4. Na lista criada:
   - Digite o item e clique em **+** para adicionar ao inventário
   - Marque o checkbox para marcar como conquistado/comprado
   - Clique em **Limpar Concluídos** para remover items coletados
   - Clique em **Deletar Lista** para remover a quest inteira

## 📊 Importar Save Game (CSV)

Seu arquivo `PLANEJAMENTO FINANCEIRO.xlsx - 2025.csv` será automaticamente reconhecido pelo script de importação.

**Para importar:**
```powershell
python importar_dados.py
```

O script irá:
- ✅ Ler seu CSV automáticamente
- ✅ Extrair todas as transações
- ✅ Categorizar automaticamente
- ✅ Importar ganhos e despesas
- ✅ Marcar como pago/pendente
- ✅ Salvar no banco de dados

**Resultado:**
```
Importação concluída!
✓ Transações importadas: 42
✗ Erros: 0
```

## 🔄 Multiplayer (Compartilhar na Rede)

Você pode acessar o aplicativo de outros computadores:

### Acessar de Outros Dispositivos na Mesma Rede

No arquivo `app/app.py`, altere a última linha de:
```python
app.run(debug=True, host='127.0.0.1', port=5000)
```

Para:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

Depois, acesse de outro computador usando o IP do seu computador:
- `http://SEU_IP:5000`
- Para descobrir seu IP, abra PowerShell e digite: `ipconfig`

### Modificar a Porta

Se a porta 5000 estiver em uso, altere para outra (ex: 8000):
```python
app.run(debug=True, host='127.0.0.1', port=8000)
```

## 💾 Save Game (Backup dos Dados)

Todos os dados são salvos em um banco de dados SQLite (`financeiro.db`) na pasta `app/`. 

**Backup**: Para fazer backup do seu save game, copie o arquivo `financeiro.db` para um local seguro.

**Restaurar**: Para restaurar, substitua o arquivo `financeiro.db` pelo backup.

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"

Execute:
```powershell
pip install -r requirements.txt
```

### "Address already in use"

A porta 5000 está em uso. Altere a porta em `app/app.py` ou feche o outro aplicativo.

### "Permission denied"

Execute o PowerShell como Administrador.

### O CSV não foi importado

1. Verifique se o arquivo está na pasta do projeto
2. O nome deve ser: `PLANEJAMENTO FINANCEIRO.xlsx - 2025.csv`
3. Execute novamente: `python importar_dados.py`

## 📝 Notas Técnicas

- O aplicativo está configurado para desenvolvimento (`debug=True`)
- Os dados persistem mesmo após fechar o navegador ou desligar o computador
- Não é necessário configuração adicional - tudo funciona "plug and play"
- O design foi gamificado com tons de roxo, ciano e verde neon para uma aparência épica de game

## 🎯 Próximas Expansões (DLCs Planejadas)

- 📊 Gráficos de progressão e tendências (Line charts animados)
- 🏆 Sistema de conquistas e badges por metas atingidas
- 💎 Orçamentos mensais (Metas de Gold) com barras de progresso
- ⚔️ Categorias customizadas para criar suas próprias quests
- 🔔 Alertas de vencimento (Quest Deadlines) com notificações
- 💾 Backup automático do save game
- 🎮 Modo escuro/claro alternável
- 📱 PWA (Progressive Web App) para instalar como app
- 🌟 Sistema de níveis baseado em economia mensal

## 🎮 Categorias Gamer Sugeridas

Você pode usar categorias com nomes gamificados:
- **🏠 Base Principal** (Moradia)
- **🍖 Provisions** (Alimentação)
- **⚡ Power-Ups** (Energia, Água, Internet)
- **🚗 Mount & Travel** (Transporte)
- **💊 Health Potions** (Saúde, Farmácia)
- **🎮 Gaming Gear** (Entretenimento, Assinaturas)
- **👕 Equipment** (Vestuário)
- **📚 Skill Tree** (Educação, Cursos)
- **💰 Gold Reserve** (Investimentos, Poupança)
- **🎁 Side Quests** (Outros gastos)

---

**Desenvolvido com ❤️ e 🎮 para gamers que levam finanças a sério!**

*"Gerencie seu Gold como um pro player gerencia seu inventário!"* 🏆
