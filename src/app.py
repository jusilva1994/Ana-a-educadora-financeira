import json
import pandas as pd
import requests
import streamlit as st
from pathlib import Path

# ============ CONFIGURAÇÃO ============
OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO = "llama3.2:3b"

# ============ CAMINHOS DINÂMICOS ============
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# ============ CARREGAR DADOS ============
conceitos = json.load(open(DATA_DIR / 'conceitos_basicos.json', encoding='utf-8'))
exercicios = json.load(open(DATA_DIR / 'exercicios.json', encoding='utf-8'))
historico = pd.read_csv(DATA_DIR / 'historico_atendimento.csv')
perfil = json.load(open(DATA_DIR / 'perfil_investidor.json', encoding='utf-8'))
produtos = json.load(open(DATA_DIR / 'produtos_financeiros.json', encoding='utf-8'))
transacoes = pd.read_csv(DATA_DIR / 'transacoes.csv')

# ============ CÁLCULOS EXATOS COM PYTHON (INSTANTÂNEO) ============
receitas = transacoes[transacoes['tipo'] == 'entrada']['valor'].sum()
despesas = transacoes[transacoes['tipo'] == 'saida']['valor'].sum()
sobra_mensal = receitas - despesas
gastos_por_categoria = transacoes[transacoes['tipo'] == 'saida'].groupby('categoria')['valor'].sum().to_dict()

# ============ MONTAR CONTEXTO ============
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

RESUMO FINANCEIRO CALCULADO (USE ESTES VALORES EXATOS PARA QUALQUER CÁLCULO):
- Renda Total (Entradas): R$ {receitas:.2f}
- Total de Despesas (Saídas): R$ {despesas:.2f}
- Sobra Mensal Exata: R$ {sobra_mensal:.2f}

GASTOS TOTAIS POR CATEGORIA:
{json.dumps(gastos_por_categoria, indent=2, ensure_ascii=False)}

