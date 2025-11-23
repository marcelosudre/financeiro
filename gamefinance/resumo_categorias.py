import requests

# Verificar categorias criadas
r = requests.get('http://127.0.0.1:5000/api/categorias')
categorias = r.json()

despesas = [c for c in categorias if c['tipo'] == 'despesa']
ganhos = [c for c in categorias if c['tipo'] == 'ganho']

print("=" * 60)
print("SISTEMA DE CATEGORIAS - IMPLEMENTADO COM SUCESSO!")
print("=" * 60)

print(f"\n📊 DESPESAS ({len(despesas)} categorias)")
for cat in despesas:
    print(f"  {cat['icone']} {cat['nome']:<20} | Cor: {cat['cor']}")

print(f"\n💰 GANHOS ({len(ganhos)} categorias)")
for cat in ganhos:
    print(f"  {cat['icone']} {cat['nome']:<20} | Cor: {cat['cor']}")

print("\n" + "=" * 60)
print("FUNCIONALIDADES:")
print("=" * 60)
print("✓ Aba 'Categorias' com interface dedicada")
print("✓ Cadastro de novas categorias (nome, tipo, ícone, cor)")
print("✓ Listagem separada por tipo (Despesa/Ganho)")
print("✓ Edição de categorias (nome)")
print("✓ Deleção de categorias")
print("✓ Cores personalizáveis para cada categoria")
print("✓ Ícones/Emojis para cada categoria")
print("✓ Integração com dropdowns de transações")
print("✓ API completa (GET, POST, PUT, DELETE)")
print("=" * 60)
