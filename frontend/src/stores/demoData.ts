import type { Asset, MarketBenchmarkPoint, PriceHistoryPoint } from '@/types/asset'
import type { AllocationItem, BenchmarkSeries, PerformancePoint, TopMoversResponse } from '@/types/dashboard'
import type { Dividend } from '@/types/dividend'
import type { GlossaryCategory, GlossaryTermDetail } from '@/types/glossary'
import type { PortfolioSummary } from '@/types/portfolio'
import type { ComparisonSeries } from '@/types/simulation'
import type { Transaction } from '@/types/transaction'

const petr4: Asset = {
  id: 'demo-asset-petr4',
  ticker: 'PETR4',
  name: 'Petrobras PN',
  asset_class: 'acao',
  currency: 'BRL',
}
const hglg11: Asset = {
  id: 'demo-asset-hglg11',
  ticker: 'HGLG11',
  name: 'CSHG Logística FII',
  asset_class: 'fii',
  currency: 'BRL',
}
const bova11: Asset = {
  id: 'demo-asset-bova11',
  ticker: 'BOVA11',
  name: 'iShares Ibovespa ETF',
  asset_class: 'etf',
  currency: 'BRL',
}
const tesouroSelic: Asset = {
  id: 'demo-asset-selic2029',
  ticker: 'TESOURO_SELIC_2029',
  name: 'Tesouro Selic 2029',
  asset_class: 'tesouro_direto',
  currency: 'BRL',
}

export const demoAssets: Asset[] = [petr4, hglg11, bova11, tesouroSelic]

export const demoPortfolioSummary: PortfolioSummary = {
  positions: [
    {
      asset: petr4,
      quantity: '100',
      avg_price: '32.10',
      invested_value: '3210.00',
      current_price: '38.50',
      current_value: '3850.00',
      profit: '640.00',
      profit_pct: '19.94',
    },
    {
      asset: hglg11,
      quantity: '25',
      avg_price: '170.00',
      invested_value: '4250.00',
      current_price: '165.20',
      current_value: '4130.00',
      profit: '-120.00',
      profit_pct: '-2.82',
    },
    {
      asset: bova11,
      quantity: '40',
      avg_price: '108.00',
      invested_value: '4320.00',
      current_price: '112.40',
      current_value: '4496.00',
      profit: '176.00',
      profit_pct: '4.07',
    },
    {
      asset: tesouroSelic,
      quantity: '10',
      avg_price: '1500.00',
      invested_value: '15000.00',
      current_price: '1523.40',
      current_value: '15234.00',
      profit: '234.00',
      profit_pct: '1.56',
    },
  ],
  total_invested: '26780.00',
  total_current: '27710.00',
  total_profit: '930.00',
  total_profit_pct: '3.47',
}

export const demoTransactions: Transaction[] = [
  {
    id: 'demo-tx-1',
    asset: petr4,
    operation: 'compra',
    quantity: '100',
    unit_price: '32.10',
    fees: '8.50',
    operation_date: '2026-04-12',
  },
  {
    id: 'demo-tx-2',
    asset: hglg11,
    operation: 'compra',
    quantity: '25',
    unit_price: '170.00',
    fees: '3.20',
    operation_date: '2026-05-03',
  },
  {
    id: 'demo-tx-3',
    asset: bova11,
    operation: 'compra',
    quantity: '40',
    unit_price: '108.00',
    fees: '5.00',
    operation_date: '2026-05-20',
  },
  {
    id: 'demo-tx-4',
    asset: tesouroSelic,
    operation: 'compra',
    quantity: '10',
    unit_price: '1500.00',
    fees: '0.00',
    operation_date: '2026-06-01',
  },
]

export const demoAllocation: AllocationItem[] = [
  { asset_class: 'acao', value: '3850.00', percentage: '13.89' },
  { asset_class: 'fii', value: '4130.00', percentage: '14.90' },
  { asset_class: 'etf', value: '4496.00', percentage: '16.22' },
  { asset_class: 'tesouro_direto', value: '15234.00', percentage: '54.98' },
]

