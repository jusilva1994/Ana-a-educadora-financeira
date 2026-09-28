# Base de Conhecimento

> [!TIP]
> **Prompt usado para esta etapa:**
> 
> Organize a base de conhecimento da agente "Ana" usando os 4 arquivos da pasta `data/` (em anexo). Explique pra que serve cada arquivo e monte um exemplo de contexto formatado que será enviado pro LLM. Preencha o template abaixo.
>
> [cole ou anexe o template `02-base-conhecimento.md` pra contexto]

## Dados Utilizados

| Arquivo                     | Formato | Para que serve na Ana? |
|------------------------------|---------|------------------------|
| `historico_atendimento.csv` | CSV     | Contextualizar interações anteriores, permitindo dar continuidade ao atendimento de forma mais eficiente. |
| `perfil_investidor.json`    | JSON    | Personalizar as explicações de acordo com as dúvidas e necessidades de aprendizado do cliente. |
| `produtos_financeiros.json` | JSON    | Listar os produtos financeiros disponíveis para que possam ser ensinados ao cliente. |
| `transacoes.csv`            | CSV     | Analisar padrões de gastos do cliente e usar essas informações de forma didática. |
| `conceitos_basicos.json`    | JSON    | Definir e explicar conceitos financeiros fundamentais de forma clara e prática. |
| `exercicios.csv`            | CSV     | Propor exercícios interativos para reforçar o aprendizado e garantir melhor compreensão dos assuntos. |

---


## 📂 Dados Mockados e Ajustes

Os dados utilizados inicialmente foram os do **João Silva**, definidos no arquivo `perfil_investidor.json`. Esse perfil fictício serviu como base para simular cenários reais de atendimento e personalização das respostas da Ana.

Posteriormente, foi criado o arquivo `conceitos_dados.json`, adicionando informações complementares. Essa atualização foi necessária porque as respostas iniciais não estavam satisfatórias em termos de clareza e precisão. Com os novos dados, a Ana passou a oferecer explicações mais completas e consistentes.

## ⚙️ Escolhas Técnicas

## 📏 Regras e Blindagem da Ana

Para evitar alucinações e garantir respostas consistentes, foram definidas regras rígidas de funcionamento:

- **Neutralidade:** A Ana nunca recomenda investimentos específicos, apenas explica conceitos e características.  
- **Uso de dados mockados:** Sempre utiliza os dados fornecidos (ex.: João Silva) sem inventar valores.  
- **Glossário oficial:** Explicações de CDI, Selic, Liquidez e Inflação seguem estritamente o arquivo `conceitos_basicos.json`.  
- **Matemática controlada:** Nunca recalcula de cabeça; usa apenas os valores do `RESUMO FINANCEIRO CALCULADO`.  
- **Categorias de gastos:** Sempre respeita os dados do `transacoes.csv` sem misturar categorias.  
- **Tesouro Selic:** Explicado corretamente como título de vencimento longo, mas com liquidez diária.  

### Escolhas técnicas
- **Modelo LLM:** Foi escolhido o `llama 3.2:3b` por ser mais leve, adequado a PCs com pouca memória, garantindo maior velocidade nas respostas.  
- **Arquivo `exercicios.csv`:** Incluído para propor exercícios práticos e engajar o usuário no aprendizado.  
- **Arquivo `conceitos_dados.json`:** Adicionado para complementar informações e melhorar a precisão das explicações.  

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades, injetar os dados diretamente no prompt (Ctrl + C, Ctrl + V) ou carregar os arquivos via código, como no exemplo abaixo:

```python
import json
import pandas as pd
import requests
import streamlit as st
from pathlib import Path

conceitos = json.load(open(DATA_DIR / 'conceitos_basicos.json', encoding='utf-8'))
exercicios = json.load(open(DATA_DIR / 'exercicios.json', encoding='utf-8'))
historico = pd.read_csv(DATA_DIR / 'historico_atendimento.csv')
perfil = json.load(open(DATA_DIR / 'perfil_investidor.json', encoding='utf-8'))
produtos = json.load(open(DATA_DIR / 'produtos_financeiros.json', encoding='utf-8'))
transacoes = pd.read_csv(DATA_DIR / 'transacoes.csv')

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Para simplificar, podemos simplesmente "injetar" os dados em nosso prompt, garantindo que a Agente tenha o melhor contexto possível. Lembrando que, em soluções mais robustas, o ideal é que essas informaçoes sejam carregadas dinamicamente para que possamos ganhar flexibilidade.

```text
DADOS DO CLIENTE E PERFIL (data/perfil_investidor.json):
{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.00,
  "perfil_investidor": "moderado",
  "objetivo_principal": "Construir reserva de emergência",
  "patrimonio_total": 15000.00,
  "reserva_emergencia_atual": 10000.00,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.00,
      "prazo": "2026-06"
    },
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 50000.00,
      "prazo": "2027-12"
    }
  ]
}