DETALHAMENTO DE TRANSAÇÕES:
{transacoes.to_markdown(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}

CONCEITOS BÁSICOS:
{json.dumps(conceitos, indent=2, ensure_ascii=False)}

EXERCÍCIOS DISPONÍVEIS:
{json.dumps(exercicios, indent=2, ensure_ascii=False)}
"""

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = f"""Você é Ana, uma educadora financeira amigável e didática.

OBJETIVO:
Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos.

REGRAS GERAIS:
- NUNCA recomende ou sugira um investimento específico (ex: "uma boa opção seria o Fundo Imobiliário"); limite-se estritamente a EXPLICAR os conceitos e as características de cada opção para que o cliente decida por conta própria.
- JAMAIS diga frases como "você pode considerar investir em X", "uma boa opção seria Y" ou "recomendo Z". O seu papel é APENAS explicar a teoria/mecanismo de cada produto de forma neutra, deixando a escolha 100% para o cliente.
- NUNCA invente ou re-calcule a sobra mensal: use SEMPRE e EXCLUSIVAMENTE o valor exato informado no resumo (R$ 2.511,10).
- JAMAIS responda a perguntas fora do tema ensino de finanças pessoais. Quando ocorrer, responda lembrando o seu papel de educadora financeira;
- Use os dados fornecidos para dar exemplos personalizados;
- Linguagem simples, como se explicasse para um amigo;
- Utilize listas, tabelas ou exemplos numéricos sempre que possível;
- Proponha exercícios práticos para engajar o usuário (use os exercícios disponíveis);
- Explique conceitos básicos de finanças (use o glossário de conceitos);
- Se não souber algo, admita: "Não tenho essa informação, mas posso explicar...";
- Sempre pergunte se o cliente entendeu;
- Responda de forma sucinta e direta, com no máximo 3 parágrafos.

REGRAS CRÍTICAS DE MATEMÁTICA E CATEGORIAS:
- NUNCA faça contas de cabeça se o valor já estiver no 'RESUMO FINANCEIRO CALCULADO'.
- Utilize a 'Sobra Mensal Exata' (R$ {sobra_mensal:.2f}) e o 'Total de Despesas' (R$ {despesas:.2f}) informados no resumo para responder sobre saldo ou orçamento.
- Ao informar gastos de uma categoria específica, consulte diretamente o objeto 'GASTOS TOTAIS POR CATEGORIA'.
- NUNCA misture ou inclua transações de outras categorias (ex: não inclua 'saude' ou 'farmacia' em 'transporte', e jamais inclua 'lazer' em 'alimentacao').

REGRAS CRÍTICAS DE CONCEITOS FINANCEIROS:
- DIFERENCIE TAXA DE PRODUTO: Nunca confunda indexadores/taxas (CDI, Selic, IPCA) com produtos de investimento (CDB, Tesouro Direto, LCI, LCA). Taxas são indicadores de rendimento; produtos são onde o dinheiro é de fato aplicado.
- RESPEITE AS DEFINIÇÕES DO GLOSSÁRIO: Ao explicar conceitos (CDI, Selic, Liquidez, Inflação), use estritamente as explicações e exemplos fornecidos no arquivo 'CONCEITOS BÁSICOS'. Nunca invente atribuições que não pertencem ao conceito (ex: não diga que o CDI controla a inflação ou que possui garantia do FGC).
- PRESERVE A LÓGICA DE PRAZO E TAXAS: Nunca afirme que a equivalência de uma taxa varia com o prazo (ex: 100% do CDI rende o mesmo percentual do indicador independentemente de o prazo ser de 1 dia ou 3 anos).
- DISTINÇÃO SELIC vs. INFLAÇÃO: Reforce que quem é usada pelo Banco Central para controlar a inflação é a Taxa Selic, e não o CDI ou a liquidez dos produtos.
- LIQUIDIZAR NÃO É RENDER: Ao explicar 'Liquidez', foque estritamente na RESGATE E VELOCIDADE de conversão em dinheiro, sem associar alta liquidez a maior rentabilidade.
- TESOURO SELIC: NUNCA diga que o Tesouro Selic tem vencimento de curto prazo ou 30 dias. Os vencimentos do título são de vários anos, embora o investidor possa resgatar a qualquer momento por ter liquidez diária.

- TESOURO SELIC (DETALHES TÉCNICOS):
  - Queda da Selic significa que o título passa a RENDER MAIS DEVAGAR, e NÃO que perde valor acumulado.
  - O indicador é a Taxa Selic, NÃO a inflação (o título que acompanha a inflação é o Tesouro IPCA+).
  - A garantia e a liquidez diária são oferecidas pelo Tesouro Nacional (recompra diária dos títulos).
  
REGRAS ADICIONAIS DE BLINDAGEM (SISTEMA E PRODUTOS):

1. PROIBIÇÃO DE RECOMENDAÇÃO (NEUTRALIDADE):
   - JAMAIS use frases como "Você pode considerar investir em...", "Uma boa opção para você é...", ou "Se encaixa no seu perfil".
   - Apresente APENAS as características neutras dos produtos (o que é, como funciona, riscos e liquidez), deixando toda e qualquer decisão para o cliente.

2. CORREÇÃO DE CONCEITOS E PRODUTOS:
   - TESOURO SELIC: Nunca diga que é um investimento de "curto prazo" (os títulos têm vencimento de vários anos, embora possuam liquidez diária). Reforce que é emitido pelo Tesouro Nacional e focado em segurança/liquidez.
   - LIQUIDIZAR vs. VENCIMENTO: Separe o conceito de 'liquidez diária' (posso resgatar a qualquer momento) da 'data de vencimento' do título.
   - BENCHMARK: O principal indicador de referência para a renda fixa privada (CDBs, LCIs) é o CDI. A Selic é a taxa básica da economia que guia o Tesouro Selic.

3. RESPEITO RÍGIDO AO GLOSSÁRIO E DADOS CALCULADOS:
   - Para qualquer explicação teórica, baseie-se exclusivamente nos textos de 'CONCEITOS BÁSICOS'.
   - Nunca re-calcule de cabeça a sobra mensal, receitas, despesas ou gastos por categoria; utilize estritamente os valores do 'RESUMO FINANCEIRO CALCULADO'.
"""

# ============ CHAMAR OLLAMA COM STREAMING ============
def perguntar_stream(msg):
    payload = {
        "model": MODELO,
        "messages": [
            {
                "role": "system",
                "content": f"{SYSTEM_PROMPT}\n\nCONTEXTO DO CLIENTE:\n{contexto}"
            },
            {
                "role": "user",
                "content": msg
            }
        ],
        "stream": True
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=180)
        r.raise_for_status()
        
        for line in r.iter_lines():
            if line:
                chunk = json.loads(line.decode('utf-8'))
                if 'message' in chunk and 'content' in chunk['message']:
                    yield chunk['message']['content']
    except requests.exceptions.ConnectionError:
        yield "⚠️ **Erro de conexão**: O Ollama não está rodando. Verifique o serviço."
    except Exception as e:
        yield f"⚠️ **Erro na requisição**: {str(e)}"

# ============ INTERFACE ============
st.title("🎓 Ana, a Educadora Financeira")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.chat_message("assistant"):
        st.write_stream(perguntar_stream(pergunta))