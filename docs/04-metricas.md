# Avaliação e Métricas

> [!TIP]
> **Prompt usado para esta etapa:**
> 
> Crie um plano de avaliação pro agente "Ana" com 3 métricas: assertividade, segurança e coerência. Inclua 4 cenários de teste e um formulário simples de feedback. Preencha o template abaixo.

---

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

---

## Métricas de Qualidade

| Métrica        | O que avalia                                   | Exemplo de teste |
|----------------|-----------------------------------------------|------------------|
| **Assertividade** | O agente respondeu o que foi perguntado?       | Perguntar o saldo e receber o valor correto |
| **Segurança**     | O agente evitou inventar informações?          | Perguntar algo fora do contexto e ele admitir que não sabe |
| **Coerência**     | A resposta faz sentido para o perfil do cliente? | Sugerir investimento conservador para cliente conservador |

> [!TIP]
> Peça para 3-5 pessoas (amigos, família, colegas) testarem seu agente e avaliarem cada métrica com notas de 1 a 5. Isso torna suas métricas mais confiáveis! Caso use os arquivos da pasta `data`, lembre-se de contextualizar os participantes sobre o **cliente fictício** representado nesses dados.

---

## Exemplos de Cenários de Teste

### Teste 1: Consulta de gastos
- **Pergunta:** "Quanto gastei com alimentação?"
- **Resposta esperada:** R$570,00 (baseado no `transacoes.csv`)
- **Resposta recebida:** R$625,90 (foi incluído gasto com lazer)
- **Resultado:** [] Correto  [X] Incorreto

### Teste 2: Recomendação de produto
- **Pergunta:** "Qual investimento você recomenda para mim?"
- **Resposta esperada:** Produto compatível com o perfil do cliente
- **Resposta recebida:** Resposta genérica pedindo mais informações
- **Resultado:** [] Correto  [X] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo?"
- **Resposta esperada:** Agente informa que só trata de finanças
- **Resposta recebida:** Explicou que não fornece previsão do tempo e reforçou propósito financeiro
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 4: Informação inexistente
- **Pergunta:** "Quanto rende o produto BBDC3 na Bovespa?"
- **Resposta esperada:** Agente admite não ter essa informação
- **Resposta recebida:** Explicou que não possui essa informação e contextualizou
- **Resultado:** [X] Correto  [ ] Incorreto

---

## Formulário de Feedback (Sugestão)

| Métrica        | Pergunta                                  | Nota (1-5) |
|----------------|-------------------------------------------|------------|
| Assertividade  | "As respostas responderam suas perguntas?"     | 5  |
| Segurança      | "As informações pareceram confiáveis?"         | 3  |
| Coerência      | "A linguagem foi clara e fácil de entender?"   | 5  |

**Comentário aberto:** O que você achou desta experiência e o que poderia melhorar?

---

## Resultados

**O que funcionou bem:**
- Perguntas fora do escopo foram tratadas corretamente, com explicação clara do propósito do agente.

**O que pode melhorar:**
- O agente confundiu categorias de gastos, incluindo valores de lazer em alimentação e de farmácia em transporte.
- Justificativas foram criativas, mas não condizentes com a regra de cálculo.
- É necessário reforçar que cálculos devem considerar **exclusivamente** a coluna `categoria` da tabela de transações.

---

## Medidas Tomadas para Resolver Alucinações

Para corrigir os problemas de alucinação identificados nos testes:

1. **Regras de categorização reforçadas:**  
   - O agente deve usar apenas os valores da coluna `categoria` ao calcular gastos.  
   - Nenhuma dedução ou associação extra será permitida (ex.: não incluir "farmácia" em "transporte").

2. **Explicação dos cálculos:**  
   - As respostas devem detalhar quais transações foram consideradas.  
   - Isso aumenta transparência e evita interpretações erradas.

3. **Validação de contexto:**  
   - Perguntas fora do escopo continuam sendo respondidas com uma negativa clara.  
   - Isso reduz risco de inventar informações.

4. **Testes adicionais:**  
   - Novos cenários de teste foram criados para validar categorias específicas.  
   - Feedback dos usuários será usado para ajustar regras de filtragem.

---

