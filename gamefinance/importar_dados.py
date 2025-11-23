"""
Script para importar transações do CSV do planejamento financeiro
"""
import csv
import re
from datetime import datetime
import sys
import os

# Adicionar pasta app ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import app, db, Transacao

def extrair_valor(texto):
    """Extrai valor numérico de um texto formatado em real"""
    if not texto or texto.strip() == '':
        return None
    
    # Remove "R$ " e espaços
    texto = str(texto).replace('R$', '').strip()
    
    # Tira pontos de milhar e converte vírgula para ponto
    texto = texto.replace('.', '').replace(',', '.')
    
    try:
        return float(texto)
    except:
        return None

def converter_data(data_str):
    """Converte data de formato DD/MM para datetime do ano atual"""
    if not data_str or data_str.strip() == '':
        return None
    
    data_str = str(data_str).strip()
    
    try:
        # Tenta formato DD/MM
        if '/' in data_str:
            dia, mes = data_str.split('/')
            return datetime(2025, int(mes), int(dia)).date()
    except:
        pass
    
    return None

def importar_csv():
    """Importa transações do CSV"""
    csv_path = os.path.join(os.path.dirname(__file__), 'PLANEJAMENTO FINANCEIRO.xlsx - 2025.csv')
    
    if not os.path.exists(csv_path):
        print(f"Erro: Arquivo {csv_path} não encontrado!")
        return
    
    print(f"Importando transações de: {csv_path}\n")
    
    transacoes_importadas = 0
    erros = 0
    
    with app.app_context():
        with open(csv_path, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        
        mes_atual = None
        
        for i, linha in enumerate(linhas):
            linha = linha.strip()
            
            # Pular linhas vazias
            if not linha or linha.count(',') < 2:
                continue
            
            # Dividir por vírgula, removendo espaços extras
            cols = [col.strip().strip('"') for col in linha.split(',')]
            
            # Detectar mês (formato: "JANEIRO", "FEVEREIRO", etc)
            meses = {
                'JANEIRO': 1, 'FEVEREIRO': 2, 'MARÇO': 3, 'ABRIL': 4,
                'MAIO': 5, 'JUNHO': 6, 'JULHO': 7, 'AGOSTO': 8,
                'SETEMBRO': 9, 'OUTUBRO': 10, 'NOVEMBRO': 11, 'DEZEMBRO': 12
            }
            
            for mes_nome, mes_num in meses.items():
                if mes_nome in linha.upper():
                    mes_atual = mes_num
                    print(f"Processando {mes_nome}...")
                    break
            
            # Procurar por "CONTAS" ou "GANHOS" para identificar seções
            if 'CONTAS' in linha.upper() or 'GANHOS' in linha.upper():
                continue
            
            # Verificar se tem dados de transação (descrição, vencimento, valor)
            # Formato esperado: descrição, valor, data, status, , ganho_desc
            
            if len(cols) >= 3 and mes_atual:
                # Coluna 4 é descrição, 5 é valor/data, 6 é status
                descricao = cols[4] if len(cols) > 4 else None
                valor_texto = cols[5] if len(cols) > 5 else None
                status_texto = cols[6] if len(cols) > 6 else None
                
                # Tentar extrair data (pode estar em col 5 ou 6)
                data_vencimento = None
                if len(cols) > 5:
                    data_vencimento = converter_data(cols[5])
                if not data_vencimento and len(cols) > 6:
                    data_vencimento = converter_data(cols[6])
                
                # Extrair valor (pode estar em col 6 ou 7)
                valor = None
                if len(cols) > 6:
                    valor = extrair_valor(cols[6])
                if not valor and len(cols) > 7:
                    valor = extrair_valor(cols[7])
                
                # Verificar se é uma transação válida
                if descricao and descricao not in ['CONTAS', 'TOTAL', 'GANHOS', 'COMPRA', 'FLUXO', 'RECARGA', 'GASTOS', 'GUARDAR', 'FARMACIA', 'RAÇÃO', '']:
                    
                    # Detectar tipo de transação
                    tipo = 'despesa'  # Padrão
                    categoria = categorizar_transacao(descricao)
                    
                    # Se tem valor mas sem data específica, pular
                    if valor and valor > 0:
                        if not data_vencimento:
                            # Usar dia 20 do mês se não tiver data
                            data_vencimento = datetime(2025, mes_atual, 20).date()
                        
                        # Verificar se já existe
                        existe = Transacao.query.filter_by(
                            descricao=descricao,
                            valor=valor,
                            vencimento=data_vencimento,
                            tipo=tipo
                        ).first()
                        
                        if not existe:
                            try:
                                mes_ref = datetime(2025, mes_atual, 1).date()
                                
                                transacao = Transacao(
                                    descricao=descricao,
                                    valor=valor,
                                    vencimento=data_vencimento,
                                    tipo=tipo,
                                    categoria=categoria,
                                    mes_referencia=mes_ref,
                                    pago=bool(status_texto)  # Se tem algo na coluna de status, já foi pago
                                )
                                
                                # Se foi pago, usar a data de pagamento
                                if transacao.pago:
                                    transacao.data_pagamento = data_vencimento
                                
                                db.session.add(transacao)
                                transacoes_importadas += 1
                                print(f"  ✓ {descricao} - R$ {valor:.2f} ({data_vencimento.strftime('%d/%m')})")
                            except Exception as e:
                                print(f"  ✗ Erro ao adicionar {descricao}: {str(e)}")
                                erros += 1
        
        # Também processar ganhos (coluna 10+)
        print("\nProcessando ganhos...")
        for i, linha in enumerate(linhas):
            linha = linha.strip()
            if not linha:
                continue
            
            cols = [col.strip().strip('"') for col in linha.split(',')]
            
            # Detectar mês
            mes_atual = None
            meses = {
                'JANEIRO': 1, 'FEVEREIRO': 2, 'MARÇO': 3, 'ABRIL': 4,
                'MAIO': 5, 'JUNHO': 6, 'JULHO': 7, 'AGOSTO': 8,
                'SETEMBRO': 9, 'OUTUBRO': 10, 'NOVEMBRO': 11, 'DEZEMBRO': 12
            }
            
            for mes_nome, mes_num in meses.items():
                if mes_nome in linha.upper():
                    mes_atual = mes_num
                    break
            
            # Ganhos começam em coluna 10
            if len(cols) > 10:
                ganho_desc = cols[10] if len(cols) > 10 else None
                ganho_valor = cols[11] if len(cols) > 11 else None
                
                if ganho_desc and ganho_desc not in ['GANHOS', 'CONTA', 'TOTAL', 'FLUXO'] and ganho_valor:
                    valor = extrair_valor(ganho_valor)
                    
                    if valor and valor > 0 and mes_atual:
                        existe = Transacao.query.filter_by(
                            descricao=ganho_desc,
                            valor=valor,
                            tipo='ganho'
                        ).first()
                        
                        if not existe:
                            try:
                                mes_ref = datetime(2025, mes_atual, 1).date()
                                
                                transacao = Transacao(
                                    descricao=ganho_desc,
                                    valor=valor,
                                    vencimento=mes_ref,
                                    tipo='ganho',
                                    categoria=ganho_desc,
                                    mes_referencia=mes_ref,
                                    pago=True,  # Ganhos geralmente já foram recebidos
                                    data_pagamento=mes_ref
                                )
                                
                                db.session.add(transacao)
                                transacoes_importadas += 1
                                print(f"  ✓ {ganho_desc} - R$ {valor:.2f}")
                            except Exception as e:
                                print(f"  ✗ Erro ao adicionar ganho {ganho_desc}: {str(e)}")
                                erros += 1
        
        db.session.commit()
    
    print(f"\n{'='*50}")
    print(f"Importação concluída!")
    print(f"✓ Transações importadas: {transacoes_importadas}")
    print(f"✗ Erros: {erros}")
    print(f"{'='*50}\n")

def categorizar_transacao(descricao):
    """Categoriza uma transação baseada na descrição"""
    descricao_upper = str(descricao).upper()
    
    categorias = {
        'Aluguel': ['ALUGUEL'],
        'Alimentação': ['PICPAY', 'COMPRA', 'SUPERMERCADO'],
        'Combustível': ['COMBUSTÍVEL', 'GASOLINA'],
        'Contas': ['LUZ', 'ÁGUA', 'AGUA', 'NET', 'TELEFONE', 'INTERNET'],
        'Educação': ['FACUL', 'ESCOLA'],
        'Farmácia': ['FARMACIA', 'FARMÁCIA'],
        'Ração': ['RAÇÃO', 'RACAO', 'PET'],
        'Investimento': ['INTER', 'POUPANÇA'],
        'Diverso': ['DEISY', 'GASTOS', 'RECARGA', 'GUARDAR', 'NEXT', 'POLE', 'IPVA', 'IPTU', 'ACADEMIA', 'MEI', 'SERRALHEIRO', 'NIVER', 'CARTAO']
    }
    
    for categoria, palavras in categorias.items():
        if any(palavra in descricao_upper for palavra in palavras):
            return categoria
    
    return 'Outro'

if __name__ == '__main__':
    importar_csv()
