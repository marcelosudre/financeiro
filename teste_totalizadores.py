import requests

# Buscar todas as transações
r = requests.get('http://127.0.0.1:5000/api/transacoes')
transacoes = r.json()

ganhos = [t for t in transacoes if t['tipo'] == 'ganho']
despesas = [t for t in transacoes if t['tipo'] == 'despesa']

ganhosPendentes = [t for t in ganhos if not t['pago']]
ganhosRecebidos = [t for t in ganhos if t['pago']]
despesasPendentes = [t for t in despesas if not t['pago']]
despesasPagas = [t for t in despesas if t['pago']]

ganhosPendentesTotal = sum(t['valor'] for t in ganhosPendentes)
ganhosRecebidosTotal = sum(t['valor'] for t in ganhosRecebidos)
despesasPendentesTotal = sum(t['valor'] for t in despesasPendentes)
despesasPagasTotal = sum(t['valor'] for t in despesasPagas)

print("=" * 60)
print("TOTALIZADORES DETALHADOS DO KANBAN")
print("=" * 60)
print("\n💰 GANHOS")
print(f"  ⏳ Pendentes: R$ {ganhosPendentesTotal:.2f} ({len(ganhosPendentes)} transações)")
print(f"  ✅ Recebidos: R$ {ganhosRecebidosTotal:.2f} ({len(ganhosRecebidos)} transações)")
print(f"  Total: R$ {ganhosPendentesTotal + ganhosRecebidosTotal:.2f}")

print("\n💸 DESPESAS")
print(f"  ⏳ Pendentes: R$ {despesasPendentesTotal:.2f} ({len(despesasPendentes)} transações)")
print(f"  ✅ Pagas: R$ {despesasPagasTotal:.2f} ({len(despesasPagas)} transações)")
print(f"  Total: R$ {despesasPendentesTotal + despesasPagasTotal:.2f}")

ganhosTotal = ganhosPendentesTotal + ganhosRecebidosTotal
despesasTotal = despesasPendentesTotal + despesasPagasTotal
saldo = ganhosTotal - despesasTotal

print("\n⚖️ SALDO GERAL")
print(f"  Total Ganhos: +R$ {ganhosTotal:.2f}")
print(f"  Total Despesas: -R$ {despesasTotal:.2f}")
print(f"  Saldo: {'+' if saldo >= 0 else ''} R$ {saldo:.2f}")
print("=" * 60)
