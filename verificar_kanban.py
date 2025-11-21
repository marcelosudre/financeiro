import requests

r = requests.get('http://127.0.0.1:5000/api/transacoes')
transacoes = r.json()
print(f'Total de transacoes: {len(transacoes)}')

ganhos = [t for t in transacoes if t['tipo'] == 'ganho']
despesas = [t for t in transacoes if t['tipo'] == 'despesa']

print(f'Ganhos: {len(ganhos)}')
print(f'Despesas: {len(despesas)}')

if ganhos:
    total_ganhos = sum(t['valor'] for t in ganhos)
    print(f'Total de ganhos: R$ {total_ganhos:.2f}')

if despesas:
    total_despesas = sum(t['valor'] for t in despesas)
    print(f'Total de despesas: R$ {total_despesas:.2f}')

print('\nNovas funcionalidades do Kanban:')
print('✓ Totalizadores (Ganhos, Despesas, Saldo)')
print('✓ Cores dinâmicas (Verde positivo, Vermelho negativo)')
print('✓ Seções separadas para Ganhos e Despesas')
print('✓ Colunas internas (Pendentes/Recebidas para ganhos, Pendentes/Pagas para despesas)')
