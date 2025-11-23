"""
Script para importar transações do PDF do planejamento financeiro
Baseado na estrutura visual do PDF onde cada mês está organizado verticalmente
"""
import csv
import os
import sys
from datetime import datetime
import io

# Configurar encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import app, db, Transacao

# ==================== DADOS BASEADOS NO PDF ====================
# Estrutura: cada mês tem suas contas e ganhos específicos

DADOS_POR_MES = {
    'JANEIRO': {
        'despesas': [
            {'desc': 'COMPRA', 'venc': 5, 'valor': 0, 'pago': False},
            {'desc': 'IPVA', 'venc': 16, 'valor': 583.24, 'pago': True},
            {'desc': 'LUZ', 'venc': 24, 'valor': 154.20, 'pago': True},
            {'desc': 'COMBUSTÍVEL', 'venc': 20, 'valor': 0, 'pago': False},
            {'desc': 'PICPAY', 'venc': 13, 'valor': 408.41, 'pago': True},
            {'desc': 'POLE', 'venc': 17, 'valor': 180.00, 'pago': True},
            {'desc': 'ALUGUEL', 'venc': 15, 'valor': 610.00, 'pago': True},
            {'desc': 'NET', 'venc': 20, 'valor': 0, 'pago': False},
            {'desc': 'MEI', 'venc': 20, 'valor': 75.00, 'pago': True},
            {'desc': 'INTER', 'venc': 20, 'valor': 1243.44, 'pago': True},
            {'desc': 'NEXT', 'venc': 20, 'valor': 0, 'pago': False},
            {'desc': 'ÁGUA', 'venc': 17, 'valor': 46.91, 'pago': True},
            {'desc': 'FACUL', 'venc': 20, 'valor': 171.00, 'pago': True},
            {'desc': 'RECARGA', 'venc': 0, 'valor': 0, 'pago': False},
            {'desc': 'RAÇÃO', 'venc': 0, 'valor': 0, 'pago': False},
            {'desc': 'GASTOS', 'venc': 0, 'valor': 0, 'pago': False},
            {'desc': 'Deisy', 'venc': 0, 'valor': 500.00, 'pago': True},
            {'desc': 'FARMÁCIA', 'venc': 0, 'valor': 0, 'pago': False},
            {'desc': 'GUARDAR', 'venc': 0, 'valor': 0, 'pago': False},
        ],
        'ganhos': [
            {'desc': 'CONTA', 'valor': 0, 'pago': False},
            {'desc': 'GLE', 'valor': 0, 'pago': False},
            {'desc': 'MAR', 'valor': 0, 'pago': False},
            {'desc': 'VALUU', 'valor': 0, 'pago': False},
        ]
    },
    'FEVEREIRO': {
        'despesas': [
            {'desc': 'COMPRA', 'venc': 5, 'valor': 0, 'pago': False},
            {'desc': 'LUZ', 'venc': 24, 'valor': 144.00, 'pago': True},
            {'desc': 'COMBUSTÍVEL', 'venc': 10, 'valor': 0, 'pago': False},
            {'desc': 'POLE', 'venc': 17, 'valor': 120.00, 'pago': True},
            {'desc': 'ALUGUEL', 'venc': 15, 'valor': 0, 'pago': False},
            {'desc': 'NET', 'venc': 20, 'valor': 65.00, 'pago': True},
            {'desc': 'MEI', 'venc': 20, 'valor': 80.90, 'pago': True},
            {'desc': 'INTER', 'venc': 20, 'valor': 1903.28, 'pago': True},
            {'desc': 'ÁGUA', 'venc': 17, 'valor': 41.91, 'pago': True},
            {'desc': 'FACUL', 'venc': 20, 'valor': 171.00, 'pago': True},
            {'desc': 'PIC PAY', 'venc': 0, 'valor': 1102.88, 'pago': True},
        ],
        'ganhos': [
            {'desc': 'CONTA', 'valor': 140.00, 'pago': True},
            {'desc': 'GLE', 'valor': 0, 'pago': False},
            {'desc': 'MAR', 'valor': 250.00, 'pago': True},
            {'desc': 'VALUU', 'valor': 0, 'pago': False},
        ]
    },
    'MARÇO': {
        'despesas': [
            {'desc': 'COMPRA', 'venc': 5, 'valor': 0, 'pago': False},
            {'desc': 'LUZ', 'venc': 24, 'valor': 155.00, 'pago': True},
            {'desc': 'COMBUSTÍVEL', 'venc': 10, 'valor': 0, 'pago': False},
            {'desc': 'POLE', 'venc': 17, 'valor': 0, 'pago': False},
            {'desc': 'ALUGUEL', 'venc': 15, 'valor': 609.00, 'pago': True},
            {'desc': 'NET', 'venc': 20, 'valor': 65.00, 'pago': True},
            {'desc': 'MEI', 'venc': 20, 'valor': 82.00, 'pago': True},
            {'desc': 'INTER', 'venc': 20, 'valor': 2554.15, 'pago': True},
            {'desc': 'ÁGUA', 'venc': 17, 'valor': 49.00, 'pago': True},
            {'desc': 'FACUL', 'venc': 20, 'valor': 171.00, 'pago': True},
            {'desc': 'RECARGA', 'venc': 0, 'valor': 65.00, 'pago': True},
            {'desc': 'RAÇÃO', 'venc': 0, 'valor': 115.00, 'pago': True},
            {'desc': 'IPTU', 'venc': 20, 'valor': 119.04, 'pago': True},
            {'desc': 'PIC PAY', 'venc': 0, 'valor': 317.00, 'pago': True},
            {'desc': 'FARMÁCIA', 'venc': 0, 'valor': 140.00, 'pago': True},
        ],
        'ganhos': [
            {'desc': 'CONTA', 'valor': 505.91, 'pago': True},
            {'desc': 'GLE', 'valor': 270.00, 'pago': True},
            {'desc': 'MAR', 'valor': 0, 'pago': False},
            {'desc': 'VALUU', 'valor': 0, 'pago': False},
        ]
    },
    'ABRIL': {
        'despesas': [
            {'desc': 'COMPRA', 'venc': 5, 'valor': 200.00, 'pago': True},
            {'desc': 'LUZ', 'venc': 24, 'valor': 138.00, 'pago': True},
            {'desc': 'COMBUSTÍVEL', 'venc': 10, 'valor': 0, 'pago': False},
            {'desc': 'POLE', 'venc': 17, 'valor': 0, 'pago': False},
            {'desc': 'ALUGUEL', 'venc': 15, 'valor': 495.00, 'pago': True},
            {'desc': 'NET', 'venc': 20, 'valor': 65.00, 'pago': True},
            {'desc': 'MEI', 'venc': 20, 'valor': 75.00, 'pago': True},
            {'desc': 'INTER', 'venc': 20, 'valor': 0, 'pago': False},
            {'desc': 'PIC PAY', 'venc': 0, 'valor': 0, 'pago': False},
            {'desc': 'ÁGUA', 'venc': 17, 'valor': 44.00, 'pago': True},
            {'desc': 'FACUL M', 'venc': 20, 'valor': 197.00, 'pago': True},
            {'desc': 'FACUL G', 'venc': 20, 'valor': 0, 'pago': False},
            {'desc': 'GASTOS', 'venc': 0, 'valor': 2000.00, 'pago': True},
            {'desc': 'IPTU', 'venc': 20, 'valor': 119.04, 'pago': True},
        ],
        'ganhos': [
            {'desc': 'CONTA', 'valor': 2105.00, 'pago': True},
            {'desc': 'GLE', 'valor': 270.00, 'pago': True},
            {'desc': 'MAR', 'valor': 0, 'pago': False},
            {'desc': 'VALUU', 'valor': 0, 'pago': False},
        ]
    },
    'MAIO': {
        'despesas': [
            {'desc': 'COMPRA', 'venc': 5, 'valor': 0, 'pago': False},
            {'desc': 'LUZ', 'venc': 26, 'valor': 137.00, 'pago': True},
            {'desc': 'COMBUSTÍVEL', 'venc': 10, 'valor': 0, 'pago': False},
            {'desc': 'POLE', 'venc': 17, 'valor': 0, 'pago': False},
            {'desc': 'ALUGUEL', 'venc': 15, 'valor': 613.00, 'pago': True},
            {'desc': 'NET', 'venc': 20, 'valor': 65.00, 'pago': True},
            {'desc': 'MEI', 'venc': 20, 'valor': 81.00, 'pago': True},
            {'desc': 'INTER', 'venc': 20, 'valor': 4431.04, 'pago': True},
            {'desc': 'PICPAY', 'venc': 0, 'valor': 0, 'pago': False},
            {'desc': 'ÁGUA', 'venc': 17, 'valor': 49.18, 'pago': True},
            {'desc': 'FACUL M', 'venc': 20, 'valor': 0, 'pago': False},
            {'desc': 'IPTU', 'venc': 20, 'valor': 119.04, 'pago': True},
            {'desc': 'GUARDAR', 'venc': 0, 'valor': 500.00, 'pago': True},
        ],
        'ganhos': [
            {'desc': 'CONTA', 'valor': 72.22, 'pago': True},
            {'desc': 'GLE', 'valor': 790.00, 'pago': True},
            {'desc': 'MAR', 'valor': 0, 'pago': False},
            {'desc': 'VALUU', 'valor': 0, 'pago': False},
        ]
    },
    'JUNHO': {
        'despesas': [
            {'desc': 'COMPRA', 'venc': 5, 'valor': 100.00, 'pago': True},
            {'desc': 'LUZ', 'venc': 24, 'valor': 134.00, 'pago': True},
            {'desc': 'COMBUSTÍVEL', 'venc': 10, 'valor': 0, 'pago': False},
            {'desc': 'POLE', 'venc': 17, 'valor': 0, 'pago': False},
            {'desc': 'ALUGUEL', 'venc': 15, 'valor': 0, 'pago': False},
            {'desc': 'NET', 'venc': 20, 'valor': 65.00, 'pago': True},
            {'desc': 'MEI', 'venc': 20, 'valor': 80.90, 'pago': True},
            {'desc': 'INTER', 'venc': 20, 'valor': 2108.85, 'pago': True},
            {'desc': 'ÁGUA', 'venc': 17, 'valor': 44.00, 'pago': True},
            {'desc': 'FACUL', 'venc': 20, 'valor': 171.00, 'pago': True},
            {'desc': 'RAÇÃO', 'venc': 0, 'valor': 115.00, 'pago': True},
            {'desc': 'Deisy', 'venc': 0, 'valor': 500.00, 'pago': True},
        ],
        'ganhos': [
            {'desc': 'CONTA', 'valor': 1524.23, 'pago': True},
            {'desc': 'GLE', 'valor': 520.00, 'pago': True},
            {'desc': 'MAR', 'valor': 0, 'pago': False},
            {'desc': 'VALUU', 'valor': 0, 'pago': False},
        ]
    },
    'JULHO': {
        'despesas': [
            {'desc': 'COMPRA', 'venc': 5, 'valor': 0, 'pago': False},
            {'desc': 'LUZ', 'venc': 24, 'valor': 0, 'pago': False},
            {'desc': 'COMBUSTÍVEL', 'venc': 10, 'valor': 0, 'pago': False},
            {'desc': 'POLE', 'venc': 17, 'valor': 0, 'pago': False},
            {'desc': 'ALUGUEL', 'venc': 15, 'valor': 0, 'pago': False},
            {'desc': 'NET', 'venc': 20, 'valor': 65.00, 'pago': True},
            {'desc': 'MEI', 'venc': 20, 'valor': 80.90, 'pago': True},
            {'desc': 'INTER', 'venc': 20, 'valor': 3274.99, 'pago': True},
            {'desc': 'ÁGUA', 'venc': 17, 'valor': 0, 'pago': False},
            {'desc': 'FACUL', 'venc': 20, 'valor': 171.00, 'pago': True},
            {'desc': 'GASTOS', 'venc': 0, 'valor': 3060.19, 'pago': True},
        ],
        'ganhos': [
            {'desc': 'CONTA', 'valor': 0, 'pago': False},
            {'desc': 'GLE', 'valor': 0, 'pago': False},
            {'desc': 'MAR', 'valor': 0, 'pago': False},
            {'desc': 'VALUU', 'valor': 0, 'pago': False},
        ]
    },
    'AGOSTO': {
        'despesas': [
            {'desc': 'COMPRA', 'venc': 5, 'valor': 0, 'pago': False},
            {'desc': 'LUZ', 'venc': 24, 'valor': 0, 'pago': False},
            {'desc': 'COMBUSTÍVEL', 'venc': 10, 'valor': 0, 'pago': False},
            {'desc': 'POLE', 'venc': 17, 'valor': 242.00, 'pago': True},
            {'desc': 'ALUGUEL', 'venc': 15, 'valor': 0, 'pago': False},
            {'desc': 'NET', 'venc': 20, 'valor': 0, 'pago': False},
            {'desc': 'MEI', 'venc': 20, 'valor': 0, 'pago': False},
            {'desc': 'INTER', 'venc': 20, 'valor': 3424.97, 'pago': True},
            {'desc': 'ÁGUA', 'venc': 17, 'valor': 0, 'pago': False},
            {'desc': 'FACUL', 'venc': 20, 'valor': 0, 'pago': False},
        ],
        'ganhos': [
            {'desc': 'CONTA', 'valor': 355.00, 'pago': True},
            {'desc': 'GLE', 'valor': 430.00, 'pago': True},
            {'desc': 'MAR', 'valor': 0, 'pago': False},
            {'desc': 'VALUU', 'valor': 0, 'pago': False},
        ]
    },
    'SETEMBRO': {
        'despesas': [
            {'desc': 'COMPRA', 'venc': 5, 'valor': 400.00, 'pago': True},
            {'desc': 'LUZ', 'venc': 24, 'valor': 0, 'pago': False},
            {'desc': 'COMBUSTÍVEL', 'venc': 10, 'valor': 70.00, 'pago': True},
            {'desc': 'POLE', 'venc': 17, 'valor': 0, 'pago': False},
            {'desc': 'ALUGUEL', 'venc': 15, 'valor': 0, 'pago': False},
            {'desc': 'NET', 'venc': 20, 'valor': 0, 'pago': False},
            {'desc': 'MEI', 'venc': 20, 'valor': 0, 'pago': False},
            {'desc': 'INTER', 'venc': 20, 'valor': 0, 'pago': False},
            {'desc': 'ÁGUA', 'venc': 17, 'valor': 0, 'pago': False},
            {'desc': 'FACUL', 'venc': 20, 'valor': 0, 'pago': False},
            {'desc': 'GASTOS', 'venc': 0, 'valor': 0, 'pago': False},
        ],
        'ganhos': [
            {'desc': 'CONTA', 'valor': 1028.34, 'pago': True},
            {'desc': 'GLE', 'valor': 270.00, 'pago': True},
            {'desc': 'MAR', 'valor': 0, 'pago': False},
            {'desc': 'VALUU', 'valor': 0, 'pago': False},
        ]
    },
    'OUTUBRO': {
        'despesas': [
            {'desc': 'COMPRA', 'venc': 5, 'valor': 0, 'pago': False},
            {'desc': 'LUZ', 'venc': 24, 'valor': 0, 'pago': False},
            {'desc': 'COMBUSTÍVEL', 'venc': 10, 'valor': 0, 'pago': False},
            {'desc': 'POLE', 'venc': 17, 'valor': 0, 'pago': False},
            {'desc': 'ACADEMIA', 'venc': 19, 'valor': 130.00, 'pago': True},
            {'desc': 'ALUGUEL', 'venc': 15, 'valor': 618.00, 'pago': True},
            {'desc': 'NET', 'venc': 20, 'valor': 65.00, 'pago': True},
            {'desc': 'MEI', 'venc': 20, 'valor': 80.90, 'pago': True},
            {'desc': 'INTER', 'venc': 20, 'valor': 0, 'pago': False},
            {'desc': 'ÁGUA', 'venc': 17, 'valor': 0, 'pago': False},
            {'desc': 'FACUL', 'venc': 20, 'valor': 171.00, 'pago': True},
            {'desc': 'RECARGA', 'venc': 0, 'valor': 0, 'pago': False},
            {'desc': 'RAÇÃO', 'venc': 0, 'valor': 120.00, 'pago': True},
        ],
        'ganhos': [
            {'desc': 'CONTA', 'valor': 0, 'pago': False},
            {'desc': 'GLE', 'valor': 0, 'pago': False},
            {'desc': 'MAR', 'valor': 0, 'pago': False},
            {'desc': 'VALUU', 'valor': 0, 'pago': False},
        ]
    },
    'NOVEMBRO': {
        'despesas': [
            {'desc': 'COMPRA', 'venc': 5, 'valor': 0, 'pago': False},
            {'desc': 'LUZ', 'venc': 24, 'valor': 155.00, 'pago': True},
            {'desc': 'COMBUSTÍVEL', 'venc': 10, 'valor': 50.00, 'pago': True},
            {'desc': 'POLE', 'venc': 17, 'valor': 0.00, 'pago': False},
            {'desc': 'ACADEMIA', 'venc': 0, 'valor': 0, 'pago': False},
            {'desc': 'ALUGUEL', 'venc': 15, 'valor': 0, 'pago': False},
            {'desc': 'NET', 'venc': 20, 'valor': 65.00, 'pago': True},
            {'desc': 'MEI', 'venc': 20, 'valor': 0, 'pago': False},
            {'desc': 'INTER', 'venc': 20, 'valor': 3666.68, 'pago': True},
            {'desc': 'ÁGUA', 'venc': 17, 'valor': 0, 'pago': False},
            {'desc': 'FACUL', 'venc': 20, 'valor': 0, 'pago': False},
            {'desc': 'Deisy', 'venc': 0, 'valor': 500.00, 'pago': True},
        ],
        'ganhos': [
            {'desc': 'CONTA', 'valor': 4088.32, 'pago': True},
            {'desc': 'GLE', 'valor': 540.00, 'pago': True},
            {'desc': 'MAR', 'valor': 0, 'pago': False},
            {'desc': 'VALUU', 'valor': 0, 'pago': False},
        ]
    },
    'DEZEMBRO': {
        'despesas': [
            {'desc': 'COMPRA', 'venc': 5, 'valor': 900.00, 'pago': True},
            {'desc': 'LUZ', 'venc': 24, 'valor': 155.00, 'pago': True},
            {'desc': 'COMBUSTÍVEL', 'venc': 10, 'valor': 300.00, 'pago': True},
            {'desc': 'POLE', 'venc': 17, 'valor': 185.00, 'pago': True},
            {'desc': 'ACADEMIA', 'venc': 0, 'valor': 0, 'pago': False},
            {'desc': 'CARTÃO G', 'venc': 0, 'valor': 242.09, 'pago': True},
            {'desc': 'ALUGUEL', 'venc': 15, 'valor': 618.00, 'pago': True},
            {'desc': 'NET', 'venc': 20, 'valor': 65.00, 'pago': True},
            {'desc': 'MEI', 'venc': 20, 'valor': 81.00, 'pago': True},
            {'desc': 'INTER', 'venc': 20, 'valor': 633.42, 'pago': True},
            {'desc': 'ÁGUA', 'venc': 17, 'valor': 121.06, 'pago': True},
            {'desc': 'FACUL', 'venc': 20, 'valor': 171.00, 'pago': True},
            {'desc': 'RECARGA', 'venc': 0, 'valor': 65.00, 'pago': True},
            {'desc': 'RAÇÃO', 'venc': 0, 'valor': 120.50, 'pago': True},
            {'desc': 'GASTOS', 'venc': 0, 'valor': 300.00, 'pago': True},
            {'desc': 'Deisy', 'venc': 0, 'valor': 500.00, 'pago': True},
            {'desc': 'FARMÁCIA', 'venc': 0, 'valor': 160.00, 'pago': True},
            {'desc': 'GUARDAR', 'venc': 0, 'valor': 500.00, 'pago': True},
        ],
        'ganhos': [
            {'desc': 'CONTA', 'valor': 0, 'pago': False},
            {'desc': 'GLE', 'valor': 1080.00, 'pago': True},
            {'desc': 'MAR', 'valor': 2440.00, 'pago': True},
            {'desc': 'VALUU', 'valor': 1280.00, 'pago': True},
        ]
    }
}

