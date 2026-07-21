"""create glossary tables and seed content

Revision ID: 0004
Revises: 0003
Create Date: 2026-07-21

"""
import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


CATEGORIES = [
    {"slug": "renda-variavel", "name": "Renda Variável", "sort_order": 1},
    {"slug": "renda-fixa", "name": "Renda Fixa", "sort_order": 2},
    {"slug": "fundos", "name": "Fundos", "sort_order": 3},
    {"slug": "indicadores", "name": "Indicadores", "sort_order": 4},
    {"slug": "conceitos-gerais", "name": "Conceitos Gerais", "sort_order": 5},
]

TERMS = [
    # Renda Variável
    (
        "renda-variavel",
        "acao",
        "Ação",
        "Menor parcela do capital social de uma empresa negociada em bolsa.",
        "Ao comprar uma ação, você se torna sócio da empresa e passa a ter direito a uma fração de "
        "seus lucros (via dividendos) e do seu valor de mercado. O preço varia diariamente conforme "
        "oferta e demanda, resultados da empresa e cenário econômico — por isso é chamada de renda "
        "variável: não há retorno garantido.",
        "Comprar 100 ações de PETR4 significa ter uma pequena participação na Petrobras.",
    ),
    (
        "renda-variavel",
        "bdr",
        "BDR",
        "Certificado negociado na B3 que representa ações de empresas estrangeiras.",
        "BDR (Brazilian Depositary Receipt) permite investir em empresas como Apple ou Amazon sem "
        "precisar abrir conta em corretora no exterior, negociando na bolsa brasileira em reais.",
        "AAPL34 é o BDR da Apple negociado na B3.",
    ),
    (
        "renda-variavel",
        "day-trade",
        "Day Trade",
        "Compra e venda do mesmo ativo no mesmo dia, buscando lucro com a oscilação de curto prazo.",
        "É uma estratégia de alto risco que exige acompanhamento constante do mercado e tem tributação "
        "e regras específicas, diferente do investimento de longo prazo (buy and hold).",
        None,
    ),
    (
        "renda-variavel",
        "volatilidade",
        "Volatilidade",
        "Medida de quanto o preço de um ativo oscila em um período.",
        "Ativos mais voláteis têm variações de preço mais bruscas (para cima ou para baixo), o que "
        "representa mais risco, mas também mais potencial de ganho ou perda no curto prazo.",
        None,
    ),
    # Renda Fixa
    (
        "renda-fixa",
        "tesouro-selic",
        "Tesouro Selic",
        "Título público pós-fixado que acompanha a taxa Selic, com alta liquidez diária.",
        "É considerado o investimento mais conservador do mercado brasileiro, indicado para reserva "
        "de emergência por ter baixo risco e poder ser resgatado a qualquer momento com pouca variação "
        "de preço.",
        None,
    ),
    (
        "renda-fixa",
        "tesouro-ipca",
        "Tesouro IPCA+",
        "Título público que paga uma taxa fixa mais a variação da inflação (IPCA).",
        "Protege o poder de compra do investidor no longo prazo, pois garante um ganho real acima da "
        "inflação. Costuma ter maior oscilação de preço no curto prazo se vendido antes do vencimento.",
        None,
    ),
    (
        "renda-fixa",
        "cdb",
        "CDB",
        "Certificado de Depósito Bancário: título de renda fixa emitido por bancos.",
        "Ao investir em um CDB, você empresta dinheiro ao banco em troca de uma remuneração (geralmente "
        "um percentual do CDI). Conta com a garantia do FGC até o limite legal por CPF e instituição.",
        None,
    ),
    (
        "renda-fixa",
        "lci-lca",
        "LCI / LCA",
        "Letras de Crédito Imobiliário/do Agronegócio, isentas de Imposto de Renda para pessoa física.",
        "Funcionam como o CDB, mas os recursos captados são direcionados a financiar os setores "
        "imobiliário ou do agronegócio. Costumam ter prazos de carência maiores.",
        None,
    ),
    # Fundos
    (
        "fundos",
        "fii",
        "FII",
        "Fundo de Investimento Imobiliário: aplica em imóveis físicos ou papéis do setor imobiliário.",
        "Ao comprar uma cota de FII, você recebe periodicamente parte da renda gerada pelos imóveis "
        "(aluguéis) na forma de proventos, geralmente isentos de Imposto de Renda para pessoa física.",
        "HGLG11 é um FII que investe em galpões logísticos.",
    ),
    (
        "fundos",
        "etf",
        "ETF",
        "Fundo negociado em bolsa que replica o desempenho de um índice.",
        "Um ETF permite investir em uma cesta diversificada de ativos com uma única compra, geralmente "
        "com taxas de administração menores que fundos ativos tradicionais.",
        "BOVA11 replica o Ibovespa.",
    ),
    (
        "fundos",
        "taxa-de-administracao",
        "Taxa de Administração",
        "Percentual anual cobrado pelo gestor de um fundo pela administração dos recursos.",
        "É descontada diretamente da cota do fundo, então quanto maior a taxa, maior o impacto negativo "
        "na rentabilidade líquida do investidor no longo prazo.",
        None,
    ),
    (
        "fundos",
        "come-cotas",
        "Come-cotas",
        "Antecipação semestral de Imposto de Renda sobre fundos de investimento (exceto ações e FIIs).",
        "Ocorre em maio e novembro: o fundo reduz a quantidade de cotas do investidor no valor "
        "equivalente ao imposto devido sobre o rendimento até aquele momento.",
        None,
    ),
    # Indicadores
    (
        "indicadores",
        "cdi",
        "CDI",
        "Taxa de referência usada nos empréstimos entre bancos, muito próxima da Selic.",
        "É o principal indexador da renda fixa brasileira — investimentos são comumente descritos como "
        '"% do CDI" (ex: 110% do CDI) para indicar sua rentabilidade esperada.',
        None,
    ),
    (
        "indicadores",
        "selic",
        "Taxa Selic",
        "Taxa básica de juros da economia brasileira, definida pelo Copom.",
        "Serve de referência para todas as demais taxas de juros do país, incluindo empréstimos, "
        "financiamentos e a rentabilidade de investimentos de renda fixa.",
        None,
    ),
    (
        "indicadores",
        "ipca",
        "IPCA",
        "Índice oficial de inflação do Brasil, medido pelo IBGE.",
        "É usado como meta de inflação pelo Banco Central e como indexador de diversos títulos de "
        "renda fixa (ex: Tesouro IPCA+) para proteger o poder de compra do investidor.",
        None,
    ),
    (
        "indicadores",
        "dividend-yield",
        "Dividend Yield (DY)",
        "Percentual que representa os proventos pagos por um ativo em relação ao seu preço.",
        "Um DY de 8% ao ano significa que, ao preço atual, o ativo pagou o equivalente a 8% de seu "
        "valor em proventos no período — mas não garante que esse valor se repetirá no futuro.",
        None,
    ),
    (
        "indicadores",
        "p-l",
        "P/L",
        "Relação Preço/Lucro: quantos anos de lucro atual seriam necessários para pagar o preço da ação.",
        "É um indicador usado para comparar se uma ação está \"cara\" ou \"barata\" frente a outras "
        "empresas do mesmo setor, mas deve ser analisado junto de outros fatores.",
        None,
    ),
    # Conceitos gerais
    (
        "conceitos-gerais",
        "juros-compostos",
        "Juros Compostos",
        "Juros que incidem sobre o valor inicial mais os juros já acumulados em períodos anteriores.",
        'Também chamado de "juros sobre juros", é o motor do crescimento exponencial dos investimentos '
        "no longo prazo: quanto mais tempo o dinheiro permanece investido, maior o efeito da "
        "capitalização composta.",
        None,
    ),
    (
        "conceitos-gerais",
        "liquidez",
        "Liquidez",
        "Facilidade de converter um investimento em dinheiro sem perda relevante de valor.",
        "Ativos de alta liquidez (como Tesouro Selic ou ações de grandes empresas) podem ser vendidos "
        "rapidamente; ativos de baixa liquidez (como imóveis) podem levar tempo para encontrar comprador.",
        None,
    ),
    (
        "conceitos-gerais",
        "diversificacao",
        "Diversificação",
        "Estratégia de distribuir investimentos entre diferentes ativos para reduzir riscos.",
        'A ideia por trás do ditado "não coloque todos os ovos na mesma cesta": perdas em um ativo '
        "podem ser compensadas por ganhos em outros, reduzindo o impacto de um evento negativo isolado.",
        None,
    ),
    (
        "conceitos-gerais",
        "preco-medio",
        "Preço Médio",
        "Custo médio de aquisição de um ativo, considerando todas as compras realizadas.",
        "Quando você compra o mesmo ativo em momentos e preços diferentes, o preço médio pondera essas "
        "compras pela quantidade, servindo de referência para calcular o lucro ou prejuízo da posição.",
        None,
    ),
    (
        "conceitos-gerais",
        "dividendo",
        "Dividendo",
        "Parte do lucro de uma empresa distribuída aos acionistas.",
        "É uma forma de remuneração ao investidor além da valorização do preço da ação, geralmente paga "
        "em dinheiro proporcionalmente à quantidade de ações que o investidor possui.",
        None,
    ),
]


