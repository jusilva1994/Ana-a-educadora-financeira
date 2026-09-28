# Passo a Passo de Execução

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

## Código Completo

Todo o código-fonte está no arquivo `app.py`.

## Como Rodar

```bash
# 1. Instalar dependências
pip install streamlit pandas requests tabulate

# 2. Garantir que Ollama está rodando
ollama serve

# 3. Rodar o app
streamlit run src/app.py
```
