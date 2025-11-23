from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from decimal import Decimal
import os
from sqlalchemy import func, inspect, text
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import locale

# Tentar configurar locale para PT-BR
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
    except:
        pass

app = Flask(__name__)

# Configuração do banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'financeiro.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== MODELOS ====================

class Transacao(db.Model):
    """Modelo para contas a pagar/receber"""
    __tablename__ = 'transacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    vencimento = db.Column(db.Date, nullable=False)
    pago = db.Column(db.Boolean, default=False)
    data_pagamento = db.Column(db.Date)
    tipo = db.Column(db.String(10), nullable=False)  # 'despesa' ou 'ganho'
    categoria = db.Column(db.String(50))
    tipo_conta = db.Column(db.String(20), default='variavel')  # 'fixa' ou 'variavel'
    mes_referencia = db.Column(db.Date)  # Primeiro dia do mês
    criado_em = db.Column(db.DateTime, default=datetime.now)
    observacao = db.Column(db.Text)
    # Recorrência / parcelamento
    recorrente = db.Column(db.Boolean, default=False)
    dia_recorrente = db.Column(db.Integer)
    parcelado = db.Column(db.Boolean, default=False)
    parcelas_total = db.Column(db.Integer)
    parcela_num = db.Column(db.Integer)
    origem_id = db.Column(db.Integer)
    
    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'valor': self.valor,
            'vencimento': self.vencimento.strftime('%Y-%m-%d'),
            'pago': self.pago,
            'data_pagamento': self.data_pagamento.strftime('%Y-%m-%d') if self.data_pagamento else None,
            'tipo': self.tipo,
            'categoria': self.categoria,
            'tipo_conta': self.tipo_conta,
            'mes_referencia': self.mes_referencia.strftime('%Y-%m') if self.mes_referencia else None,
            'observacao': self.observacao,
            'recorrente': bool(self.recorrente),
            'dia_recorrente': self.dia_recorrente,
            'parcelado': bool(self.parcelado),
            'parcelas_total': self.parcelas_total,
            'parcela_num': self.parcela_num,
            'origem_id': self.origem_id,
        }

class ListaCompras(db.Model):
    """Modelo para lista de compras/tarefas"""
    __tablename__ = 'lista_compras'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    itens = db.Column(db.Text, default='[]')  # JSON com items
    criado_em = db.Column(db.DateTime, default=datetime.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    ativo = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        import json
        try:
            itens_parsed = json.loads(self.itens) if self.itens else []
        except:
            itens_parsed = []
        
        return {
            'id': self.id,
            'titulo': self.titulo,
            'itens': itens_parsed,
            'criado_em': self.criado_em.strftime('%Y-%m-%d %H:%M'),
            'atualizado_em': self.atualizado_em.strftime('%Y-%m-%d %H:%M'),
            'ativo': self.ativo,
        }

class Categoria(db.Model):
    """Modelo para categorias de transações"""
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    tipo = db.Column(db.String(20), nullable=False)  # 'despesa' ou 'ganho'
    cor = db.Column(db.String(7), default='#001f3f')  # Cor em hexadecimal
    icone = db.Column(db.String(100), default='📌')  # Emoji ou unicode
    criado_em = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo': self.tipo,
            'cor': self.cor,
            'icone': self.icone,
        }


def ensure_observacao_column():
    """Cria a coluna observacao em transacoes caso ainda não exista."""
    with app.app_context():
        inspector = inspect(db.engine)
        colunas = [col['name'] for col in inspector.get_columns('transacoes')]
        if 'observacao' not in colunas:
            with db.engine.begin() as conn:
                conn.execute(text('ALTER TABLE transacoes ADD COLUMN observacao TEXT'))


