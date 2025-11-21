# 💰 Sistema de Controle Financeiro Familiar

Um aplicativo web elegante e intuitivo para gerenciar contas, ganhos e lista de compras em família. Design moderno com tons de azul marinho e preto.

## ✨ Funcionalidades

### 📊 Financeiro
- **Adicionar Transações**: Registre despesas e ganhos com categorias
- **Acompanhamento**: Marque transações como pagas/não pagas
- **Métricas Detalhadas**:
  - Total de despesas e ganhos por mês
  - Fluxo de caixa
  - Saldo (ganhos - despesas)
  - Análise por categoria
- **Filtros**: Filtre por tipo (despesa/ganho), status (pago/pendente) e mês
- **Exportação em PDF**: Gere relatórios profissionais em PDF do seu mês financeiro
- **Importação de Dados**: Importe transações do seu CSV de planejamento anterior

### 📝 Lista de Compras
- **Múltiplas Listas**: Crie listas para diferentes ocasiões
- **Checklist**: Marque itens como concluídos
- **Gerenciar**: Adicione, remova e organize seus itens

## 🎨 Design Moderno
- Interface elegante com tons de azul marinho (#001f3f) e preto
- Responsiva para desktop, tablet e celular
- Animações suaves e intuitivas
- Acessibilidade melhorada

## 🚀 Como Usar

### 1. Instalação das Dependências

Abra o PowerShell na pasta do projeto e execute:

```powershell
pip install -r requirements.txt
```

### 2. Importar Dados do CSV (Opcional)

Se você tem um CSV de planejamento anterior, pode importar automaticamente:

```powershell
python importar_dados.py
```

Este script vai:
- Ler seu arquivo `PLANEJAMENTO FINANCEIRO.xlsx - 2025.csv`
- Categorizar automaticamente as transações
- Importar todas as contas e ganhos para o banco de dados

### 3. Iniciar o Aplicativo

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
d:\projetos\Financeiro\
├── requirements.txt              # Dependências Python
├── importar_dados.py             # Script para importar CSV
├── README.md                     # Este arquivo
├── iniciar.bat                   # Script para iniciar (Windows)
├── iniciar.ps1                   # Script PowerShell (alternativa)
├── PLANEJAMENTO FINANCEIRO.xlsx - 2025.csv  # Seu CSV de dados
└── app\
    ├── app.py                    # Aplicação Flask (backend + banco de dados)
    ├── financeiro.db             # Banco de dados (criado automaticamente)
    └── templates\
        └── index.html            # Interface web (HTML + CSS + JavaScript)
```

## 💡 Como Usar Cada Funcionalidade

### Adicionar Transação

1. Clique na aba **📊 Financeiro**
2. Preencha o formulário "Adicionar Transação":
   - **Tipo**: Selecione "Despesa" ou "Ganho"
   - **Descrição**: Nome da transação (ex: "Aluguel", "Salário")
   - **Valor**: Quanto custou ou quanto ganhou
   - **Categoria**: Selecione uma categoria ou deixe em branco
   - **Data de Vencimento**: Quando vence
   - **Já foi pago?**: Marque se já pagou/recebeu
3. Clique em **Adicionar Transação**

### Ver Métricas

No card "Resumo do Mês":
- Selecione o mês desejado
- Visualize todas as métricas calculadas automaticamente
- Veja o breakdown por categoria

### Exportar em PDF

1. Selecione o mês desejado no card "Resumo do Mês"
2. Clique no botão **📥 Exportar PDF**
3. Um relatório profissional será baixado com:
   - Resumo financeiro (despesas, ganhos, fluxo de caixa)
   - Lista completa de todas as transações
   - Tabelas formatadas com categorias

### Filtrar Transações

Use os filtros na seção "Transações":
- **Tipo**: Todas, apenas Despesas ou apenas Ganhos
- **Status**: Todas, apenas Pendentes ou apenas Pagas
- **Mês**: Selecione o mês para visualizar

### Gerenciar Transações

Para cada transação, você pode:
- **Marcar Pago**: Clique se ainda não marcou como pago
- **Desfazer**: Clique se marcou errado como pago
- **Deletar**: Remove a transação

### Criar Lista de Compras

1. Clique na aba **📝 Lista de Compras**
2. Digite um título (ex: "Compras do Mês", "Açougue")
3. Clique em **Criar Lista**
4. Na lista criada:
   - Digite o item e clique em **+** para adicionar
   - Marque o checkbox para marcar como concluído
   - Clique em **Limpar Concluídos** para remover concluídos
   - Clique em **Deletar Lista** para remover a lista inteira

## 📊 Importar Dados do CSV

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

## 🔄 Sincronização Entre Usuários

Ambos os usuários (você e sua esposa) podem:
- Acessar o mesmo aplicativo no mesmo computador
- Acessar de computadores diferentes na mesma rede (alterar `host` em `app.py`)
- Todos os dados são salvos em tempo real no banco de dados

## ⚙️ Configurações Avançadas

### Acessar de Outros Computadores na Rede

No arquivo `app\app.py`, altere a última linha de:
```python
app.run(debug=True, host='127.0.0.1', port=5000)
```

Para:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

Depois, acesse de outro computador usando o IP do seu computador:
- `http://SEU_IP:5000`
- Para achar seu IP, abra PowerShell e digite: `ipconfig`

### Modificar a Porta

Se a porta 5000 estiver em uso, altere para outra (ex: 8000):
```python
app.run(debug=True, host='127.0.0.1', port=8000)
```

## 📊 Dados Salvos

Todos os dados são salvos em um banco de dados SQLite (`financeiro.db`) na pasta `app/`. 

**Backup**: Para fazer backup, copie o arquivo `financeiro.db` para um local seguro.

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"

Execute:
```powershell
pip install -r requirements.txt
```

### "Address already in use"

A porta 5000 está em uso. Altere a porta em `app.py` ou feche o outro aplicativo.

### "Permission denied"

Se receber erro de permissão, execute o PowerShell como Administrador.

### O CSV não foi importado

1. Verifique se o arquivo está na pasta: `d:\projetos\Financeiro\`
2. O nome deve ser: `PLANEJAMENTO FINANCEIRO.xlsx - 2025.csv`
3. Execute novamente: `python importar_dados.py`

## 📝 Notas

- O aplicativo está configurado para desenvolvimento (`debug=True`)
- Os dados persistem mesmo após fechar o navegador ou desligar o computador
- Não é necessário configuração adicional - tudo funciona "pronto para usar"
- O design foi modernizado com tons de azul marinho e preto para uma aparência mais profissional

## 🎯 Próximas Funcionalidades (Sugestões)

- Gráficos de tendências
- Orçamentos mensais
- Compartilhamento de categorias customizadas
- Alertas de vencimento
- Backup automático

---

**Desenvolvido com ❤️ para controle financeiro familiar**
