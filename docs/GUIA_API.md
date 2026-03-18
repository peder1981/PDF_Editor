# 🐍 Guia de Referência da API Python

## 📋 Índice

1. [Introdução](#introdução)
2. [Instalação](#instalação)
3. [Classes Principais](#classes-principais)
4. [Métodos Disponíveis](#métodos-disponíveis)
5. [Exemplos de Código](#exemplos-de-código)
6. [Boas Práticas](#boas-práticas)

---

## 🚀 Introdução

A API Python do PDF Editor permite integração direta com seus projetos Python, ideal para automação, scripts personalizados e aplicações customizadas.

### **Vantagens da API Python**

✅ **Flexibilidade** - Integração total com Python  
✅ **Automação** - Scripts personalizados e automatizados  
✅ **Programático** - Controle total sobre o processo  
✅ **Extensível** - Fácil de estender e customizar  
✅ **Completa** - Todas as funcionalidades disponíveis  

---

## 📦 Instalação

### **Pré-requisitos**

```bash
# Python 3.8 ou superior
python3 --version

# Instalar dependências
pip install -r requirements.txt
```

### **Importação Básica**

```python
# Importar classes principais
from core.pdf_editor import PDFEditor, EditOperation, TextInstance
from core.batch_processor import BatchProcessor, BatchJob
from core.improved_layout_editor import ImprovedLayoutEditor
import fitz
```

---

## 🎯 Classes Principais

### **PDFEditor**

Classe principal para edição de PDFs.

#### **Construtor**

```python
editor = PDFEditor()
```

#### **Atributos**

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `document` | `fitz.Document` | Documento PDF carregado |
| `file_path` | `str` | Caminho do arquivo PDF |
| `text_instances` | `List[TextInstance]` | Lista de instâncias de texto |
| `layout_editor` | `ImprovedLayoutEditor` | Editor de preservação de layout |

---

### **TextInstance**

Representa uma instância de texto com suas propriedades.

#### **Atributos**

```python
@dataclass
class TextInstance:
    text: str                    # Texto da instância
    rect: fitz.Rect              # Posição e dimensões
    font: str                    # Nome da fonte
    fontsize: float              # Tamanho da fonte
    color: Tuple[float, float, float]  # Cor do texto (RGB)
    page_num: int                # Número da página
```

#### **Exemplo**

```python
instance = TextInstance(
    text="Exemplo de texto",
    rect=fitz.Rect(100, 200, 300, 250),
    font="Helvetica",
    fontsize=12.0,
    color=(0, 0, 0),
    page_num=0
)
```

---

### **EditOperation**

Representa uma operação de edição.

#### **Atributos**

```python
@dataclass
class EditOperation:
    search_text: str             # Texto a buscar
    replace_text: str            # Texto de substituição
    page_num: Optional[int] = None      # Página específica (opcional)
    case_sensitive: bool = False        # Busca sensível a maiúsculas
    regex: bool = False                 # Usar regex
```

#### **Exemplos**

```python
# Substituição simples
op1 = EditOperation("texto antigo", "texto novo")

# Com case-sensitive
op2 = EditOperation("Texto", "Novo", case_sensitive=True)

# Em página específica
op3 = EditOperation("texto", "novo", page_num=2)

# Com regex
op4 = EditOperation(r"texto.*novo", "substituição", regex=True)
```

---

### **BatchJob**

Representa um job de processamento em lote.

#### **Atributos**

```python
@dataclass
class BatchJob:
    input_file: str              # Arquivo de entrada
    output_file: str             # Arquivo de saída
    operations: List[EditOperation]  # Lista de operações
    method: str = "exact"        # Método de edição
```

#### **Exemplo**

```python
job = BatchJob(
    input_file="contrato.pdf",
    output_file="contrato_editado.pdf",
    operations=[
        EditOperation("ACME Corporation", "TechStart Inc."),
        EditOperation("2023", "2024")
    ],
    method="layout-preserving"
)
```

---

## 📖 Métodos Disponíveis

### **PDFEditor**

#### **load(file_path: str) -> bool**

Carrega um arquivo PDF.

```python
editor = PDFEditor()
success = editor.load("documento.pdf")

if success:
    print("PDF carregado com sucesso")
else:
    print("Erro ao carregar PDF")
```

**Retorna:** `True` se carregado com sucesso, `False` caso contrário.

---

#### **search_text(search_text: str, case_sensitive: bool = False) -> List[TextInstance]**

Busca texto no documento.

```python
# Busca simples
results = editor.search_text("texto a buscar")

# Busca case-sensitive
results = editor.search_text("Texto", case_sensitive=True)

# Processar resultados
for instance in results:
    print(f"Página {instance.page_num}: {instance.text}")
    print(f"  Posição: {instance.rect}")
    print(f"  Fonte: {instance.font} ({instance.fontsize}pt)")
```

**Retorna:** Lista de `TextInstance` encontradas.

---

#### **replace_text_exact(search_text: str, replace_text: str, case_sensitive: bool = False) -> int**

Substitui texto usando método exato.

```python
# Substituição simples
replacements = editor.replace_text_exact("texto antigo", "texto novo")

# Com case-sensitive
replacements = editor.replace_text_exact("Texto", "Novo", case_sensitive=True)

print(f"Feitas {replacements} substituições")
```

**Retorna:** Número de substituições realizadas.

---

#### **replace_text_comprehensive(search_text: str, replace_text: str) -> int**

Substitui texto separando elementos gráficos.

```python
replacements = editor.replace_text_comprehensive("texto antigo", "texto novo")
print(f"Feitas {replacements} substituições")
```

**Retorna:** Número de substituições realizadas.

---

#### **replace_text_structure_preserving(search_text: str, replace_text: str) -> int**

Substitui texto preservando estrutura com fonte homogênea.

```python
replacements = editor.replace_text_structure_preserving("texto antigo", "texto novo")
print(f"Feitas {replacements} substituições")
```

**Retorna:** Número de substituições realizadas.

---

#### **replace_text_layout_preserving(search_text: str, replace_text: str, case_sensitive: bool = False) -> int** ⭐

Substitui texto preservando gráficos, imagens e backgrounds.

```python
# Preservar todos os elementos visuais
replacements = editor.replace_text_layout_preserving("texto antigo", "texto novo")

# Com case-sensitive
replacements = editor.replace_text_layout_preserving("Texto", "Novo", case_sensitive=True)

print(f"Feitas {replacements} substituições")
print("Gráficos e backgrounds foram preservados")
```

**Retorna:** Número de substituições realizadas.

---

#### **replace_text_background_preserving(search_text: str, replace_text: str, case_sensitive: bool = False) -> int** ⭐

Substitui texto preservando cores de fundo e elementos decorativos.

```python
# Preservar backgrounds coloridos
replacements = editor.replace_text_background_preserving("texto antigo", "texto novo")

print(f"Feitas {replacements} substituições")
print("Backgrounds foram preservados")
```

**Retorna:** Número de substituições realizadas.

---

#### **batch_replace(operations: List[EditOperation], method: str = "exact") -> Dict[str, int]**

Realiza múltiplas substituições em lote.

```python
# Criar operações
operations = [
    EditOperation("texto1", "novo1"),
    EditOperation("texto2", "novo2", case_sensitive=True),
    EditOperation("texto3", "novo3")
]

# Processar em lote com método específico
results = editor.batch_replace(operations, method="layout-preserving")

# Verificar resultados
for op, count in results.items():
    print(f"{op}: {count} substituições")
```

**Retorna:** Dicionário com resultados de cada operação.

---

#### **save(output_path: str) -> bool**

Salva o documento modificado.

```python
success = editor.save("output.pdf")

if success:
    print("Documento salvo com sucesso")
else:
    print("Erro ao salvar documento")
```

**Retorna:** `True` se salvo com sucesso, `False` caso contrário.

---

#### **save_versions(base_path: str) -> Dict[str, str]**

Salva múltiplas versões com diferentes métodos.

```python
versions = editor.save_versions("documento")

# Verificar versões criadas
for method, file_path in versions.items():
    print(f"{method}: {file_path}")
```

**Retorna:** Dicionário com caminhos de cada versão.

---

#### **get_document_info() -> Dict[str, Any]**

Obtém informações do documento.

```python
info = editor.get_document_info()

print(f"Páginas: {info['page_count']}")
print(f"Instâncias de texto: {info['text_instances']}")
print(f"Tamanho: {info['file_size']} bytes")
print(f"Metadados: {info['metadata']}")
```

**Retorna:** Dicionário com informações do documento.

---

#### **close() -> None**

Fecha o documento e libera recursos.

```python
editor.close()
```

---

### **BatchProcessor**

#### **add_job(job: BatchJob) -> None**

Adiciona um job ao processador.

```python
processor = BatchProcessor()

job = BatchJob(
    input_file="contrato.pdf",
    output_file="contrato_editado.pdf",
    operations=[
        EditOperation("ACME Corporation", "TechStart Inc.")
    ]
)

processor.add_job(job)
```

---

#### **add_jobs_from_config(config_file: str) -> None**

Adiciona jobs a partir de arquivo de configuração.

```python
processor = BatchProcessor()
processor.add_jobs_from_config("config.json")
```

---

#### **add_directory(input_dir: str, output_dir: str, operations: List[EditOperation]) -> None**

Adiciona todos os PDFs de um diretório.

```python
processor = BatchProcessor()

operations = [
    EditOperation("texto antigo", "texto novo")
]

processor.add_directory("contratos/", "contratos_editados/", operations)
```

---

#### **process() -> Dict[str, Any]**

Processa todos os jobs.

```python
results = processor.process()

print(f"Total de jobs: {results['total_jobs']}")
print(f"Jobs bem-sucedidos: {results['successful_jobs']}")
print(f"Jobs com erro: {results['failed_jobs']}")
print(f"Tempo total: {results['total_time']:.2f} segundos")
```

**Retorna:** Dicionário com resultados do processamento.

---

## 💡 Exemplos de Código

### **Exemplo 1: Edição Simples**

```python
from core.pdf_editor import PDFEditor

# Criar editor
editor = PDFEditor()

# Carregar documento
editor.load("documento.pdf")

# Substituir texto
replacements = editor.replace_text_exact("texto antigo", "texto novo")
print(f"Feitas {replacements} substituições")

# Salvar resultado
editor.save("output.pdf")

# Fechar editor
editor.close()
```

---

### **Exemplo 2: Substituições Múltiplas**

```python
from core.pdf_editor import PDFEditor, EditOperation

# Criar editor
editor = PDFEditor()

# Carregar documento
editor.load("documento.pdf")

# Criar operações
operations = [
    EditOperation("texto1", "novo1"),
    EditOperation("texto2", "novo2"),
    EditOperation("texto3", "novo3")
]

# Processar em lote
results = editor.batch_replace(operations, method="layout-preserving")

# Verificar resultados
for op, count in results.items():
    print(f"{op}: {count} substituições")

# Salvar resultado
editor.save("output.pdf")

# Fechar editor
editor.close()
```

---

### **Exemplo 3: Preservação de Layout**

```python
from core.pdf_editor import PDFEditor

# Criar editor
editor = PDFEditor()

# Carregar documento
editor.load("documento_com_imagens.pdf")

# Substituir texto preservando gráficos e backgrounds
replacements = editor.replace_text_layout_preserving(
    "texto antigo",
    "texto novo"
)

print(f"Feitas {replacements} substituições")
print("Gráficos e backgrounds foram preservados")

# Salvar resultado
editor.save("output.pdf")

# Fechar editor
editor.close()
```

---

### **Exemplo 4: Busca e Substituição**

```python
from core.pdf_editor import PDFEditor

# Criar editor
editor = PDFEditor()

# Carregar documento
editor.load("documento.pdf")

# Buscar texto
results = editor.search_text("texto a buscar")

print(f"Encontradas {len(results)} ocorrências:")
for instance in results:
    print(f"  Página {instance.page_num}: {instance.text}")

# Substituir se encontrado
if results:
    replacements = editor.replace_text_exact("texto a buscar", "texto novo")
    print(f"Feitas {replacements} substituições")
    
    # Salvar resultado
    editor.save("output.pdf")

# Fechar editor
editor.close()
```

---

### **Exemplo 5: Processamento em Lote**

```python
from core.batch_processor import BatchProcessor, BatchJob, EditOperation

# Criar processador
processor = BatchProcessor()

# Adicionar jobs
jobs = [
    BatchJob(
        input_file="contrato1.pdf",
        output_file="contrato1_editado.pdf",
        operations=[
            EditOperation("ACME Corporation", "TechStart Inc."),
            EditOperation("2023", "2024")
        ],
        method="layout-preserving"
    ),
    BatchJob(
        input_file="contrato2.pdf",
        output_file="contrato2_editado.pdf",
        operations=[
            EditOperation("ACME Corporation", "TechStart Inc."),
            EditOperation("2023", "2024")
        ],
        method="layout-preserving"
    )
]

for job in jobs:
    processor.add_job(job)

# Processar todos os jobs
results = processor.process()

print(f"Processamento concluído:")
print(f"  Total: {results['total_jobs']}")
print(f"  Sucesso: {results['successful_jobs']}")
print(f"  Erros: {results['failed_jobs']}")
```

---

### **Exemplo 6: Processamento de Diretório**

```python
from core.batch_processor import BatchProcessor, EditOperation

# Criar processador
processor = BatchProcessor()

# Definir operações
operations = [
    EditOperation("texto antigo", "texto novo"),
    EditOperation("outro texto", "novo texto")
]

# Adicionar todos os PDFs de um diretório
processor.add_directory(
    input_dir="documentos/",
    output_dir="documentos_editados/",
    operations=operations
)

# Processar todos os PDFs
results = processor.process()

print(f"Processamento concluído:")
print(f"  Total: {results['total_jobs']}")
print(f"  Sucesso: {results['successful_jobs']}")
print(f"  Erros: {results['failed_jobs']}")
```

---

### **Exemplo 7: Validação de Resultados**

```python
from core.pdf_editor import PDFEditor

# Criar editor
editor = PDFEditor()

# Carregar documento
editor.load("documento.pdf")

# Buscar texto antes da substituição
antes = editor.search_text("texto a buscar")
print(f"Antes: {len(antes)} ocorrências")

# Substituir
replacements = editor.replace_text_layout_preserving(
    "texto a buscar",
    "texto novo"
)

# Buscar texto após substituição
depois = editor.search_text("texto novo")
print(f"Depois: {len(depois)} ocorrências")

# Verificar se texto antigo foi removido
restantes = editor.search_text("texto a buscar")
print(f"Restantes: {len(restantes)} ocorrências")

# Salvar se tudo estiver correto
if len(depois) > 0 and len(restantes) == 0:
    editor.save("output.pdf")
    print("Substituição validada e salva")
else:
    print("Substituição não validada")

# Fechar editor
editor.close()
```

---

### **Exemplo 8: Tratamento de Erros**

```python
from core.pdf_editor import PDFEditor

try:
    # Criar editor
    editor = PDFEditor()
    
    # Carregar documento
    if not editor.load("documento.pdf"):
        raise Exception("Erro ao carregar documento")
    
    # Substituir texto
    replacements = editor.replace_text_layout_preserving(
        "texto antigo",
        "texto novo"
    )
    
    if replacements == 0:
        print("Aviso: Nenhuma substituição realizada")
    else:
        print(f"Feitas {replacements} substituições")
        
        # Salvar resultado
        if not editor.save("output.pdf"):
            raise Exception("Erro ao salvar documento")
        
        print("Documento salvo com sucesso")
    
    # Fechar editor
    editor.close()
    
except Exception as e:
    print(f"Erro: {e}")
    # Tratamento de erro adicional
```

---

## 🎨 Boas Práticas

### **1. Sempre Fechar o Editor**

```python
# ✅ Bom
editor = PDFEditor()
editor.load("documento.pdf")
editor.replace_text_exact("texto", "novo")
editor.save("output.pdf")
editor.close()

# ❌ Ruim
editor = PDFEditor()
editor.load("documento.pdf")
editor.replace_text_exact("texto", "novo")
editor.save("output.pdf")
# editor.close() não foi chamado
```

---

### **2. Usar Context Manager (se disponível)**

```python
# ✅ Bom (usando try-finally)
editor = PDFEditor()
try:
    editor.load("documento.pdf")
    editor.replace_text_exact("texto", "novo")
    editor.save("output.pdf")
finally:
    editor.close()
```

---

### **3. Validar Operações**

```python
# ✅ Bom - Validar antes de processar
editor = PDFEditor()
editor.load("documento.pdf")

# Buscar texto primeiro
results = editor.search_text("texto a buscar")
if not results:
    print("Texto não encontrado")
    editor.close()
    exit()

# Depois substituir
replacements = editor.replace_text_exact("texto a buscar", "texto novo")
editor.save("output.pdf")
editor.close()
```

---

### **4. Escolher o Método Certo**

```python
# ✅ Bom - Escolher método apropriado
from core.pdf_editor import PDFEditor

editor = PDFEditor()
editor.load("documento.pdf")

# Para documentos simples
editor.replace_text_exact("texto", "novo")

# Para documentos com imagens
editor.replace_text_layout_preserving("texto", "novo")

# Para documentos com backgrounds coloridos
editor.replace_text_background_preserving("texto", "novo")

editor.save("output.pdf")
editor.close()
```

---

### **5. Tratar Erros Adequadamente**

```python
# ✅ Bom - Tratamento de erros
from core.pdf_editor import PDFEditor

def editar_pdf(input_path, output_path, search, replace, method="exact"):
    editor = PDFEditor()
    try:
        if not editor.load(input_path):
            print(f"Erro ao carregar {input_path}")
            return False
        
        if method == "layout-preserving":
            replacements = editor.replace_text_layout_preserving(search, replace)
        elif method == "background-preserving":
            replacements = editor.replace_text_background_preserving(search, replace)
        else:
            replacements = editor.replace_text_exact(search, replace)
        
        if replacements == 0:
            print(f"Aviso: Nenhuma substituição em {input_path}")
            return False
        
        if not editor.save(output_path):
            print(f"Erro ao salvar {output_path}")
            return False
        
        print(f"Sucesso: {replacements} substituições em {input_path}")
        return True
    
    except Exception as e:
        print(f"Erro ao processar {input_path}: {e}")
        return False
    
    finally:
        editor.close()

# Usar a função
editar_pdf("documento.pdf", "output.pdf", "texto antigo", "texto novo", "layout-preserving")
```

---

### **6. Logging e Debug**

```python
# ✅ Bom - Adicionar logging
import logging
from core.pdf_editor import PDFEditor

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def editar_pdf_com_logging(input_path, output_path, search, replace):
    logger.info(f"Processando {input_path}")
    
    editor = PDFEditor()
    try:
        editor.load(input_path)
        
        logger.info(f"Buscando: {search}")
        results = editor.search_text(search)
        logger.info(f"Encontradas {len(results)} ocorrências")
        
        replacements = editor.replace_text_layout_preserving(search, replace)
        logger.info(f"Feitas {replacements} substituições")
        
        editor.save(output_path)
        logger.info(f"Salvo: {output_path}")
        
    except Exception as e:
        logger.error(f"Erro: {e}")
    
    finally:
        editor.close()
```

---

## 📚 Recursos Adicionais

- [README.md](../README.md) - Visão geral do projeto
- [docs/DOCUMENTACAO_COMPLETA.md](DOCUMENTACAO_COMPLETA.md) - Documentação completa
- [docs/LAYOUT_PRESERVATION.md](LAYOUT_PRESERVATION.md) - Preservação de layout
- [docs/GUIA_CLI.md](GUIA_CLI.md) - Guia da interface de linha de comando
- [docs/GUIA_GUI.md](GUIA_GUI.md) - Guia da interface gráfica
- [docs/GUIA_TUI.md](GUIA_TUI.md) - Guia da interface terminal