export const demoPerformance: PerformancePoint[] = [
  { date: '2026-02-01', value: '24100.00' },
  { date: '2026-03-01', value: '24980.00' },
  { date: '2026-04-01', value: '25610.00' },
  { date: '2026-05-01', value: '26330.00' },
  { date: '2026-06-01', value: '27020.00' },
  { date: '2026-07-01', value: '27710.00' },
]

export const demoBenchmarks: BenchmarkSeries = {
  portfolio: [
    { date: '2026-02-01', value: '0.00' },
    { date: '2026-03-01', value: '3.65' },
    { date: '2026-04-01', value: '6.27' },
    { date: '2026-05-01', value: '9.25' },
    { date: '2026-06-01', value: '12.12' },
    { date: '2026-07-01', value: '14.98' },
  ],
  cdi: [
    { date: '2026-02-01', value: '0.00' },
    { date: '2026-03-01', value: '0.85' },
    { date: '2026-04-01', value: '1.71' },
    { date: '2026-05-01', value: '2.58' },
    { date: '2026-06-01', value: '3.46' },
    { date: '2026-07-01', value: '4.35' },
  ],
  ipca: [
    { date: '2026-02-01', value: '0.00' },
    { date: '2026-03-01', value: '0.42' },
    { date: '2026-04-01', value: '0.85' },
    { date: '2026-05-01', value: '1.28' },
    { date: '2026-06-01', value: '1.71' },
    { date: '2026-07-01', value: '2.15' },
  ],
  ibov: [
    { date: '2026-02-01', value: '0.00' },
    { date: '2026-03-01', value: '2.10' },
    { date: '2026-04-01', value: '1.40' },
    { date: '2026-05-01', value: '4.80' },
    { date: '2026-06-01', value: '6.90' },
    { date: '2026-07-01', value: '8.30' },
  ],
}

export const demoTopMovers: TopMoversResponse = {
  gainers: [
    { asset: bova11, change_pct: '1.83' },
    { asset: petr4, change_pct: '1.21' },
  ],
  losers: [
    { asset: hglg11, change_pct: '-0.92' },
    { asset: tesouroSelic, change_pct: '-0.05' },
  ],
}

export const demoDividends: Dividend[] = [
  { id: 'demo-div-1', asset: petr4, amount: '42.30', payment_date: '2026-03-20' },
  { id: 'demo-div-2', asset: hglg11, amount: '187.50', payment_date: '2026-04-15' },
  { id: 'demo-div-3', asset: petr4, amount: '38.90', payment_date: '2026-04-20' },
  { id: 'demo-div-4', asset: hglg11, amount: '192.00', payment_date: '2026-05-15' },
  { id: 'demo-div-5', asset: hglg11, amount: '196.50', payment_date: '2026-06-15' },
  { id: 'demo-div-6', asset: petr4, amount: '45.10', payment_date: '2026-06-20' },
]

// --- Mercado (demo mode) ---

export const demoAssetPriceHistory: Record<string, PriceHistoryPoint[]> = {
  PETR4: [
    { price_date: '2026-06-01', close_price: '35.10' },
    { price_date: '2026-06-08', close_price: '36.40' },
    { price_date: '2026-06-15', close_price: '35.80' },
    { price_date: '2026-06-22', close_price: '37.20' },
    { price_date: '2026-06-29', close_price: '38.00' },
    { price_date: '2026-07-06', close_price: '37.60' },
    { price_date: '2026-07-13', close_price: '38.50' },
  ],
  HGLG11: [
    { price_date: '2026-06-01', close_price: '172.00' },
    { price_date: '2026-06-08', close_price: '170.50' },
    { price_date: '2026-06-15', close_price: '168.90' },
    { price_date: '2026-06-22', close_price: '167.30' },
    { price_date: '2026-06-29', close_price: '166.00' },
    { price_date: '2026-07-06', close_price: '165.80' },
    { price_date: '2026-07-13', close_price: '165.20' },
  ],
  BOVA11: [
    { price_date: '2026-06-01', close_price: '104.00' },
    { price_date: '2026-06-08', close_price: '105.60' },
    { price_date: '2026-06-15', close_price: '107.10' },
    { price_date: '2026-06-22', close_price: '108.40' },
    { price_date: '2026-06-29', close_price: '109.90' },
    { price_date: '2026-07-06', close_price: '111.20' },
    { price_date: '2026-07-13', close_price: '112.40' },
  ],
  TESOURO_SELIC_2029: [
    { price_date: '2026-06-01', close_price: '1508.20' },
    { price_date: '2026-06-15', close_price: '1513.70' },
    { price_date: '2026-06-29', close_price: '1518.90' },
    { price_date: '2026-07-13', close_price: '1523.40' },
  ],
}