# ==================== DEFINIÇÃO DE CONTAS FIXAS ====================
CONTAS_FIXAS = {
    'ALUGUEL', 'NET', 'AGUA', 'ÁGUA', 'LUZ', 'FACUL', 'FACUL M', 'FACUL G',
    'INTER', 'MEI', 'POLE', 'ACADEMIA'
}

def obter_categoria(descricao):
    """Categoriza uma transação"""
    desc_upper = str(descricao).upper()
    
    categorias = {
        'Aluguel': ['ALUGUEL'],
        'Alimentação': ['PICPAY', 'COMPRA', 'SUPERMERCADO'],
        'Combustível': ['COMBUSTÍVEL'],
        'Contas': ['LUZ', 'ÁGUA', 'AGUA', 'NET', 'TELEFONE', 'INTERNET'],
        'Educação': ['FACUL', 'ESCOLA', 'ACADEMIA'],
        'Farmácia': ['FARMACIA', 'FARMÁCIA'],
        'Ração': ['RAÇÃO', 'RACAO', 'PET'],
        'Investimento': ['INTER', 'POUPANÇA'],
        'Outros': ['DEISY', 'GASTOS', 'RECARGA', 'GUARDAR', 'NEXT', 'IPVA', 'IPTU', 'CARTAO']
    }
    
    for categoria, palavras in categorias.items():
        if any(palavra in desc_upper for palavra in palavras):
            return categoria
    
    return 'Outros'