TRANSACOES DO CLIENTE (data/transacoes.csv):
data,descricao,categoria,valor,tipo
2025-10-01,Salário,receita,5000.00,entrada
2025-10-02,Aluguel,moradia,1200.00,saida
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-05,Netflix,lazer,55.90,saida
2025-10-07,Farmácia,saude,89.00,saida
2025-10-10,Restaurante,alimentacao,120.00,saida
2025-10-12,Uber,transporte,45.00,saida
2025-10-15,Conta de Luz,moradia,180.00,saida
2025-10-20,Academia,saude,99.00,saida
2025-10-25,Combustível,transporte,250.00,saida

HISTORICO DE ATENDIMENTO DO CLIENTE (data/historico_atendimento.csv):
data,canal,tema,resumo,resolvido
2025-09-15,chat,CDB,Cliente perguntou sobre rentabilidade e prazos,sim
2025-09-22,telefone,Problema no app,Erro ao visualizar extrato foi corrigido,sim
2025-10-01,chat,Tesouro Selic,Cliente pediu explicação sobre o funcionamento do Tesouro Direto,sim
2025-10-12,chat,Metas financeiras,Cliente acompanhou o progresso da reserva de emergência,sim
2025-10-25,email,Atualização cadastral,Cliente atualizou e-mail e telefone,sim

PRODUTOS DISPONIVEIS PARA ENSINO (data/produtos_financeiros.json):
[
  {
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic",
    "aporte_minimo": 30.00,
    "indicado_para": "Reserva de emergência e iniciantes"
  },
  {
    "nome": "CDB Liquidez Diária",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "102% do CDI",
    "aporte_minimo": 100.00,
    "indicado_para": "Quem busca segurança com rendimento diário"
  },
  {
    "nome": "LCI/LCA",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "95% do CDI",
    "aporte_minimo": 1000.00,
    "indicado_para": "Quem pode esperar 90 dias (isento de IR)"
  },
  {
    "nome": "Fundo Imobiliário (FII)",
    "categoria": "fundo",
    "risco": "medio",
    "rentabilidade": "Dividend Yield (DY) costuma ficar entre 6% a 12% ao ano",
    "aporte_minimo": 100.00,
    "indicado_para": "Perfil moderado que busca diversificação e renda recorrente mensal"
  },
  {
    "nome": "Fundo de Ações",
    "categoria": "fundo",
    "risco": "alto",
    "rentabilidade": "Variável",
    "aporte_minimo": 100.00,
    "indicado_para": "Perfil arrojado com foco no longo prazo"
  }
]
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

O exemplo de contexto montado abaixo, se baseia nos dados originais da base de conhecimento, mas os sintetiza deixando apenas as informações mais relevantes, otimizando assim o consumo de tokens. Entretanto, vale lembrar que mais importante do que economizar tokens, é ter todas as informações relevantes disponíveis em seu contexto.

```
DADOS DO CLIENTE:
- Nome: João Silva
- Perfil: Moderado
- Objetivo: Construir reserva de emergência
- Reserva atual: R$ 10.000 (meta: R$ 15.000)

RESUMO DE GASTOS:
- Moradia: R$ 1.380
- Alimentação: R$ 570
- Transporte: R$ 295
- Saúde: R$ 188
- Lazer: R$ 55,90
- Total de saídas: R$ 2.488,90

PRODUTOS DISPONÍVEIS PARA EXPLICAR:
- Tesouro Selic (risco baixo)
- CDB Liquidez Diária (risco baixo)
- LCI/LCA (risco baixo)
- Fundo Imobiliário - FII (risco médio)
- Fundo de Ações (risco alto)
```
