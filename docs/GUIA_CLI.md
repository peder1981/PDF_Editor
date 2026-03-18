# 📟 Guia da Interface de Linha de Comando (CLI)

## 📋 Índice

1. [Introdução](#introdução)
2. [Instalação](#instalação)
3. [Comandos Disponíveis](#comandos-disponíveis)
4. [Uso Avançado](#uso-avançado)
5. [Exemplos Práticos](#exemplos-práticos)
6. [Dicas e Truques](#dicas-e-truques)

---

## 🚀 Introdução

A Interface de Linha de Comando (CLI) do PDF Editor permite editar PDFs de forma rápida e eficiente, ideal para automação e scripts.

### **Vantagens da CLI**

✅ **Automação** - Perfeito para scripts e automação  
✅ **Velocidade** - Processamento rápido e direto  
✅ **Flexibilidade** - Todas as funcionalidades disponíveis  
✅ **Batch Processing** - Processamento em lote nativo  
✅ **Integração** - Fácil integração com outras ferramentas  

---

## 📦 Instalação

### **Pré-requisitos**

```bash
# Python 3.8 ou superior
python3 --version

# Instalar dependências
pip install -r requirements.txt
```

### **Verificar Instalação**

```bash
# Testar CLI
python3 -m interfaces.cli --help

# Deve mostrar:
# Advanced PDF Editor - Edit PDFs while preserving structure
```

### **Correções Recentes**

✅ **Added CLI support for layout-preserving and background-preserving**
- Métodos `layout-preserving` e `background-preserving` agora funcionam em CLI
- Help text atualizado com novos métodos
- Todos os métodos de edição disponíveis via CLI:
  - `exact`
  - `comprehensive`
  - `structure`
  - `smart`
  - `heuristic`
  - `integral`
  - `template`
  - `layout-preserving` ⭐
  - `background-preserving` ⭐

---

## 🎯 Comandos Disponíveis

### **1. replace**

Substitui texto em um arquivo PDF.

#### **Sintaxe**

```bash
python3 -m interfaces.cli replace [OPÇÕES]
```

#### **Argumentos**

| Argumento | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `input_file` | Path | ✅ Sim | Arquivo PDF de entrada |
| `search_text` | str | ✅ Sim | Texto a buscar |
| `replace_text` | str | ✅ Sim | Texto de substituição |
| `output_file` | Path | ❌ Não | Arquivo PDF de saída |

#### **Opções**

| Opção | Descrição | Padrão |
|-------|-----------|--------|
| `--method` | Método de edição | `exact` |
| `--case-sensitive, -c` | Busca sensível a maiúsculas/minúsculas | `False` |
| `--preview, -p` | Pré-visualizar alterações | `False` |

#### **Métodos Disponíveis**

- `exact` - Substituição precisa na posição exata
- `comprehensive` - Separa elementos gráficos do texto
- `structure` - Reescreve parágrafo com fonte consistente
- `smart` - Seleção inteligente do método
- `heuristic` - Substituição heurística sequencial
- `integral` - Substituição integral de bloco
- `template` - Cria template limpo
- `layout-preserving` ⭐ - Preserva gráficos e backgrounds
- `background-preserving` ⭐ - Preserva backgrounds coloridos

#### **Exemplos**

```bash
# Substituição simples
python3 -m interfaces.cli replace documento.pdf \
  "texto antigo" \
  "texto novo" \
  output.pdf

# Com preservação de layout
python3 -m interfaces.cli replace documento.pdf \
  "texto antigo" \
  "texto novo" \
  output.pdf \
  --method layout-preserving

# Com pré-visualização
python3 -m interfaces.cli replace documento.pdf \
  "texto antigo" \
  "texto novo" \
  output.pdf \
  --preview

# Sensível a maiúsculas/minúsculas
python3 -m interfaces.cli replace documento.pdf \
  "Texto" \
  "Novo" \
  output.pdf \
  --case-sensitive

# Saída automática (mesmo nome + _edited)
python3 -m interfaces.cli replace documento.pdf \
  "texto antigo" \
  "texto novo"
```

---

### **2. search**

Busca texto em um arquivo PDF.

#### **Sintaxe**

```bash
python3 -m interfaces.cli search [OPÇÕES]
```

#### **Argumentos**

| Argumento | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `input_file` | Path | ✅ Sim | Arquivo PDF de entrada |
| `search_text` | str | ✅ Sim | Texto a buscar |

#### **Opções**

| Opção | Descrição | Padrão |
|-------|-----------|--------|
| `--case-sensitive, -c` | Busca sensível a maiúsculas/minúsculas | `False` |

#### **Exemplos**

```bash
# Busca simples
python3 -m interfaces.cli search documento.pdf "texto a buscar"

# Busca sensível a maiúsculas/minúsculas
python3 -m interfaces.cli search documento.pdf "Texto" --case-sensitive

# Busca com expressão regular
python3 -m interfaces.cli search documento.pdf "texto.*novo"
```

#### **Saída**

```
Search Results: 'texto a buscar'
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Page ┃ Text                                                         ┃ Font      ┃ Size ┃ Position       ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━┩
│    1 │ texto a buscar encontrado aqui...                              │ Helvetica │ 11.0 │ (110.5, 156.0) │
│    2 │ outra ocorrência do texto a buscar...                          │ Helvetica │ 11.0 │ (110.5, 200.0) │
└──────┴──────────────────────────────────────────────────────────────┴───────────┴──────┴────────────────┘

Found 2 instances
```

---

### **3. info**

Exibe informações detalhadas de um arquivo PDF.

#### **Sintaxe**

```bash
python3 -m interfaces.cli info [OPÇÕES]
```

#### **Argumentos**

| Argumento | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `input_file` | Path | ✅ Sim | Arquivo PDF de entrada |

#### **Exemplos**

```bash
# Informações do documento
python3 -m interfaces.cli info documento.pdf
```

#### **Saída**

```
📄 Document Information
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Page Count: 5
📝 Text Instances: 127
📦 File Size: 2.5 MB

📋 Metadata:
  Title: Meu Documento
  Author: João Silva
  Subject: Documento Importante
  Keywords: pdf, editor, teste
  Creator: PDF Editor
  Producer: PyMuPDF
  CreationDate: 2026-03-16
  ModDate: 2026-03-16
```

---

### **4. batch**

Processa múltiplos PDFs em lote.

#### **Sintaxe**

```bash
python3 -m interfaces.cli batch [OPÇÕES]
```

#### **Argumentos**

| Argumento | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `input_dir` | Path | ✅ Sim | Diretório de entrada |
| `config_file` | Path | ✅ Sim | Arquivo de configuração JSON |
| `output_dir` | Path | ✅ Sim | Diretório de saída |

#### **Arquivo de Configuração**

```json
{
  "replacements": [
    {
      "search": "texto antigo",
      "replace": "texto novo",
      "case_sensitive": false
    },
    {
      "search": "outro texto",
      "replace": "novo texto",
      "case_sensitive": true
    }
  ],
  "method": "layout-preserving"
}
```

#### **Exemplos**

```bash
# Processamento em lote
python3 -m interfaces.cli batch pasta_entrada/ \
  config.json \
  pasta_saida/

# Com método de preservação de layout
cat > config.json << EOF
{
  "replacements": [
    {
      "search": "texto antigo",
      "replace": "texto novo",
      "case_sensitive": false
    }
  ],
  "method": "layout-preserving"
}
EOF

python3 -m interfaces.cli batch pasta_entrada/ \
  config.json \
  pasta_saida/
```

---

## 🔧 Uso Avançado

### **Pipeline de Processamento**

```bash
# Buscar texto primeiro
python3 -m interfaces.cli search documento.pdf "texto a buscar"

# Pré-visualizar alterações
python3 -m interfaces.cli replace documento.pdf \
  "texto a buscar" \
  "texto novo" \
  output.pdf \
  --preview

# Aplicar alterações
python3 -m interfaces.cli replace documento.pdf \
  "texto a buscar" \
  "texto novo" \
  output.pdf

# Verificar resultado
python3 -m interfaces.cli search output.pdf "texto novo"
```

### **Processamento em Lote com Múltiplos Arquivos**

```bash
# Criar script de processamento
cat > processar_contratos.sh << EOF
#!/bin/bash

for arquivo in contratos/*.pdf; do
    nome_saida="atualizados/$(basename $arquivo)"
    
    python3 -m interfaces.cli replace "$arquivo" \
      "ACME Corporation" \
      "TechStart Inc." \
      "$nome_saida" \
      --method layout-preserving
    
    echo "Processado: $arquivo -> $nome_saida"
done

echo "Processamento concluído!"
EOF

chmod +x processar_contratos.sh
./processar_contratos.sh
```

### **Integração com Outras Ferramentas**

```bash
# Com grep para filtrar resultados
python3 -m interfaces.cli search documento.pdf "texto" | grep "Page 1"

# Com awk para processar saída
python3 -m interfaces.cli info documento.pdf | awk '/Page Count/ {print $3}'

# Com xargs para processamento paralelo
find documentos/ -name "*.pdf" | xargs -P 4 -I {} \
  python3 -m interfaces.cli replace {} \
    "texto antigo" \
    "texto novo" \
    "atualizados/{}" \
    --method layout-preserving
```

### **Script Python com CLI**

```python
import subprocess
import json

# Buscar texto
result = subprocess.run(
    ["python3", "-m", "interfaces.cli", "search", "documento.pdf", "texto"],
    capture_output=True,
    text=True
)
print(result.stdout)

# Substituir texto
result = subprocess.run(
    [
        "python3", "-m", "interfaces.cli", "replace",
        "documento.pdf",
        "texto antigo",
        "texto novo",
        "output.pdf",
        "--method", "layout-preserving"
    ],
    capture_output=True,
    text=True
)
print(result.stdout)

# Obter informações
result = subprocess.run(
    ["python3", "-m", "interfaces.cli", "info", "documento.pdf"],
    capture_output=True,
    text=True
)
print(result.stdout)
```

---

## 📖 Exemplos Práticos

### **Exemplo 1: Atualizar Atestado Médico**

```bash
# Passo 1: Buscar nome atual
python3 -m interfaces.cli search atestado.pdf "Marcelo"

# Passo 2: Substituir nome com preservação de layout
python3 -m interfaces.cli replace atestado.pdf \
  "Marcelo de Freitas Ferreira" \
  "Fernando Augusto Vargas Rodrigues Paes" \
  atestado_atualizado.pdf \
  --method layout-preserving

# Passo 3: Substituir idade
python3 -m interfaces.cli replace atestado_atualizado.pdf \
  "46 anos" \
  "36 anos" \
  atestado_atualizado.pdf \
  --method layout-preserving

# Passo 4: Substituir data
python3 -m interfaces.cli replace atestado_atualizado.pdf \
  "19 de agosto de 1979" \
  "29 de maio de 1989" \
  atestado_final.pdf \
  --method layout-preserving

# Passo 5: Verificar resultado
python3 -m interfaces.cli info atestado_final.pdf
```

### **Exemplo 2: Processar Contratos em Lote**

```bash
# Criar configuração
cat > config_contratos.json << EOF
{
  "replacements": [
    {
      "search": "ACME Corporation",
      "replace": "TechStart Inc.",
      "case_sensitive": false
    },
    {
      "search": "2023",
      "replace": "2024",
      "case_sensitive": false
    },
    {
      "search": "João Silva",
      "replace": "Maria Santos",
      "case_sensitive": true
    }
  ],
  "method": "layout-preserving"
}
EOF

# Processar todos os contratos
python3 -m interfaces.cli batch contratos/ \
  config_contratos.json \
  contratos_atualizados/
```

### **Exemplo 3: Atualizar Formulário com Background**

```bash
# Preservar background colorido
python3 -m interfaces.cli replace formulario.pdf \
  "Nome: João" \
  "Nome: Maria" \
  formulario_atualizado.pdf \
  --method background-preserving

python3 -m interfaces.cli replace formulario_atualizado.pdf \
  "Idade: 30" \
  "Idade: 25" \
  formulario_atualizado.pdf \
  --method background-preserving
```

### **Exemplo 4: Substituir em PDF com Imagens**

```bash
# Preservar todas as imagens e gráficos
python3 -m interfaces.cli replace documento_com_imagens.pdf \
  "texto antigo" \
  "texto novo" \
  documento_atualizado.pdf \
  --method layout-preserving
```

### **Exemplo 5: Buscar e Substituir com Validação**

```bash
# Script de validação
cat > validar_e_substituir.sh << EOF
#!/bin/bash

DOCUMENTO=$1
TEXTO_BUSCAR=$2
TEXTO_NOVO=$3

# Buscar texto
echo "Buscando: $TEXTO_BUSCAR"
python3 -m interfaces.cli search "$DOCUMENTO" "$TEXTO_BUSCAR"

# Perguntar confirmação
read -p "Deseja substituir '$TEXTO_BUSCAR' por '$TEXTO_NOVO'? (s/n) " resposta

if [ "$resposta" = "s" ]; then
    python3 -m interfaces.cli replace "$DOCUMENTO" \
      "$TEXTO_BUSCAR" \
      "$TEXTO_NOVO" \
      "${DOCUMENTO%.*}_editado.pdf" \
      --method layout-preserving
    
    echo "Substituição concluída!"
else
    echo "Substituição cancelada."
fi
EOF

chmod +x validar_e_substituir.sh

# Usar o script
./validar_e_substituir.sh documento.pdf "texto antigo" "texto novo"
```

---

## 💡 Dicas e Truques

### **1. Usar Preview Antes de Aplicar**

```bash
# Sempre use --preview primeiro
python3 -m interfaces.cli replace documento.pdf \
  "texto antigo" \
  "texto novo" \
  output.pdf \
  --preview

# Depois aplique sem --preview
python3 -m interfaces.cli replace documento.pdf \
  "texto antigo" \
  "texto novo" \
  output.pdf
```

### **2. Escolher o Método Certo**

```bash
# Para documentos simples
--method exact

# Para documentos com imagens
--method layout-preserving

# Para documentos com backgrounds coloridos
--method background-preserving

# Para consistência visual
--method structure
```

### **3. Usar Case-Sensitive Quando Necessário**

```bash
# Busca exata (maiúsculas/minúsculas)
--case-sensitive

# Busca insensível (padrão)
# (sem --case-sensitive)
```

### **4. Processamento Paralelo**

```bash
# Usar GNU Parallel para processamento paralelo
find documentos/ -name "*.pdf" | parallel -j 4 \
  python3 -m interfaces.cli replace {} \
    "texto antigo" \
    "texto novo" \
    "atualizados/{/}" \
    --method layout-preserving
```

### **5. Logging e Debug**

```bash
# Redirecionar saída para log
python3 -m interfaces.cli replace documento.pdf \
  "texto antigo" \
  "texto novo" \
  output.pdf \
  --method layout-preserving \
  > log.txt 2>&1

# Ver log
cat log.txt
```

### **6. Backup Automático**

```bash
# Criar backup antes de editar
cp documento.pdf documento_backup.pdf

python3 -m interfaces.cli replace documento.pdf \
  "texto antigo" \
  "texto novo" \
  documento_editado.pdf

# Se algo der errado, restaurar
cp documento_backup.pdf documento.pdf
```

### **7. Validação de Resultados**

```bash
# Verificar se substituição foi aplicada
python3 -m interfaces.cli search output.pdf "texto novo"

# Verificar se texto antigo foi removido
python3 -m interfaces.cli search output.pdf "texto antigo"
```

---

## 📚 Recursos Adicionais

- [README.md](../README.md) - Visão geral do projeto
- [docs/DOCUMENTACAO_COMPLETA.md](DOCUMENTACAO_COMPLETA.md) - Documentação completa
- [docs/LAYOUT_PRESERVATION.md](LAYOUT_PRESERVATION.md) - Preservação de layout
- [docs/GUIA_GUI.md](GUIA_GUI.md) - Guia da interface gráfica
- [docs/GUIA_TUI.md](GUIA_TUI.md) - Guia da interface terminal
- [docs/GUIA_API.md](GUIA_API.md) - Guia da API Python