export const demoMarketBenchmarks: Record<string, MarketBenchmarkPoint[]> = {
  cdi: [
    { ref_date: '2026-06-01', value: '0.04' },
    { ref_date: '2026-06-15', value: '0.04' },
    { ref_date: '2026-06-29', value: '0.04' },
    { ref_date: '2026-07-13', value: '0.04' },
  ],
  ipca: [
    { ref_date: '2026-06-01', value: '0.35' },
    { ref_date: '2026-07-01', value: '0.30' },
  ],
  ibov: [
    { ref_date: '2026-06-01', value: '128400' },
    { ref_date: '2026-06-15', value: '130100' },
    { ref_date: '2026-06-29', value: '131800' },
    { ref_date: '2026-07-13', value: '133500' },
  ],
}

// --- Simulações (demo mode) ---

export const demoComparisonSeries: ComparisonSeries[] = [
  {
    key: 'PETR4',
    label: 'PETR4',
    points: [
      { date: '2026-01-01', value: '0.00' },
      { date: '2026-02-01', value: '4.20' },
      { date: '2026-03-01', value: '2.10' },
      { date: '2026-04-01', value: '8.90' },
      { date: '2026-05-01', value: '11.40' },
      { date: '2026-06-01', value: '15.20' },
      { date: '2026-07-01', value: '19.94' },
    ],
  },
  {
    key: 'BOVA11',
    label: 'BOVA11',
    points: [
      { date: '2026-01-01', value: '0.00' },
      { date: '2026-02-01', value: '1.80' },
      { date: '2026-03-01', value: '3.40' },
      { date: '2026-04-01', value: '2.90' },
      { date: '2026-05-01', value: '5.10' },
      { date: '2026-06-01', value: '6.80' },
      { date: '2026-07-01', value: '8.30' },
    ],
  },
  {
    key: 'cdi',
    label: 'CDI',
    points: [
      { date: '2026-01-01', value: '0.00' },
      { date: '2026-02-01', value: '0.85' },
      { date: '2026-03-01', value: '1.71' },
      { date: '2026-04-01', value: '2.58' },
      { date: '2026-05-01', value: '3.46' },
      { date: '2026-06-01', value: '4.35' },
      { date: '2026-07-01', value: '5.25' },
    ],
  },
  {
    key: 'ipca',
    label: 'IPCA',
    points: [
      { date: '2026-01-01', value: '0.00' },
      { date: '2026-02-01', value: '0.42' },
      { date: '2026-03-01', value: '0.85' },
      { date: '2026-04-01', value: '1.28' },
      { date: '2026-05-01', value: '1.71' },
      { date: '2026-06-01', value: '2.15' },
      { date: '2026-07-01', value: '2.59' },
    ],
  },
  {
    key: 'ibov',
    label: 'IBOV',
    points: [
      { date: '2026-01-01', value: '0.00' },
      { date: '2026-02-01', value: '2.10' },
      { date: '2026-03-01', value: '1.40' },
      { date: '2026-04-01', value: '4.80' },
      { date: '2026-05-01', value: '6.90' },
      { date: '2026-06-01', value: '8.30' },
      { date: '2026-07-01', value: '10.20' },
    ],
  },
]

// --- Aprendizado (demo mode) ---

