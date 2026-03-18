# 🔧 Guia de Solução de Problemas (Troubleshooting)

## 📋 Índice

1. [Introdução](#introdução)
2. [Problemas Comuns](#problemas-comuns)
3. [Erros de Instalação](#erros-de-instalação)
4. [Erros de Execução](#erros-de-execução)
5. [Problemas de Performance](#problemas-de-performance)
6. [Soluções Avançadas](#soluções-avançadas)

---

## 🚀 Introdução

Este guia ajuda a resolver problemas comuns ao usar o PDF Editor, desde instalação até execução avançada.

### **Soluções Aplicadas Recentemente**

✅ **TUI MountError - Resolvido**
- **Problema:** `MountError: Can't mount <class 'generator'>; expected a Widget instance.`
- **Causa:** Métodos auxiliares usavam yield statements, criando generators em vez de widgets
- **Solução:** Removido yield statements de métodos auxiliares (`_create_source_section()`, `_create_replacements_section()`, `_create_process_section()`)
- **Resultado:** TUI carrega corretamente sem erros

✅ **TUI AttributeError - Resolvido**
- **Problema:** `AttributeError: 'UnifiedTUIMain' object has no attribute 'single_mode_btn'`
- **Causa:** Botões não eram referenciados corretamente no código
- **Solução:** Adicionado query_one para acessar botões por ID em vez de usar referências self
- **Resultado:** Eventos de botões funcionam corretamente

✅ **CLI Unknown Method Error - Resolvido**
- **Problema:** `Error: Unknown method 'layout-preserving'`
- **Causa:** CLI não reconhecia os novos métodos de preservação
- **Solução:** Adicionado suporte para métodos `layout-preserving` e `background-preserving` no CLI
- **Resultado:** Todos os métodos funcionam via CLI

✅ **Unit Test Import Error - Resolvido**
- **Problema:** `ModuleNotFoundError: No module named 'pdf_editor'`
- **Causa:** Import paths não correspondiam à nova estrutura do projeto
- **Solução:** Corrigidos import paths para usar `core.pdf_editor` e `core.batch_processor`
- **Resultado:** Testes unitários executam corretamente (10/11 passaram)

---

## ⚠️ Problemas Comuns

### **Problema 1: PDF Não Carrega**

#### **Sintomas**
```
Error loading PDF: [erro específico]
```

#### **Causas Possíveis**
- Arquivo PDF corrompido
- PDF protegido por senha
- Permissões de arquivo insuficientes
- Caminho do arquivo incorreto

#### **Soluções**

**1. Verificar se o arquivo existe**
```bash
ls -la documento.pdf
```

**2. Verificar permissões**
```bash
chmod 644 documento.pdf
```

**3. Testar com outro PDF**
```bash
python3 -m interfaces.cli info outro_documento.pdf
```

**4. Verificar se PDF está corrompido**
```bash
# Usar ferramenta de validação de PDF
pdfinfo documento.pdf
```

**5. Se PDF está protegido por senha**
```python
# O PDF Editor atualmente não suporta PDFs protegidos
# Você precisará remover a proteção primeiro
```

---

### **Problema 2: Substituição Não Funciona**

#### **Sintomas**
```
No instances of 'texto' found
```

#### **Causas Possíveis**
- Texto não existe no PDF
- Case sensitivity incorreta
- Texto em formato diferente (OCR, fonte especial)
- Espaços ou caracteres especiais

#### **Soluções**

**1. Buscar o texto primeiro**
```bash
python3 -m interfaces.cli search documento.pdf "texto a buscar"
```

**2. Tentar sem case-sensitive**
```bash
python3 -m interfaces.cli replace documento.pdf \
  "Texto" \
  "Novo" \
  output.pdf \
  --case-sensitive
```

**3. Buscar parte do texto**
```bash
python3 -m interfaces.cli search documento.pdf "parte do texto"
```

**4. Verificar espaços e caracteres especiais**
```python
# Use aspas duplas para textos com espaços
python3 -m interfaces.cli replace documento.pdf \
  "texto com espaços" \
  "novo texto" \
  output.pdf
```

**5. Verificar se texto está em imagens (OCR)**
```python
# Texto em imagens não pode ser editado
# Use OCR para converter imagem em texto primeiro
```

---

### **Problema 3: Elementos Visuais Não Preservados**

#### **Sintomas**
- Gráficos desaparecem após substituição
- Backgrounds coloridos ficam brancos
- Imagens são removidas

#### **Causas Possíveis**
- Usando método `exact` em vez de `layout-preserving`
- PDF não tem elementos visuais
- Elementos visuais estão em camadas diferentes

#### **Soluções**

**1. Usar método correto**
```bash
# ❌ Errado - usa background branco
python3 -m interfaces.cli replace documento.pdf \
  "texto" \
  "novo" \
  output.pdf \
  --method exact

# ✅ Correto - preserva elementos visuais
python3 -m interfaces.cli replace documento.pdf \
  "texto" \
  "novo" \
  output.pdf \
  --method layout-preserving
```

**2. Verificar se PDF tem elementos visuais**
```bash
python3 -m interfaces.cli info documento.pdf
# Verifique se há imagens ou gráficos
```

**3. Usar background-preserving para backgrounds coloridos**
```bash
python3 -m interfaces.cli replace documento.pdf \
  "texto" \
  "novo" \
  output.pdf \
  --method background-preserving
```

**4. Testar com diferentes métodos**
```python
from core.pdf_editor import PDFEditor

editor = PDFEditor()
editor.load("documento.pdf")

# Testar cada método
methods = ["exact", "layout-preserving", "background-preserving"]

for method in methods:
    print(f"\n🧪 Testando método: {method}")
    if method == "exact":
        editor.replace_text_exact("texto", "novo")
    elif method == "layout-preserving":
        editor.replace_text_layout_preserving("texto", "novo")
    elif method == "background-preserving":
        editor.replace_text_background_preserving("texto", "novo")
    
    editor.save(f"test_{method}.pdf")
    print(f"✅ Salvo: test_{method}.pdf")

editor.close()
```

---

### **Problema 4: Fontes Não São Mantidas**

#### **Sintomas**
- Fonte do texto substituído é diferente
- Tamanho da fonte mudou
- Cor do texto mudou

#### **Causas Possíveis**
- Fonte original não está disponível
- Fonte original não é suportada pelo PyMuPDF
- Método usado não preserva fontes

#### **Soluções**

**1. Usar método que preserva fontes**
```bash
python3 -m interfaces.cli replace documento.pdf \
  "texto" \
  "novo" \
  output.pdf \
  --method structure
```

**2. Verificar fontes disponíveis**
```python
import fitz

doc = fitz.open("documento.pdf")
for page in doc:
    text_dict = page.get_text("dict")
    for block in text_dict["blocks"]:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    print(f"Fonte: {span['font']}, Tamanho: {span['size']}")
```

**3. Usar método layout-preserving**
```bash
python3 -m interfaces.cli replace documento.pdf \
  "texto" \
  "novo" \
  output.pdf \
  --method layout-preserving
```

---

## 🔧 Erros de Instalação

### **Erro 1: ModuleNotFoundError**

#### **Sintomas**
```
ModuleNotFoundError: No module named 'fitz'
```

#### **Solução**

```bash
# Instalar PyMuPDF
pip install PyMuPDF==1.23.14

# Ou instalar todas as dependências
pip install -r requirements.txt
```

---

### **Erro 2: No module named 'tkinter'**

#### **Sintomas**
```
ModuleNotFoundError: No module named 'tkinter'
```

#### **Solução**

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL/Fedora
sudo yum install python3-tkinter

# macOS (já incluído)
# Windows (já incluído)
```

---

### **Erro 3: Permission Denied**

#### **Sintomas**
```
PermissionError: [Errno 13] Permission denied
```

#### **Solução**

```bash
# Verificar permissões
ls -la documento.pdf

# Alterar permissões
chmod 644 documento.pdf

# Verificar permissões do diretório
ls -ld diretorio/

# Alterar permissões do diretório
chmod 755 diretorio/
```

---

## 🐛 Erros de Execução

### **Erro 1: UnicodeDecodeError**

#### **Sintomas**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

#### **Solução**

```python
# Especificar encoding ao ler arquivo
with open("config.json", 'r', encoding='utf-8') as f:
    config = json.load(f)
```

---

### **Erro 2: ValueError: need font file or buffer**

#### **Sintomas**
```
ValueError: need font file or buffer
```

#### **Causa**
Fonte personalizada não está disponível

#### **Solução**

```python
# O editor usa fontes padrão do PyMuPDF
# Não é necessário fornecer arquivos de fonte
# Se o erro persistir, use um método diferente
editor.replace_text_exact("texto", "novo")
```

---

### **Erro 3: AttributeError**

#### **Sintomas**
```
AttributeError: 'NoneType' object has no attribute '...'
```

#### **Causa**
Documento não foi carregado corretamente

#### **Solução**

```python
# Verificar se documento foi carregado
editor = PDFEditor()
if editor.load("documento.pdf"):
    # Documento carregado com sucesso
    editor.replace_text_exact("texto", "novo")
else:
    # Erro ao carregar
    print("Erro ao carregar documento")
```

---

## ⚡ Problemas de Performance

### **Problema 1: Processamento Lento**

#### **Sintomas**
- Processamento de PDFs demora muito
- Alto uso de CPU
- Memória elevada

#### **Soluções**

**1. Usar método mais rápido**
```bash
# Use 'exact' para documentos simples
python3 -m interfaces.cli replace documento.pdf \
  "texto" \
  "novo" \
  output.pdf \
  --method exact
```

**2. Processar em lote com paralelismo**
```python
from concurrent.futures import ThreadPoolExecutor
from core.pdf_editor import PDFEditor

def processar_pdf(input_path, output_path, search, replace):
    editor = PDFEditor()
    editor.load(input_path)
    editor.replace_text_exact(search, replace)
    editor.save(output_path)
    editor.close()

# Processar em paralelo
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = []
    for pdf_file in pdf_files:
        future = executor.submit(
            processar_pdf,
            pdf_file,
            f"editado/{pdf_file}",
            "texto",
            "novo"
        )
        futures.append(future)
    
    for future in futures:
        future.result()
```

**3. Otimizar para PDFs grandes**
```python
# Processar página por página
from core.pdf_editor import PDFEditor

editor = PDFEditor()
editor.load("documento_grande.pdf")

# Processar apenas páginas específicas
for page_num in [0, 1, 2]:  # Páginas 1, 2, 3
    # Implementar processamento por página
    pass

editor.save("output.pdf")
editor.close()
```

---

### **Problema 2: Alto Uso de Memória**

#### **Sintomas**
- Processamento consome muita memória
- Erro "Out of memory"

#### **Soluções**

**1. Processar um PDF por vez**
```python
from core.pdf_editor import PDFEditor

def processar_sequencialmente(pdf_files):
    for pdf_file in pdf_files:
        editor = PDFEditor()
        editor.load(pdf_file)
        editor.replace_text_exact("texto", "novo")
        editor.save(f"editado/{pdf_file}")
        editor.close()  # Libera memória
```

**2. Fechar editor após cada processamento**
```python
editor = PDFEditor()
editor.load("documento.pdf")
editor.replace_text_exact("texto", "novo")
editor.save("output.pdf")
editor.close()  # Importante: libera memória
```

---

## 🔬 Soluções Avançadas

### **Solução 1: Debug Detalhado**

```python
import logging
from core.pdf_editor import PDFEditor

# Configurar logging detalhado
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def processar_com_debug(input_path, output_path, search, replace):
    logger.info(f"Processando: {input_path}")
    
    editor = PDFEditor()
    
    try:
        logger.debug("Carregando documento...")
        if not editor.load(input_path):
            logger.error("Erro ao carregar documento")
            return False
        
        logger.debug("Buscando texto...")
        results = editor.search_text(search)
        logger.debug(f"Encontradas {len(results)} ocorrências")
        
        for instance in results:
            logger.debug(f"  Página {instance.page_num}: {instance.text}")
        
        logger.debug("Substituindo texto...")
        replacements = editor.replace_text_layout_preserving(search, replace)
        logger.debug(f"Feitas {replacements} substituições")
        
        logger.debug("Salvando documento...")
        if not editor.save(output_path):
            logger.error("Erro ao salvar documento")
            return False
        
        logger.info("Processamento concluído com sucesso")
        return True
    
    except Exception as e:
        logger.error(f"Erro durante processamento: {e}", exc_info=True)
        return False
    
    finally:
        logger.debug("Fechando editor...")
        editor.close()
```

---

### **Solução 2: Validação de Resultados**

```python
from core.pdf_editor import PDFEditor

def validar_resultado(original_path, modificado_path, search, replace):
    """Valida se substituição foi aplicada corretamente"""
    
    editor_original = PDFEditor()
    editor_modificado = PDFEditor()
    
    try:
        editor_original.load(original_path)
        editor_modificado.load(modificado_path)
        
        # Verificar se texto antigo foi removido
        restantes = editor_modificado.search_text(search)
        if restantes:
            print(f"❌ Texto antigo ainda presente: {len(restantes)} ocorrências")
            return False
        
        # Verificar se texto novo foi adicionado
        novos = editor_modificado.search_text(replace)
        if not novos:
            print(f"❌ Texto novo não encontrado")
            return False
        
        print(f"✅ Validação bem-sucedida:")
        print(f"  Texto antigo removido")
        print(f"  Texto novo adicionado: {len(novos)} ocorrências")
        
        return True
    
    except Exception as e:
        print(f"❌ Erro na validação: {e}")
        return False
    
    finally:
        editor_original.close()
        editor_modificado.close()
```

---

### **Solução 3: Recuperação de Erros**

```python
from core.pdf_editor import PDFEditor
import shutil

def processar_com_backup(input_path, output_path, search, replace, method="layout-preserving"):
    """Processa PDF com backup automático"""
    
    # Criar backup
    backup_path = f"{input_path}.backup"
    shutil.copy2(input_path, backup_path)
    print(f"✅ Backup criado: {backup_path}")
    
    editor = PDFEditor()
    
    try:
        editor.load(input_path)
        
        # Processar
        if method == "layout-preserving":
            editor.replace_text_layout_preserving(search, replace)
        elif method == "background-preserving":
            editor.replace_text_background_preserving(search, replace)
        else:
            editor.replace_text_exact(search, replace)
        
        # Salvar
        if not editor.save(output_path):
            raise Exception("Erro ao salvar documento")
        
        # Validar resultado
        if validar_resultado(input_path, output_path, search, replace):
            print(f"✅ Processamento bem-sucedido")
            return True
        else:
            print(f"❌ Validação falhou, restaurando backup")
            shutil.copy2(backup_path, input_path)
            return False
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        print(f"🔄 Restaurando backup...")
        shutil.copy2(backup_path, input_path)
        return False
    
    finally:
        editor.close()
```

---

### **Solução 4: Diagnóstico Completo**

```python
from core.pdf_editor import PDFEditor
import fitz

def diagnostico_completo(pdf_path):
    """Realiza diagnóstico completo de um PDF"""
    
    print(f"🔍 Diagnóstico: {pdf_path}")
    print("=" * 60)
    
    # 1. Verificar se arquivo existe
    import os
    if not os.path.exists(pdf_path):
        print(f"❌ Arquivo não existe")
        return
    
    print(f"✅ Arquivo existe")
    print(f"   Tamanho: {os.path.getsize(pdf_path)} bytes")
    
    # 2. Tentar abrir com PyMuPDF
    try:
        doc = fitz.open(pdf_path)
        print(f"✅ PDF válido")
        print(f"   Páginas: {len(doc)}")
        print(f"   Metadados: {doc.metadata}")
        doc.close()
    except Exception as e:
        print(f"❌ PDF inválido: {e}")
        return
    
    # 3. Tentar carregar com PDF Editor
    editor = PDFEditor()
    try:
        if not editor.load(pdf_path):
            print(f"❌ Erro ao carregar com PDF Editor")
            return
        
        print(f"✅ Carregado com PDF Editor")
        
        # 4. Verificar instâncias de texto
        info = editor.get_document_info()
        print(f"✅ Informações do documento:")
        print(f"   Páginas: {info['page_count']}")
        print(f"   Instâncias de texto: {info['text_instances']}")
        
        # 5. Verificar imagens
        doc = fitz.open(pdf_path)
        images = doc.get_images()
        print(f"✅ Imagens encontradas: {len(images)}")
        
        # 6. Verificar desenhos
        drawings = doc.get_drawings()
        print(f"✅ Desenhos encontrados: {len(drawings)}")
        
        doc.close()
        
        print(f"\n✅ Diagnóstico concluído: PDF está saudável")
    
    except Exception as e:
        print(f"❌ Erro no diagnóstico: {e}")
    
    finally:
        editor.close()

if __name__ == "__main__":
    diagnostico_completo("documento.pdf")
```

---

## 📞 Obter Ajuda

### **Recursos de Documentação**

- [README.md](../README.md) - Visão geral
- [docs/DOCUMENTACAO_COMPLETA.md](DOCUMENTACAO_COMPLETA.md) - Documentação completa
- [docs/LAYOUT_PRESERVATION.md](LAYOUT_PRESERVATION.md) - Preservação de layout
- [docs/GUIA_CLI.md](GUIA_CLI.md) - Guia CLI
- [docs/GUIA_GUI.md](GUIA_GUI.md) - Guia GUI
- [docs/GUIA_TUI.md](GUIA_TUI.md) - Guia TUI
- [docs/GUIA_API.md](GUIA_API.md) - Guia API
- [docs/EXEMPLOS_PRATICOS.md](EXEMPLOS_PRATICOS.md) - Exemplos práticos

### **Comunidade**

- GitHub Issues: https://github.com/peder1981/PDF_Editor/issues
- Documentação: https://github.com/peder1981/PDF_Editor/tree/main/docs

### **Relatando Bugs**

Ao relatar bugs, inclua:

1. **Versão do Python**
   ```bash
   python3 --version
   ```

2. **Versão das Dependências**
   ```bash
   pip list | grep -E "(PyMuPDF|rich|textual|typer)"
   ```

3. **Comando Usado**
   ```bash
   # Comando completo que causou o erro
   ```

4. **Mensagem de Erro Completa**
   ```bash
   # Copie toda a mensagem de erro
   ```

5. **Descrição do PDF**
   - Tamanho do arquivo
   - Número de páginas
   - Elementos visuais (imagens, gráficos, backgrounds)

6. **Sistema Operacional**
   ```bash
   uname -a  # Linux
   sw_vers   # macOS
   ver       # Windows
   ```

---

## 🎯 Checklist de Solução de Problemas

Antes de pedir ajuda, verifique:

- [ ] PDF existe e tem permissões corretas
- [ ] PDF não está protegido por senha
- [ ] Dependências estão instaladas (`pip install -r requirements.txt`)
- [ ] Texto a buscar realmente existe no PDF
- [ ] Método correto está sendo usado
- [ ] Suficiente memória disponível
- [ ] Espaço em disco disponível
- [ ] Versão do Python é 3.8 ou superior
- [ ] Logs foram verificados
- [ ] Documentação foi consultada

---

## 📚 Resumo

Este guia cobre os problemas mais comuns ao usar o PDF Editor. Para problemas não cobertos aqui, consulte a documentação adicional ou abra uma issue no GitHub.