def ensure_recorrencia_columns():
    """Adiciona colunas de recorrência/parcelamento se não existirem."""
    with app.app_context():
        inspector = inspect(db.engine)
        colunas = [col['name'] for col in inspector.get_columns('transacoes')]
        with db.engine.begin() as conn:
            if 'recorrente' not in colunas:
                conn.execute(text("ALTER TABLE transacoes ADD COLUMN recorrente BOOLEAN DEFAULT 0"))
            if 'dia_recorrente' not in colunas:
                conn.execute(text("ALTER TABLE transacoes ADD COLUMN dia_recorrente INTEGER"))
            if 'parcelado' not in colunas:
                conn.execute(text("ALTER TABLE transacoes ADD COLUMN parcelado BOOLEAN DEFAULT 0"))
            if 'parcelas_total' not in colunas:
                conn.execute(text("ALTER TABLE transacoes ADD COLUMN parcelas_total INTEGER"))
            if 'parcela_num' not in colunas:
                conn.execute(text("ALTER TABLE transacoes ADD COLUMN parcela_num INTEGER"))
            if 'origem_id' not in colunas:
                conn.execute(text("ALTER TABLE transacoes ADD COLUMN origem_id INTEGER"))


ensure_recorrencia_columns()


ensure_observacao_column()