const catRendaVariavel: GlossaryCategory = { id: 'cat-renda-variavel', slug: 'renda-variavel', name: 'Renda Variável' }
const catRendaFixa: GlossaryCategory = { id: 'cat-renda-fixa', slug: 'renda-fixa', name: 'Renda Fixa' }
const catFundos: GlossaryCategory = { id: 'cat-fundos', slug: 'fundos', name: 'Fundos' }
const catIndicadores: GlossaryCategory = { id: 'cat-indicadores', slug: 'indicadores', name: 'Indicadores' }
const catConceitos: GlossaryCategory = { id: 'cat-conceitos-gerais', slug: 'conceitos-gerais', name: 'Conceitos Gerais' }

export const demoGlossaryCategories: GlossaryCategory[] = [
  catRendaVariavel,
  catRendaFixa,
  catFundos,
  catIndicadores,
  catConceitos,
]

export const demoGlossaryTerms: GlossaryTermDetail[] = [
  {
    slug: 'acao',
    term: 'Ação',
    short_definition: 'Menor parcela do capital social de uma empresa negociada em bolsa.',
    category: catRendaVariavel,
    full_explanation:
      'Ao comprar uma ação, você se torna sócio da empresa e passa a ter direito a uma fração de seus ' +
      'lucros (via dividendos) e do seu valor de mercado. O preço varia diariamente conforme oferta e ' +
      'demanda, resultados da empresa e cenário econômico — por isso é chamada de renda variável: não ' +
      'há retorno garantido.',
    example: 'Comprar 100 ações de PETR4 significa ter uma pequena participação na Petrobras.',
  },
  {
    slug: 'bdr',
    term: 'BDR',
    short_definition: 'Certificado negociado na B3 que representa ações de empresas estrangeiras.',
    category: catRendaVariavel,
    full_explanation:
      'BDR (Brazilian Depositary Receipt) permite investir em empresas como Apple ou Amazon sem precisar ' +
      'abrir conta em corretora no exterior, negociando na bolsa brasileira em reais.',
    example: 'AAPL34 é o BDR da Apple negociado na B3.',
  },
  {
    slug: 'volatilidade',
    term: 'Volatilidade',
    short_definition: 'Medida de quanto o preço de um ativo oscila em um período.',
    category: catRendaVariavel,
    full_explanation:
      'Ativos mais voláteis têm variações de preço mais bruscas (para cima ou para baixo), o que representa ' +
      'mais risco, mas também mais potencial de ganho ou perda no curto prazo.',
    example: null,
  },
  {
    slug: 'tesouro-selic',
    term: 'Tesouro Selic',
    short_definition: 'Título público pós-fixado que acompanha a taxa Selic, com alta liquidez diária.',
    category: catRendaFixa,
    full_explanation:
      'É considerado o investimento mais conservador do mercado brasileiro, indicado para reserva de ' +
      'emergência por ter baixo risco e poder ser resgatado a qualquer momento com pouca variação de preço.',
    example: null,
  },
  {
    slug: 'tesouro-ipca',
    term: 'Tesouro IPCA+',
    short_definition: 'Título público que paga uma taxa fixa mais a variação da inflação (IPCA).',
    category: catRendaFixa,
    full_explanation:
      'Protege o poder de compra do investidor no longo prazo, pois garante um ganho real acima da ' +
      'inflação. Costuma ter maior oscilação de preço no curto prazo se vendido antes do vencimento.',
    example: null,
  },
  {
    slug: 'cdb',
    term: 'CDB',
    short_definition: 'Certificado de Depósito Bancário: título de renda fixa emitido por bancos.',
    category: catRendaFixa,
    full_explanation:
      'Ao investir em um CDB, você empresta dinheiro ao banco em troca de uma remuneração (geralmente um ' +
      'percentual do CDI). Conta com a garantia do FGC até o limite legal por CPF e instituição.',
    example: null,
  },
  {
    slug: 'fii',
    term: 'FII',
    short_definition: 'Fundo de Investimento Imobiliário: aplica em imóveis físicos ou papéis do setor imobiliário.',
    category: catFundos,
    full_explanation:
      'Ao comprar uma cota de FII, você recebe periodicamente parte da renda gerada pelos imóveis ' +
      '(aluguéis) na forma de proventos, geralmente isentos de Imposto de Renda para pessoa física.',
    example: 'HGLG11 é um FII que investe em galpões logísticos.',
  },
  {
    slug: 'etf',
    term: 'ETF',
    short_definition: 'Fundo negociado em bolsa que replica o desempenho de um índice.',
    category: catFundos,
    full_explanation:
      'Um ETF permite investir em uma cesta diversificada de ativos com uma única compra, geralmente com ' +
      'taxas de administração menores que fundos ativos tradicionais.',
    example: 'BOVA11 replica o Ibovespa.',
  },
  {
    slug: 'come-cotas',
    term: 'Come-cotas',
    short_definition: 'Antecipação semestral de Imposto de Renda sobre fundos de investimento.',
    category: catFundos,
    full_explanation:
      'Ocorre em maio e novembro: o fundo reduz a quantidade de cotas do investidor no valor equivalente ' +
      'ao imposto devido sobre o rendimento até aquele momento (exceto ações e FIIs).',
    example: null,
  },
  {
    slug: 'cdi',
    term: 'CDI',
    short_definition: 'Taxa de referência usada nos empréstimos entre bancos, muito próxima da Selic.',
    category: catIndicadores,
    full_explanation:
      'É o principal indexador da renda fixa brasileira — investimentos são comumente descritos como ' +
      '"% do CDI" (ex: 110% do CDI) para indicar sua rentabilidade esperada.',
    example: null,
  },
  {
    slug: 'ipca',
    term: 'IPCA',
    short_definition: 'Índice oficial de inflação do Brasil, medido pelo IBGE.',
    category: catIndicadores,
    full_explanation:
      'É usado como meta de inflação pelo Banco Central e como indexador de diversos títulos de renda ' +
      'fixa (ex: Tesouro IPCA+) para proteger o poder de compra do investidor.',
    example: null,
  },
  {
    slug: 'dividend-yield',
    term: 'Dividend Yield (DY)',
    short_definition: 'Percentual que representa os proventos pagos por um ativo em relação ao seu preço.',
    category: catIndicadores,
    full_explanation:
      'Um DY de 8% ao ano significa que, ao preço atual, o ativo pagou o equivalente a 8% de seu valor em ' +
      'proventos no período — mas não garante que esse valor se repetirá no futuro.',
    example: null,
  },
  {
    slug: 'juros-compostos',
    term: 'Juros Compostos',
    short_definition: 'Juros que incidem sobre o valor inicial mais os juros já acumulados em períodos anteriores.',
    category: catConceitos,
    full_explanation:
      'Também chamado de "juros sobre juros", é o motor do crescimento exponencial dos investimentos no ' +
      'longo prazo: quanto mais tempo o dinheiro permanece investido, maior o efeito da capitalização composta.',
    example: null,
  },
  {
    slug: 'liquidez',
    term: 'Liquidez',
    short_definition: 'Facilidade de converter um investimento em dinheiro sem perda relevante de valor.',
    category: catConceitos,
    full_explanation:
      'Ativos de alta liquidez (como Tesouro Selic ou ações de grandes empresas) podem ser vendidos ' +
      'rapidamente; ativos de baixa liquidez (como imóveis) podem levar tempo para encontrar comprador.',
    example: null,
  },
  {
    slug: 'diversificacao',
    term: 'Diversificação',
    short_definition: 'Estratégia de distribuir investimentos entre diferentes ativos para reduzir riscos.',
    category: catConceitos,
    full_explanation:
      'A ideia por trás do ditado "não coloque todos os ovos na mesma cesta": perdas em um ativo podem ser ' +
      'compensadas por ganhos em outros, reduzindo o impacto de um evento negativo isolado.',
    example: null,
  },
  {
    slug: 'dividendo',
    term: 'Dividendo',
    short_definition: 'Parte do lucro de uma empresa distribuída aos acionistas.',
    category: catConceitos,
    full_explanation:
      'É uma forma de remuneração ao investidor além da valorização do preço da ação, geralmente paga em ' +
      'dinheiro proporcionalmente à quantidade de ações que o investidor possui.',
    example: null,
  },
]
