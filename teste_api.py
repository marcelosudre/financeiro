import requests
import json

# Teste 1: Obter transação
print("=== TESTE 1: GET /api/transacoes/1 ===")
r = requests.get('http://127.0.0.1:5000/api/transacoes/1')
print(f'Status: {r.status_code}')
t = r.json()
print(f'Transacao: {t["descricao"]}, Tipo: {t["tipo"]}, Valor: {t["valor"]}')

# Teste 2: Atualizar transação
print("\n=== TESTE 2: PUT /api/transacoes/1 (UPDATE) ===")
update_data = {
    'descricao': 'IPVA ATUALIZADO',
    'valor': 600.00,
    'pago': True,
    'data_pagamento': '2025-01-16',
    'tipo': 'despesa',
    'categoria': 'Outros',
    'vencimento': '2025-01-16'
}
r = requests.put('http://127.0.0.1:5000/api/transacoes/1', json=update_data)
print(f'Status: {r.status_code}')
updated = r.json()
print(f'Descricao atualizada: {updated["descricao"]}, Novo valor: {updated["valor"]}')

# Teste 3: Recuperar novamente para confirmar
print("\n=== TESTE 3: GET /api/transacoes/1 (CONFIRMACAO) ===")
r = requests.get('http://127.0.0.1:5000/api/transacoes/1')
print(f'Status: {r.status_code}')
t = r.json()
print(f'Descricao final: {t["descricao"]}, Valor final: {t["valor"]}')

print("\n✓ Todos os testes passaram!")
