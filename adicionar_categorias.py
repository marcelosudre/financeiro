import requests

# Categorias de despesa
categorias_despesa = [
    {'nome': 'Aluguel', 'icone': '🏠', 'cor': '#c9302c'},
    {'nome': 'Alimentação', 'icone': '🍔', 'cor': '#d9534f'},
    {'nome': 'Combustível', 'icone': '⛽', 'cor': '#ff6b6b'},
    {'nome': 'Contas', 'icone': '💡', 'cor': '#ff8c42'},
    {'nome': 'Educação', 'icone': '📚', 'cor': '#9b59b6'},
    {'nome': 'Farmácia', 'icone': '💊', 'cor': '#e74c3c'},
    {'nome': 'Ração', 'icone': '🐕', 'cor': '#e67e22'},
]

# Categorias de ganho
categorias_ganho = [
    {'nome': 'Salário', 'icone': '💰', 'cor': '#27ae60'},
    {'nome': 'Freelance', 'icone': '💻', 'cor': '#2ecc71'},
    {'nome': 'Investimento', 'icone': '📈', 'cor': '#1abc9c'},
    {'nome': 'Bonus', 'icone': '🎁', 'cor': '#16a085'},
]

print("Adicionando categorias de despesa...")
for cat in categorias_despesa:
    r = requests.post('http://127.0.0.1:5000/api/categorias', json={
        'tipo': 'despesa',
        'nome': cat['nome'],
        'icone': cat['icone'],
        'cor': cat['cor']
    })
    if r.status_code == 201:
        print(f"✓ {cat['icone']} {cat['nome']}")
    else:
        print(f"✗ {cat['nome']}: {r.json()}")

print("\nAdicionando categorias de ganho...")
for cat in categorias_ganho:
    r = requests.post('http://127.0.0.1:5000/api/categorias', json={
        'tipo': 'ganho',
        'nome': cat['nome'],
        'icone': cat['icone'],
        'cor': cat['cor']
    })
    if r.status_code == 201:
        print(f"✓ {cat['icone']} {cat['nome']}")
    else:
        print(f"✗ {cat['nome']}: {r.json()}")

print("\n✅ Categorias carregadas com sucesso!")