# ==================== ROTAS - TRANSAÇÕES ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/transacoes', methods=['GET'])
def get_transacoes():
    """Retorna todas as transações com opção de filtro"""
    tipo = request.args.get('tipo')  # 'despesa', 'ganho', ou None para todas
    mes = request.args.get('mes')  # Formato: YYYY-MM
    pago = request.args.get('pago')  # 'true', 'false', ou None
    
    query = Transacao.query
    
    if tipo and tipo in ['despesa', 'ganho']:
        query = query.filter_by(tipo=tipo)
    
    if mes:
        try:
            data_inicio = datetime.strptime(mes, '%Y-%m').date()
            data_fim = (data_inicio + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            query = query.filter(Transacao.vencimento >= data_inicio, Transacao.vencimento <= data_fim)
        except:
            pass
    
    if pago is not None:
        query = query.filter_by(pago=pago.lower() == 'true')
    
    transacoes = query.order_by(Transacao.vencimento.desc()).all()
    return jsonify([t.to_dict() for t in transacoes])

@app.route('/api/transacoes/<int:id>', methods=['GET'])
def obter_transacao(id):
    """Obtém uma transação específica"""
    transacao = Transacao.query.get(id)
    if not transacao:
        return jsonify({'erro': 'Transação não encontrada'}), 404
    return jsonify(transacao.to_dict())

@app.route('/api/transacoes', methods=['POST'])
def criar_transacao():
    """Cria uma nova transação"""
    data = request.json
    
    try:
        vencimento = datetime.strptime(data['vencimento'], '%Y-%m-%d').date()
        
        # Calcula o primeiro dia do mês para referência
        mes_ref = vencimento.replace(day=1)
        
        # Helper para somar meses respeitando dias finais do mês
        def add_months(orig_date, months):
            year = orig_date.year + (orig_date.month - 1 + months) // 12
            month = ((orig_date.month - 1 + months) % 12) + 1
            day = orig_date.day
            # Ajusta dia se exceder dias do mês
            from calendar import monthrange
            last_day = monthrange(year, month)[1]
            if day > last_day:
                day = last_day
            return datetime(year, month, day).date()

        created = []

        # Parcelado: cria várias transações (parcelas)
        if data.get('parcelado'):
            parcelas = int(data.get('parcelas_total', 1))
            first_trans = None
            for i in range(1, parcelas + 1):
                venc_i = add_months(vencimento, i - 1)
                # Para parcelamento, vencimento fixo no dia 20 de cada mês (ou último dia se o mês tiver menos dias)
                from calendar import monthrange
                last_day = monthrange(venc_i.year, venc_i.month)[1]
                day20 = 20 if 20 <= last_day else last_day
                venc_i = venc_i.replace(day=day20)
                mes_ref_i = venc_i.replace(day=1)
                t = Transacao(
                    descricao=data['descricao'],
                    valor=float(data['valor']) / parcelas if data.get('valor') else 0.0,
                    vencimento=venc_i,
                    tipo=data['tipo'],
                    categoria=data.get('categoria', ''),
                    mes_referencia=mes_ref_i,
                    pago=False,
                    observacao=data.get('observacao'),
                    parcelado=True,
                    parcelas_total=parcelas,
                    parcela_num=i
                )
                db.session.add(t)
                db.session.commit()
                if i == 1:
                    first_trans = t
                created.append(t)

            # vincula origem_id para todas as parcelas ao id da primeira
            if first_trans:
                for t in created:
                    if t.origem_id != first_trans.id:
                        t.origem_id = first_trans.id
                db.session.commit()

            return jsonify([t.to_dict() for t in created]), 201

        # Recorrente (fixa mensal): cria transações para os próximos meses usando o dia do vencimento informado
        if data.get('recorrente'):
            meses_a_frente = int(data.get('meses_a_frente', 12))
            dia = vencimento.day
            first_trans = None
            for m in range(0, meses_a_frente):
                venc_i = add_months(vencimento, m)
                # ajustar para o dia original do vencimento, ou último dia se necessário
                from calendar import monthrange
                last_day = monthrange(venc_i.year, venc_i.month)[1]
                day_use = dia if dia <= last_day else last_day
                venc_i = venc_i.replace(day=day_use)

                mes_ref_i = venc_i.replace(day=1)
                t = Transacao(
                    descricao=data['descricao'],
                    valor=float(data['valor']),
                    vencimento=venc_i,
                    tipo=data['tipo'],
                    categoria=data.get('categoria', ''),
                    mes_referencia=mes_ref_i,
                    pago=False,
                    observacao=data.get('observacao'),
                    tipo_conta='fixa',
                    recorrente=True
                )
                db.session.add(t)
                db.session.commit()
                if m == 0:
                    first_trans = t
                created.append(t)

            # marca origem_id apontando para o primeiro criado
            if first_trans:
                for t in created:
                    if t.origem_id != first_trans.id:
                        t.origem_id = first_trans.id
                db.session.commit()

            return jsonify([t.to_dict() for t in created]), 201

        # Caso padrão: criação simples de uma transação única
        transacao = Transacao(
            descricao=data['descricao'],
            valor=float(data['valor']),
            vencimento=vencimento,
            tipo=data['tipo'],  # 'despesa' ou 'ganho'
            categoria=data.get('categoria', ''),
            mes_referencia=mes_ref,
            pago=data.get('pago', False),
            observacao=data.get('observacao')
        )
        
        if data.get('pago') and data.get('data_pagamento'):
            transacao.data_pagamento = datetime.strptime(data['data_pagamento'], '%Y-%m-%d').date()
        
        db.session.add(transacao)
        db.session.commit()
        
        return jsonify(transacao.to_dict()), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/api/transacoes/<int:id>', methods=['PUT'])
def atualizar_transacao(id):
    """Atualiza uma transação"""
    transacao = Transacao.query.get(id)
    if not transacao:
        return jsonify({'erro': 'Transação não encontrada'}), 404
    
    data = request.json
    
    if 'descricao' in data:
        transacao.descricao = data['descricao']
    if 'valor' in data:
        transacao.valor = float(data['valor'])
    if 'vencimento' in data:
        vencimento = datetime.strptime(data['vencimento'], '%Y-%m-%d').date()
        transacao.vencimento = vencimento
        transacao.mes_referencia = vencimento.replace(day=1)
    if 'pago' in data:
        transacao.pago = data['pago']
        if data['pago'] and 'data_pagamento' in data:
            transacao.data_pagamento = datetime.strptime(data['data_pagamento'], '%Y-%m-%d').date()
    if 'categoria' in data:
        transacao.categoria = data['categoria']
    if 'tipo' in data:
        transacao.tipo = data['tipo']
    if 'observacao' in data:
        transacao.observacao = data['observacao']
    
    db.session.commit()
    return jsonify(transacao.to_dict())

@app.route('/api/transacoes/<int:id>', methods=['DELETE'])
def deletar_transacao(id):
    """Deleta uma transação"""
    transacao = Transacao.query.get(id)
    if not transacao:
        return jsonify({'erro': 'Transação não encontrada'}), 404
    
    db.session.delete(transacao)
    db.session.commit()
    
    return jsonify({'sucesso': True})

# ==================== ROTAS - MÉTRICAS ====================

@app.route('/api/metricas/mes', methods=['GET'])
def metricas_mes():
    """Retorna métricas do mês especificado"""
    mes = request.args.get('mes')  # Formato: YYYY-MM
    
    if not mes:
        hoje = datetime.now().date()
        mes = f"{hoje.year:04d}-{hoje.month:02d}"
    
    try:
        data_inicio = datetime.strptime(mes, '%Y-%m').date()
        data_fim = (data_inicio + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    except:
        return jsonify({'erro': 'Formato de mês inválido'}), 400
    
    transacoes = Transacao.query.filter(
        Transacao.vencimento >= data_inicio,
        Transacao.vencimento <= data_fim
    ).all()
    
    despesas_total = sum(t.valor for t in transacoes if t.tipo == 'despesa')
    despesas_pagas = sum(t.valor for t in transacoes if t.tipo == 'despesa' and t.pago)
    despesas_pendentes = despesas_total - despesas_pagas
    
    ganhos_total = sum(t.valor for t in transacoes if t.tipo == 'ganho')
    ganhos_recebidos = sum(t.valor for t in transacoes if t.tipo == 'ganho' and t.pago)
    ganhos_pendentes = ganhos_total - ganhos_recebidos
    
    fluxo_caixa = ganhos_recebidos - despesas_pagas
    
    # Agrupar por categoria
    despesas_por_categoria = {}
    ganhos_por_categoria = {}
    
    for t in transacoes:
        categoria = t.categoria or 'Sem categoria'
        if t.tipo == 'despesa':
            despesas_por_categoria[categoria] = despesas_por_categoria.get(categoria, 0) + t.valor
        else:
            ganhos_por_categoria[categoria] = ganhos_por_categoria.get(categoria, 0) + t.valor
    
    return jsonify({
        'mes': mes,
        'despesas': {
            'total': round(despesas_total, 2),
            'pagas': round(despesas_pagas, 2),
            'pendentes': round(despesas_pendentes, 2),
            'por_categoria': {k: round(v, 2) for k, v in despesas_por_categoria.items()}
        },
        'ganhos': {
            'total': round(ganhos_total, 2),
            'recebidos': round(ganhos_recebidos, 2),
            'pendentes': round(ganhos_pendentes, 2),
            'por_categoria': {k: round(v, 2) for k, v in ganhos_por_categoria.items()}
        },
        'fluxo_caixa': round(fluxo_caixa, 2),
        'saldo': round(ganhos_total - despesas_total, 2)
    })

@app.route('/api/metricas/resumo', methods=['GET'])
def metricas_resumo():
    """Retorna resumo geral de todos os meses"""
    transacoes = Transacao.query.all()
    
    despesas_total = sum(t.valor for t in transacoes if t.tipo == 'despesa')
    despesas_pagas = sum(t.valor for t in transacoes if t.tipo == 'despesa' and t.pago)
    
    ganhos_total = sum(t.valor for t in transacoes if t.tipo == 'ganho')
    ganhos_recebidos = sum(t.valor for t in transacoes if t.tipo == 'ganho' and t.pago)
    
    # Resumo por mês
    resumo_meses = {}
    for t in transacoes:
        mes_key = t.mes_referencia.strftime('%Y-%m') if t.mes_referencia else 'Sem data'
        if mes_key not in resumo_meses:
            resumo_meses[mes_key] = {
                'despesas': 0,
                'ganhos': 0,
                'fluxo': 0
            }
        
        if t.tipo == 'despesa' and t.pago:
            resumo_meses[mes_key]['despesas'] += t.valor
        elif t.tipo == 'ganho' and t.pago:
            resumo_meses[mes_key]['ganhos'] += t.valor
        
        resumo_meses[mes_key]['fluxo'] = resumo_meses[mes_key]['ganhos'] - resumo_meses[mes_key]['despesas']
    
    # Ordenar meses
    resumo_meses = {k: resumo_meses[k] for k in sorted(resumo_meses.keys())}
    
    return jsonify({
        'despesas_total': round(despesas_total, 2),
        'ganhos_total': round(ganhos_total, 2),
        'saldo_geral': round(ganhos_total - despesas_total, 2),
        'meses': {k: {kk: round(vv, 2) for kk, vv in v.items()} for k, v in resumo_meses.items()}
    })

# ==================== ROTAS - LISTA DE COMPRAS ====================

@app.route('/api/listas', methods=['GET'])
def get_listas():
    """Retorna todas as listas de compras"""
    listas = ListaCompras.query.filter_by(ativo=True).order_by(ListaCompras.criado_em.desc()).all()
    return jsonify([l.to_dict() for l in listas])

@app.route('/api/listas', methods=['POST'])
def criar_lista():
    """Cria uma nova lista de compras"""
    data = request.json
    
    try:
        lista = ListaCompras(
            titulo=data['titulo'],
            itens='[]'
        )
        db.session.add(lista)
        db.session.commit()
        
        return jsonify(lista.to_dict()), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/api/listas/<int:id>', methods=['GET'])
def get_lista(id):
    """Retorna uma lista específica"""
    lista = ListaCompras.query.get(id)
    if not lista:
        return jsonify({'erro': 'Lista não encontrada'}), 404
    
    return jsonify(lista.to_dict())

@app.route('/api/listas/<int:id>', methods=['PUT'])
def atualizar_lista(id):
    """Atualiza uma lista"""
    lista = ListaCompras.query.get(id)
    if not lista:
        return jsonify({'erro': 'Lista não encontrada'}), 404
    
    data = request.json
    
    if 'titulo' in data:
        lista.titulo = data['titulo']
    if 'itens' in data:
        import json
        lista.itens = json.dumps(data['itens'])
    if 'ativo' in data:
        lista.ativo = data['ativo']
    
    lista.atualizado_em = datetime.now()
    db.session.commit()
    
    return jsonify(lista.to_dict())

@app.route('/api/listas/<int:id>', methods=['DELETE'])
def deletar_lista(id):
    """Marca uma lista como inativa"""
    lista = ListaCompras.query.get(id)
    if not lista:
        return jsonify({'erro': 'Lista não encontrada'}), 404
    
    lista.ativo = False
    db.session.commit()
    
    return jsonify({'sucesso': True})

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    """Retorna dados completos do dashboard"""
    # Novo comportamento: se for passado ?mes=YYYY-MM, retorna métricas apenas para esse mês
    mes = request.args.get('mes')  # formato YYYY-MM opcional

    if mes:
        try:
            data_inicio = datetime.strptime(mes, '%Y-%m').date()
            data_fim = (data_inicio + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        except:
            return jsonify({'erro': 'Formato de mês inválido'}), 400

        transacoes = Transacao.query.filter(
            Transacao.vencimento >= data_inicio,
            Transacao.vencimento <= data_fim
        ).order_by(Transacao.vencimento).all()
    else:
        transacoes = Transacao.query.all()

    # Calcular totais simplificados
    despesas_total = sum(t.valor for t in transacoes if t.tipo == 'despesa')
    despesas_pagas = sum(t.valor for t in transacoes if t.tipo == 'despesa' and t.pago)
    despesas_pendentes = round(despesas_total - despesas_pagas, 2)

    ganhos_total = sum(t.valor for t in transacoes if t.tipo == 'ganho')
    ganhos_recebidos = sum(t.valor for t in transacoes if t.tipo == 'ganho' and t.pago)
    ganhos_pendentes = round(ganhos_total - ganhos_recebidos, 2)

    saldo = round(ganhos_total - despesas_total, 2)

    # Calendário de contas: agrupar transações por data (vencimento)
    calendario = {}
    for t in transacoes:
        key = t.vencimento.strftime('%Y-%m-%d')
        if key not in calendario:
            calendario[key] = []
        calendario[key].append({
            'id': t.id,
            'descricao': t.descricao,
            'valor': round(t.valor, 2),
            'tipo': t.tipo,
            'pago': t.pago,
            'categoria': t.categoria,
            'data_pagamento': t.data_pagamento.strftime('%Y-%m-%d') if t.data_pagamento else None
        })

    # Ordenar calendário por data
    calendario = {k: calendario[k] for k in sorted(calendario.keys())}

    return jsonify({
        'mes': mes if mes else None,
        'despesas': {
            'total': round(despesas_total, 2),
            'pagas': round(despesas_pagas, 2),
            'pendentes': despesas_pendentes
        },
        'ganhos': {
            'total': round(ganhos_total, 2),
            'recebidos': round(ganhos_recebidos, 2),
            'pendentes': ganhos_pendentes
        },
        'saldo': saldo,
        'calendario': calendario
    })

@app.route('/api/gastos/por-mes', methods=['GET'])
def gastos_por_mes():
    """Retorna gastos por mês filtrados por categoria"""
    categoria = request.args.get('categoria', '')
    
    query = Transacao.query.filter(
        Transacao.tipo == 'despesa',
        Transacao.pago == True
    )
    
    if categoria:
        query = query.filter(Transacao.categoria == categoria)
    
    transacoes = query.all()
    
    gastos_por_mes = {}
    for t in transacoes:
        mes = t.mes_referencia.strftime('%Y-%m') if t.mes_referencia else 'Sem data'
        if mes not in gastos_por_mes:
            gastos_por_mes[mes] = 0
        gastos_por_mes[mes] += t.valor
    
    gastos_por_mes = dict(sorted(gastos_por_mes.items()))
    
    return jsonify({k: round(v, 2) for k, v in gastos_por_mes.items()})

# ==================== ROTAS - EXPORTAÇÃO ====================

@app.route('/api/exportar/pdf', methods=['GET'])
def exportar_pdf():
    """Exporta as transações em PDF"""
    mes = request.args.get('mes')
    
    if not mes:
        hoje = datetime.now().date()
        mes = f"{hoje.year:04d}-{hoje.month:02d}"
    
    try:
        data_inicio = datetime.strptime(mes, '%Y-%m').date()
        data_fim = (data_inicio + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    except:
        return jsonify({'erro': 'Formato de mês inválido'}), 400
    
    transacoes = Transacao.query.filter(
        Transacao.vencimento >= data_inicio,
        Transacao.vencimento <= data_fim
    ).order_by(Transacao.vencimento).all()
    
    # Calcular métricas
    despesas = [t for t in transacoes if t.tipo == 'despesa']
    ganhos = [t for t in transacoes if t.tipo == 'ganho']
    
    despesas_total = sum(t.valor for t in despesas)
    despesas_pagas = sum(t.valor for t in despesas if t.pago)
    
    ganhos_total = sum(t.valor for t in ganhos)
    ganhos_recebidos = sum(t.valor for t in ganhos if t.pago)
    
    fluxo_caixa = ganhos_recebidos - despesas_pagas
    
    # Criar PDF em memória
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#001f3f'),
        spaceAfter=30,
        alignment=1
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#001f3f'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Conteúdo
    elements = []
    
    # Título
    mes_nome = data_inicio.strftime('%B de %Y').replace('January', 'Janeiro').replace('February', 'Fevereiro').replace('March', 'Março').replace('April', 'Abril').replace('May', 'Maio').replace('June', 'Junho').replace('July', 'Julho').replace('August', 'Agosto').replace('September', 'Setembro').replace('October', 'Outubro').replace('November', 'Novembro').replace('December', 'Dezembro')
    
    elements.append(Paragraph(f"Relatório Financeiro - {mes_nome}", title_style))
    elements.append(Spacer(1, 12))
    
    # Resumo
    resumo_data = [
        ['Métrica', 'Valor'],
        ['Despesas Total', f'R$ {despesas_total:.2f}'],
        ['Despesas Pagas', f'R$ {despesas_pagas:.2f}'],
        ['Ganhos Total', f'R$ {ganhos_total:.2f}'],
        ['Ganhos Recebidos', f'R$ {ganhos_recebidos:.2f}'],
        ['Fluxo de Caixa', f'R$ {fluxo_caixa:.2f}'],
        ['Saldo', f'R$ {(ganhos_total - despesas_total):.2f}']
    ]
    
    resumo_table = Table(resumo_data, colWidths=[3*inch, 1.5*inch])
    resumo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#001f3f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(resumo_table)
    elements.append(Spacer(1, 20))
    
    # Despesas
    elements.append(Paragraph("DESPESAS", heading_style))
    despesas_data = [['Descrição', 'Categoria', 'Vencimento', 'Valor', 'Status']]
    
    for t in despesas:
        despesas_data.append([
            t.descricao,
            t.categoria or '-',
            t.vencimento.strftime('%d/%m/%Y'),
            f'R$ {t.valor:.2f}',
            'Pago' if t.pago else 'Pendente'
        ])
    
    despesas_table = Table(despesas_data, colWidths=[1.5*inch, 1.3*inch, 1.2*inch, 0.9*inch, 0.8*inch])
    despesas_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#001f3f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
    ]))
    
    elements.append(despesas_table)
    elements.append(Spacer(1, 20))
    
    # Ganhos
    elements.append(Paragraph("GANHOS", heading_style))
    ganhos_data = [['Descrição', 'Categoria', 'Data', 'Valor', 'Status']]
    
    for t in ganhos:
        ganhos_data.append([
            t.descricao,
            t.categoria or '-',
            t.vencimento.strftime('%d/%m/%Y'),
            f'R$ {t.valor:.2f}',
            'Recebido' if t.pago else 'Pendente'
        ])
    
    ganhos_table = Table(ganhos_data, colWidths=[1.5*inch, 1.3*inch, 1.2*inch, 0.9*inch, 0.8*inch])
    ganhos_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#001f3f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
    ]))
    
    elements.append(ganhos_table)
    
    # Gerar PDF
    doc.build(elements)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'Relatorio_Financeiro_{mes}.pdf'
    )