def obter_tipo_conta(descricao):
    """Define se uma conta é fixa ou variável"""
    return 'fixa' if descricao.upper() in CONTAS_FIXAS else 'variavel'

def limpar_banco():
    """Limpa todas as transações do banco"""
    with app.app_context():
        try:
            db.session.query(Transacao).delete()
            db.session.commit()
            print("✓ Banco limpo\n")
        except:
            print("✓ Banco novo criado\n")

def importar_dados():
    """Importa dados baseado na estrutura correta do PDF"""
    with app.app_context():
        transacoes_importadas = 0
        
        print("Importando transações do PDF...\n")
        
        meses_ordem = {
            'JANEIRO': 1, 'FEVEREIRO': 2, 'MARÇO': 3, 'ABRIL': 4,
            'MAIO': 5, 'JUNHO': 6, 'JULHO': 7, 'AGOSTO': 8,
            'SETEMBRO': 9, 'OUTUBRO': 10, 'NOVEMBRO': 11, 'DEZEMBRO': 12
        }
        
        for mes_nome, mes_num in meses_ordem.items():
            if mes_nome not in DADOS_POR_MES:
                continue
            
            dados = DADOS_POR_MES[mes_nome]
            print(f"📅 {mes_nome}")
            
            # Importar despesas
            for item in dados['despesas']:
                if item['valor'] > 0:  # Só importa se tem valor
                    try:
                        vencimento = datetime(2025, mes_num, item['venc']).date() if item['venc'] > 0 else datetime(2025, mes_num, 15).date()
                        mes_ref = datetime(2025, mes_num, 1).date()
                        
                        transacao = Transacao(
                            descricao=item['desc'],
                            valor=item['valor'],
                            vencimento=vencimento,
                            pago=item['pago'],
                            data_pagamento=vencimento if item['pago'] else None,
                            tipo='despesa',
                            categoria=obter_categoria(item['desc']),
                            tipo_conta=obter_tipo_conta(item['desc']),
                            mes_referencia=mes_ref
                        )
                        
                        db.session.add(transacao)
                        transacoes_importadas += 1
                        
                        tipo_conta = '📌 FIXA' if obter_tipo_conta(item['desc']) == 'fixa' else '📊 Variável'
                        status = '✓' if item['pago'] else '⏳'
                        print(f"  {status} {tipo_conta} {item['desc']:20} R$ {item['valor']:8.2f}")
                    except Exception as e:
                        print(f"  ✗ Erro em {item['desc']}: {str(e)}")
            
            # Importar ganhos
            for item in dados['ganhos']:
                if item['valor'] > 0:  # Só importa se tem valor
                    try:
                        mes_ref = datetime(2025, mes_num, 1).date()
                        
                        transacao = Transacao(
                            descricao=item['desc'],
                            valor=item['valor'],
                            vencimento=mes_ref,
                            pago=item['pago'],
                            data_pagamento=mes_ref if item['pago'] else None,
                            tipo='ganho',
                            categoria=item['desc'],
                            tipo_conta='fixa',
                            mes_referencia=mes_ref
                        )
                        
                        db.session.add(transacao)
                        transacoes_importadas += 1
                        
                        status = '✓' if item['pago'] else '⏳'
                        print(f"  {status} 💰 GANHO   {item['desc']:20} R$ {item['valor']:8.2f}")
                    except Exception as e:
                        print(f"  ✗ Erro em {item['desc']}: {str(e)}")
            
            print()
        
        db.session.commit()
        
        print(f"{'='*60}")
        print(f"✓ Importação concluída!")
        print(f"✓ Total de transações importadas: {transacoes_importadas}")
        print(f"{'='*60}\n")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    limpar_banco()
    importar_dados()
