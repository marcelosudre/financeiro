import requests

# Restaurar valor original
update_data = {
    'descricao': 'IPVA',
    'valor': 583.24,
    'pago': True,
    'data_pagamento': '2025-01-16',
    'tipo': 'despesa',
    'categoria': 'Outros',
    'vencimento': '2025-01-16'
}
r = requests.put('http://127.0.0.1:5000/api/transacoes/1', json=update_data)
print(f'Transacao restaurada: Status {r.status_code}')
print(r.json())