# ==================== ROTAS - CATEGORIAS ====================

@app.route('/api/categorias', methods=['GET'])
def get_categorias():
    """Retorna todas as categorias, opcionalmente filtradas por tipo"""
    tipo = request.args.get('tipo')  # 'despesa' ou 'ganho'
    
    query = Categoria.query
    if tipo and tipo in ['despesa', 'ganho']:
        query = query.filter_by(tipo=tipo)
    
    categorias = query.order_by(Categoria.nome).all()
    return jsonify([c.to_dict() for c in categorias])

@app.route('/api/categorias', methods=['POST'])
def criar_categoria():
    """Cria uma nova categoria"""
    data = request.json
    
    try:
        # Verificar se já existe categoria com esse nome
        existente = Categoria.query.filter_by(nome=data['nome']).first()
        if existente:
            return jsonify({'erro': 'Categoria já existe'}), 400
        
        categoria = Categoria(
            nome=data['nome'],
            tipo=data['tipo'],  # 'despesa' ou 'ganho'
            cor=data.get('cor', '#001f3f'),
            icone=data.get('icone', '📌')
        )
        
        db.session.add(categoria)
        db.session.commit()
        
        return jsonify(categoria.to_dict()), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/api/categorias/<int:id>', methods=['GET'])
def obter_categoria(id):
    """Obtém uma categoria específica"""
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({'erro': 'Categoria não encontrada'}), 404
    return jsonify(categoria.to_dict())

@app.route('/api/categorias/<int:id>', methods=['PUT'])
def atualizar_categoria(id):
    """Atualiza uma categoria"""
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({'erro': 'Categoria não encontrada'}), 404
    
    data = request.json
    
    if 'nome' in data:
        # Verificar se já existe outra categoria com esse nome
        existente = Categoria.query.filter(Categoria.nome == data['nome'], Categoria.id != id).first()
        if existente:
            return jsonify({'erro': 'Já existe outra categoria com esse nome'}), 400
        categoria.nome = data['nome']
    
    if 'tipo' in data:
        categoria.tipo = data['tipo']
    if 'cor' in data:
        categoria.cor = data['cor']
    if 'icone' in data:
        categoria.icone = data['icone']
    
    db.session.commit()
    return jsonify(categoria.to_dict())

@app.route('/api/categorias/<int:id>', methods=['DELETE'])
def deletar_categoria(id):
    """Deleta uma categoria"""
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({'erro': 'Categoria não encontrada'}), 404
    
    db.session.delete(categoria)
    db.session.commit()
    
    return jsonify({'sucesso': True})

# ==================== CRIAR BANCO E RODAR ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True, port=5000)