def upgrade() -> None:
    op.create_table(
        "glossary_categories",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("slug", sa.String(50), nullable=False, unique=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_table(
        "glossary_terms",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "category_id", sa.Uuid(), sa.ForeignKey("glossary_categories.id"), nullable=False
        ),
        sa.Column("slug", sa.String(100), nullable=False, unique=True),
        sa.Column("term", sa.String(150), nullable=False),
        sa.Column("short_definition", sa.String(280), nullable=False),
        sa.Column("full_explanation", sa.Text(), nullable=False),
        sa.Column("example", sa.Text(), nullable=True),
    )

    category_ids = {category["slug"]: uuid.uuid4() for category in CATEGORIES}

    categories_table = sa.table(
        "glossary_categories",
        sa.column("id", sa.Uuid()),
        sa.column("slug", sa.String()),
        sa.column("name", sa.String()),
        sa.column("sort_order", sa.Integer()),
    )
    op.bulk_insert(
        categories_table,
        [
            {
                "id": category_ids[category["slug"]],
                "slug": category["slug"],
                "name": category["name"],
                "sort_order": category["sort_order"],
            }
            for category in CATEGORIES
        ],
    )

    terms_table = sa.table(
        "glossary_terms",
        sa.column("id", sa.Uuid()),
        sa.column("category_id", sa.Uuid()),
        sa.column("slug", sa.String()),
        sa.column("term", sa.String()),
        sa.column("short_definition", sa.String()),
        sa.column("full_explanation", sa.Text()),
        sa.column("example", sa.Text()),
    )
    op.bulk_insert(
        terms_table,
        [
            {
                "id": uuid.uuid4(),
                "category_id": category_ids[category_slug],
                "slug": slug,
                "term": term,
                "short_definition": short_definition,
                "full_explanation": full_explanation,
                "example": example,
            }
            for category_slug, slug, term, short_definition, full_explanation, example in TERMS
        ],
    )


def downgrade() -> None:
    op.drop_table("glossary_terms")
    op.drop_table("glossary_categories")
