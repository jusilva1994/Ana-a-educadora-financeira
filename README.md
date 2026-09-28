# 🎓 Ana - A educadora financeira

> Agente de IA Generativa que ensina conceitos de finanças pessoais de forma simples e personalizada, usando os próprios dados do cliente como exemplos práticos.

## 💡 O Que é a Ana?

A Ana é uma educadora financeira que **ensina**, não recomenda. Ela explica conceitos como reserva de emergência, tipos de investimentos e análise de gastos usando uma abordagem didática e exemplos concretos baseados no perfil do cliente.

**O que a Ana faz:**
- ✅ Explica conceitos financeiros de forma simples
- ✅ Usa dados do cliente como exemplos práticos
- ✅ Responde dúvidas sobre produtos financeiros
- ✅ Analisa padrões de gastos de forma educativa

**O que a Ana NÃO faz:**
- ❌ Não recomenda investimentos específicos
- ❌ Não acessa dados bancários sensíveis
- ❌ Não substitui um profissional certificado

## 🏗️ Arquitetura

```mermaid
flowchart TD
    A[Usuário] --> B[Streamlit]
    B --> C[Ollama - LLM Local]
    C --> D[Base de Conhecimento]
    D --> C
    C --> E[Resposta Educativa]

```

**Stack:**
- Interface: Streamlit
- LLM: Ollama (modelo local `llama3.2:3b`)
- Dados: JSON/CSV mockados

## 📁 Estrutura do Projeto

```plaintext
├── data/                          # Base de conhecimento
│   ├── perfil_investidor.json     # Perfil do cliente
│   ├── transacoes.csv             # Histórico financeiro
│   ├── historico_atendimento.csv  # Interações anteriores
│   ├── produtos_financeiros.json  # Produtos para ensino
│   ├── conceitos_basicos.json     # Define conceitos financeiros
│   ├── exercicios.csv             # Exercícios que a Ana faz com o usuário
│
├── docs/                          # Documentação completa
│   ├── 01-documentacao-agente.md  # Caso de uso e persona
│   ├── 02-base-conhecimento.md    # Estratégia de dados
│   ├── 03-prompts.md              # System prompt e exemplos
│   ├── 04-metricas.md             # Avaliação de qualidade
│   └── 05-pitch.md                # Apresentação do projeto
│
└── src/
    └── app.py                     # Aplicação Streamlit

```

## 🚀 Como Executar

### 1. Instalar Ollama

```bash
# Baixar em: ollama.com
ollama pull llama3.2:3b
ollama serve

```

### 2. Instalar Dependências

```bash
pip install streamlit pandas requests tabulate

```

### 3. Rodar a agente Ana

```bash
streamlit run src/app.py
```

## 🎯 Exemplo de Uso

**Pergunta:** "O que é CDI?"  
**Ana:** "O CDI (Certificado de Depósito Interbancário) é um instrumento financeiro utilizado pelos bancos para fechar o dia com saldo positivo. Ele é considerado um dos principais indicadores de referência para investimentos de renda fixa no Brasil."

**Pergunta:** "Onde estou gastando mais?"  
**Ana:** "Onde você está gastando mais? Com base nos cálculos acima, parece que você está gastando mais na moradia, com aproximadamente 54,95% de seus gastos totais."

## 📊 Métricas de Avaliação

| Métrica | Objetivo |
|---------|----------|
| **Assertividade** | O agente responde o que foi perguntado? |
| **Segurança** | Evita inventar informações (anti-alucinação)? |
| **Coerência** | A resposta é adequada ao perfil do cliente? |

## 🎬 Diferenciais

- **Personalização:** Usa os dados do próprio cliente nos exemplos
- **100% Local:** Roda com Ollama, sem enviar dados para APIs externas
- **Educativo:** Foco em ensinar, não em vender produtos
- **Seguro:** Estratégias de anti-alucinação documentadas

## 📝 Documentação Completa

Toda a documentação técnica, estratégias de prompt e casos de teste estão disponíveis na pasta [`docs/`](./docs/).
