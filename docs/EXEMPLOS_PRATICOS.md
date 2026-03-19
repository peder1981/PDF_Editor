# 💡 Exemplos Práticos do PDF Editor

## 📋 Índice

1. [Introdução](#introdução)
2. [Exemplos Básicos](#exemplos-básicos)
3. [Exemplos Intermediários](#exemplos-intermediários)
4. [Exemplos Avançados](#exemplos-avançados)
5. [Casos de Uso Reais](#casos-de-uso-reais)
6. [Scripts Prontos](#scripts-prontos)

---

## 🚀 Introdução

Este documento fornece exemplos práticos e scripts prontos para uso do PDF Editor em diferentes cenários.

---

## 📖 Exemplos Básicos

### **Exemplo 1: Substituição Simples**

Substituir um texto específico em um PDF.

```bash
# Via CLI
python3 -m interfaces.cli replace documento.pdf \
  "texto antigo" \
  "texto novo" \
  output.pdf
```

```python
# Via Python API
from core.pdf_editor import PDFEditor

editor = PDFEditor()
editor.load("documento.pdf")
editor.replace_text_exact("texto antigo", "texto novo")
editor.save("output.pdf")
editor.close()
```

---

### **Exemplo 2: Substituição com Preservação de Layout**

Substituir texto mantendo gráficos e backgrounds.

```bash
# Via CLI
python3 -m interfaces.cli replace documento.pdf \
  "texto antigo" \
  "texto novo" \
  output.pdf \
  --method layout-preserving
```

```python
# Via Python API
from core.pdf_editor import PDFEditor

editor = PDFEditor()
editor.load("documento.pdf")
editor.replace_text_layout_preserving("texto antigo", "texto novo")
editor.save("output.pdf")
editor.close()
```

---

### **Exemplo 3: Busca de Texto**

Encontrar todas as ocorrências de um texto.

```bash
# Via CLI
python3 -m interfaces.cli search documento.pdf "texto a buscar"
```

```python
# Via Python API
from core.pdf_editor import PDFEditor

editor = PDFEditor()
editor.load("documento.pdf")
results = editor.search_text("texto a buscar")

for instance in results:
    print(f"Página {instance.page_num}: {instance.text}")

editor.close()
```

---

## 🔧 Exemplos Intermediários

### **Exemplo 4: Múltiplas Substituições**

Realizar várias substituições no mesmo documento.

```bash
# Via CLI (sequencial)
python3 -m interfaces.cli replace documento.pdf \
  "texto1" \
  "novo1" \
  temp1.pdf

python3 -m interfaces.cli replace temp1.pdf \
  "texto2" \
  "novo2" \
  temp2.pdf

python3 -m interfaces.cli replace temp2.pdf \
  "texto3" \
  "novo3" \
  output.pdf
```

```python
# Via Python API (batch)
from core.pdf_editor import PDFEditor, EditOperation

editor = PDFEditor()
editor.load("documento.pdf")

operations = [
    EditOperation("texto1", "novo1"),
    EditOperation("texto2", "novo2"),
    EditOperation("texto3", "novo3")
]

results = editor.batch_replace(operations, method="layout-preserving")
for op, count in results.items():
    print(f"{op}: {count} substituições")

editor.save("output.pdf")
editor.close()
```

---

### **Exemplo 5: Processamento em Lote**

Processar múltiplos PDFs com as mesmas substituições.

```bash
# Via CLI
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

```python
# Via Python API
from core.batch_processor import BatchProcessor, EditOperation

processor = BatchProcessor()
operations = [
    EditOperation("texto antigo", "texto novo")
]

processor.add_directory("pasta_entrada/", "pasta_saida/", operations)
results = processor.process()

print(f"Processados {results['total_jobs']} arquivos")
print(f"Sucesso: {results['successful_jobs']}")
print(f"Erros: {results['failed_jobs']}")
```

---

### **Exemplo 6: Atualizar Atestado Médico**

Atualizar nome, idade e data em um atestado médico.

```bash
# Via CLI
python3 -m interfaces.cli replace atestado.pdf \
  "Marcelo de Freitas Ferreira" \
  "Fernando Augusto Vargas Rodrigues Paes" \
  atestado_atualizado.pdf \
  --method layout-preserving

python3 -m interfaces.cli replace atestado_atualizado.pdf \
  "46 anos" \
  "36 anos" \
  atestado_atualizado.pdf \
  --method layout-preserving

python3 -m interfaces.cli replace atestado_atualizado.pdf \
  "19 de agosto de 1979" \
  "29 de maio de 1989" \
  atestado_final.pdf \
  --method layout-preserving
```

```python
# Via Python API
from core.pdf_editor import PDFEditor, EditOperation

editor = PDFEditor()
editor.load("atestado.pdf")

operations = [
    EditOperation("Marcelo de Freitas Ferreira", "Fernando Augusto Vargas Rodrigues Paes"),
    EditOperation("46 anos", "36 anos"),
    EditOperation("19 de agosto de 1979", "29 de maio de 1989")
]

results = editor.batch_replace(operations, method="layout-preserving")
editor.save("atestado_final.pdf")
editor.close()
```

---

## 🚀 Exemplos Avançados

### **Exemplo 7: Script de Validação**

Script que valida substituições antes de aplicar.

```python
#!/usr/bin/env python3
"""
Script de validação de substituições em PDFs
"""

from core.pdf_editor import PDFEditor
import sys

def validar_e_substituir(input_path, output_path, search, replace, method="layout-preserving"):
    """Valida e substitui texto em PDF"""
    
    print(f"📄 Processando: {input_path}")
    print(f"🔍 Buscando: {search}")
    
    editor = PDFEditor()
    
    try:
        # Carregar documento
        if not editor.load(input_path):
            print(f"❌ Erro ao carregar {input_path}")
            return False
        
        # Buscar texto
        results = editor.search_text(search)
        
        if not results:
            print(f"⚠️  Texto '{search}' não encontrado")
            return False
        
        print(f"✅ Encontradas {len(results)} ocorrências:")
        for instance in results:
            print(f"   Página {instance.page_num}: {instance.text[:50]}...")
        
        # Confirmar substituição
        resposta = input(f"🤔 Deseja substituir '{search}' por '{replace}'? (s/n): ")
        
        if resposta.lower() != 's':
            print("❌ Substituição cancelada")
            return False
        
        # Substituir
        if method == "layout-preserving":
            replacements = editor.replace_text_layout_preserving(search, replace)
        elif method == "background-preserving":
            replacements = editor.replace_text_background_preserving(search, replace)
        else:
            replacements = editor.replace_text_exact(search, replace)
        
        print(f"✅ Feitas {replacements} substituições")
        
        # Salvar
        if not editor.save(output_path):
            print(f"❌ Erro ao salvar {output_path}")
            return False
        
        print(f"✅ Salvo: {output_path}")
        return True
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    finally:
        editor.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python3 validar_e_substituir.py <input> <output> <busca> <substituição>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    search = sys.argv[3]
    replace = sys.argv[4]
    
    if validar_e_substituir(input_path, output_path, search, replace):
        print("🎉 Processamento concluído com sucesso!")
        sys.exit(0)
    else:
        print("❌ Processamento falhou")
        sys.exit(1)
```

**Uso:**
```bash
python3 validar_e_substituir.py documento.pdf output.pdf "texto antigo" "texto novo"
```

---

### **Exemplo 8: Script de Processamento em Lote com Validação**

Processa múltiplos PDFs com validação individual.

```python
#!/usr/bin/env python3
"""
Script de processamento em lote com validação
"""

from core.pdf_editor import PDFEditor, EditOperation
from pathlib import Path
import json

def processar_lote_com_validacao(input_dir, output_dir, config_file):
    """Processa PDFs em lote com validação"""
    
    # Carregar configuração
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Encontrar todos os PDFs
    pdf_files = list(input_path.glob("*.pdf"))
    
    print(f"📁 Encontrados {len(pdf_files)} PDFs em {input_dir}")
    
    # Processar cada PDF
    for pdf_file in pdf_files:
        print(f"\n📄 Processando: {pdf_file.name}")
        
        editor = PDFEditor()
        
        try:
            # Carregar documento
            if not editor.load(str(pdf_file)):
                print(f"❌ Erro ao carregar {pdf_file.name}")
                continue
            
            # Buscar cada texto
            for replacement in config["replacements"]:
                search = replacement["search"]
                replace = replacement["replace"]
                case_sensitive = replacement.get("case_sensitive", False)
                
                results = editor.search_text(search, case_sensitive)
                
                if results:
                    print(f"✅ Encontrado '{search}': {len(results)} ocorrências")
                else:
                    print(f"⚠️  Não encontrado '{search}'")
            
            # Confirmar processamento
            resposta = input(f"🤔 Processar {pdf_file.name}? (s/n): ")
            
            if resposta.lower() != 's':
                print(f"⏭️  Pulando {pdf_file.name}")
                editor.close()
                continue
            
            # Aplicar substituições
            operations = [
                EditOperation(
                    r["search"],
                    r["replace"],
                    case_sensitive=r.get("case_sensitive", False)
                )
                for r in config["replacements"]
            ]
            
            method = config.get("method", "exact")
            results = editor.batch_replace(operations, method=method)
            
            # Salvar
            output_file = output_path / pdf_file.name
            if editor.save(str(output_file)):
                print(f"✅ Salvo: {output_file.name}")
            else:
                print(f"❌ Erro ao salvar {output_file.name}")
        
        except Exception as e:
            print(f"❌ Erro ao processar {pdf_file.name}: {e}")
        
        finally:
            editor.close()
    
    print(f"\n🎉 Processamento concluído!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 4:
        print("Uso: python3 processar_lote.py <input_dir> <output_dir> <config>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    config_file = sys.argv[3]
    
    processar_lote_com_validacao(input_dir, output_dir, config_file)
```

**Uso:**
```bash
python3 processar_lote.py contratos/ contratos_editados/ config.json
```

---

### **Exemplo 9: Script de Comparação de PDFs**

Compara PDFs antes e depois das alterações.

```python
#!/usr/bin/env python3
"""
Script de comparação de PDFs
"""

from core.pdf_editor import PDFEditor
from pathlib import Path
import sys

def comparar_pdfs(original_path, modificado_path):
    """Compara dois PDFs"""
    
    print("📊 Comparando PDFs:")
    print(f"  Original: {original_path}")
    print(f"  Modificado: {modificado_path}")
    print()
    
    # Carregar documentos
    editor_original = PDFEditor()
    editor_modificado = PDFEditor()
    
    try:
        if not editor_original.load(original_path):
            print(f"❌ Erro ao carregar {original_path}")
            return
        
        if not editor_modificado.load(modificado_path):
            print(f"❌ Erro ao carregar {modificado_path}")
            return
        
        # Comparar informações
        info_original = editor_original.get_document_info()
        info_modificado = editor_modificado.get_document_info()
        
        print("📋 Informações:")
        print(f"  Original:")
        print(f"    Páginas: {info_original['page_count']}")
        print(f"    Instâncias de texto: {info_original['text_instances']}")
        print(f"    Tamanho: {info_original['file_size']} bytes")
        
        print(f"  Modificado:")
        print(f"    Páginas: {info_modificado['page_count']}")
        print(f"    Instâncias de texto: {info_modificado['text_instances']}")
        print(f"    Tamanho: {info_modificado['file_size']} bytes")
        
        # Comparar instâncias de texto
        print(f"\n📝 Comparação de texto:")
        print(f"  Diferença de instâncias: {info_modificado['text_instances'] - info_original['text_instances']}")
        
        # Buscar diferenças específicas
        print(f"\n🔍 Análise de diferenças:")
        
        # Exemplo: buscar texto específico
        textos_buscar = ["texto antigo", "texto novo"]
        
        for texto in textos_buscar:
            count_original = len(editor_original.search_text(texto))
            count_modificado = len(editor_modificado.search_text(texto))
            
            if count_original > 0:
                print(f"  '{texto}':")
                print(f"    Original: {count_original} ocorrências")
                print(f"    Modificado: {count_modificado} ocorrências")
            
            if count_modificado > 0 and count_original == 0:
                print(f"  '{texto}':")
                print(f"    Original: 0 ocorrências")
                print(f"    Modificado: {count_modificado} ocorrências (NOVO)")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    finally:
        editor_original.close()
        editor_modificado.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 comparar_pdfs.py <original> <modificado>")
        sys.exit(1)
    
    original_path = sys.argv[1]
    modificado_path = sys.argv[2]
    
    comparar_pdfs(original_path, modificado_path)

"""
Atualiza contratos com novo ano e empresa
"""

from core.pdf_editor import PDFEditor
from pathlib import Path

def atualizar_contratos(diretorio_contratos, novo_ano, nova_empresa):
    """Atualiza contratos com novo ano e empresa"""
    
    diretorio = Path(diretorio_contratos)
    pdf_files = list(diretorio.glob("*.pdf"))
    
    print(f"📄 Encontrados {len(pdf_files)} contratos")
    
    for pdf_file in pdf_files:
        print(f"\n📄 Processando: {pdf_file.name}")
        
        editor = PDFEditor()
        
        try:
            editor.load(str(pdf_file))
            
            # Substituir ano
            ano_antigo = str(int(novo_ano) - 1)
            editor.replace_text_layout_preserving(ano_antigo, novo_ano)
            
            # Substituir empresa
            editor.replace_text_layout_preserving("ACME Corporation", nova_empresa)
            
            # Salvar
            output_file = pdf_file.parent / f"{pdf_file.stem}_atualizado{pdf_file.suffix}"
            editor.save(str(output_file))
            
            print(f"✅ Atualizado: {output_file.name}")
        
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        finally:
            editor.close()
    
    print(f"\n🎉 Atualização concluída!")

if __name__ == "__main__":
    atualizar_contratos(
        "contratos/",
        "2024",
        "TechStart Inc."
    )

"""
Processa formulários de inscrição substituindo dados
"""

from core.pdf_editor import PDFEditor
import json

def processar_formulario(template_path, dados_saida, output_path):
    """Processa formulário com dados de saída"""
    
    # Carregar dados
    with open(dados_saida, 'r') as f:
        dados = json.load(f)
    
    editor = PDFEditor()
    
    try:
        editor.load(template_path)
        
        # Substituir campos do formulário
        for campo, valor in dados.items():
            # Preservar backgrounds coloridos do formulário
            editor.replace_text_background_preserving(f"{{campo}}", valor)
        
        editor.save(output_path)
        print(f"✅ Formulário processado: {output_path}")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    finally:
        editor.close()

if __name__ == "__main__":
    # Exemplo de dados
    dados = {
        "nome": "João Silva",
        "idade": "30",
        "email": "joao.silva@email.com",
        "telefone": "(11) 99999-9999"
    }
    
    # Salvar dados em JSON
    with open("dados_saida.json", 'w') as f:
        json.dump(dados, f, indent=2)
    
    # Processar formulário
    processar_formulario(
        "formulario_template.pdf",
        "dados_saida.json",
        "formulario_preenchido.pdf"
    )

"""
Gera relatórios personalizados substituindo dados
"""

from core.pdf_editor import PDFEditor
from datetime import datetime

def gerar_relatorio(template_path, dados_relatorio, output_path):
    """Gera relatório personalizado"""
    
    editor = PDFEditor()
    
    try:
        editor.load(template_path)
        
        # Substituir data atual
        data_atual = datetime.now().strftime("%d/%m/%Y")
        editor.replace_text_layout_preserving("{{DATA}}", data_atual)
        
        # Substituir dados do relatório
        for chave, valor in dados_relatorio.items():
            editor.replace_text_layout_preserving(f"{{{chave}}}", str(valor))
        
        editor.save(output_path)
        print(f"✅ Relatório gerado: {output_path}")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    finally:
        editor.close()

if __name__ == "__main__":
    # Exemplo de dados de relatório
    dados = {
        "CLIENTE": "TechStart Inc.",
        "PROJETO": "Sistema de Gestão",
        "ORÇAMENTO": "R$ 50.000,00",
        "PRAZO": "30 dias",
        "RESPONSÁVEL": "João Silva"
    }
    
    gerar_relatorio(
        "relatorio_template.pdf",
        dados,
        f"relatorio_{datetime.now().strftime('%Y%m%d')}.pdf"
    )

"""
Atualizador de Atestados Médicos
"""

from core.pdf_editor import PDFEditor, EditOperation

def atualizar_atestado(input_path, output_path, dados):
    """Atualiza atestado médico com novos dados"""
    
    editor = PDFEditor()
    
    try:
        editor.load(input_path)
        
        operations = [
            EditOperation(dados.get('nome_antigo', ''), dados.get('nome_novo', '')),
            EditOperation(dados.get('idade_antiga', ''), dados.get('idade_nova', '')),
            EditOperation(dados.get('data_antiga', ''), dados.get('data_nova', ''))
        ]
        
        results = editor.batch_replace(operations, method="layout-preserving")
        
        total = sum(results.values())
        print(f"✅ Feitas {total} substituições")
        
        editor.save(output_path)
        print(f"✅ Salvo: {output_path}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    finally:
        editor.close()

if __name__ == "__main__":
    dados = {
        'nome_antigo': 'Marcelo de Freitas Ferreira',
        'nome_novo': 'Fernando Augusto Vargas Rodrigues Paes',
        'idade_antiga': '46 anos',
        'idade_nova': '36 anos',
        'data_antiga': '19 de agosto de 1979',
        'data_nova': '29 de maio de 1989'
    }
    
    atualizar_atestado(
        'atestado.pdf',
        'atestado_atualizado.pdf',
        dados
    )
```

---

### **Script 2: Processador de Contratos**

```python
#!/usr/bin/env python3
"""
Processador de Contratos em Lote
"""

from core.batch_processor import BatchProcessor, EditOperation

def processar_contratos(input_dir, output_dir):
    """Processa contratos em lote"""
    
    processor = BatchProcessor()
    
    operations = [
        EditOperation("ACME Corporation", "TechStart Inc."),
        EditOperation("2023", "2024"),
        EditOperation("João Silva", "Maria Santos")
    ]
    
    processor.add_directory(input_dir, output_dir, operations)
    
    results = processor.process()
    
    print(f"📊 Resultados:")
    print(f"  Total: {results['total_jobs']}")
    print(f"  Sucesso: {results['successful_jobs']}")
    print(f"  Erros: {results['failed_jobs']}")
    print(f"  Tempo: {results['total_time']:.2f}s")

if __name__ == "__main__":
    processar_contratos(
        'contratos/',
        'contratos_atualizados/'
    )
```

---

### **Script 3: Validador de Substituições**

```python
#!/usr/bin/env python3
"""
Validador de Substituições em PDFs
"""

from core.pdf_editor import PDFEditor

def validar_substituicoes(input_path, output_path, substituicoes):
    """Valida e aplica substituições"""
    
    editor = PDFEditor()
    
    try:
        editor.load(input_path)
        
        # Validar cada substituição
        for search, replace in substituicoes:
            results = editor.search_text(search)
            
            if results:
                print(f"✅ Encontrado '{search}': {len(results)} ocorrências")
            else:
                print(f"⚠️  Não encontrado '{search}'")
        
        # Confirmar
        resposta = input("🤔 Aplicar substituições? (s/n): ")
        
        if resposta.lower() != 's':
            print("❌ Cancelado")
            return
        
        # Aplicar substituições
        for search, replace in substituicoes:
            editor.replace_text_layout_preserving(search, replace)
        
        editor.save(output_path)
        print(f"✅ Salvo: {output_path}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    finally:
        editor.close()

if __name__ == "__main__":
    substituicoes = [
        ("texto1", "novo1"),
        ("texto2", "novo2"),
        ("texto3", "novo3")
    ]
    
    validar_substituicoes(
        'documento.pdf',
        'output.pdf',
        substituicoes
    )
```

---

## 📚 Recursos Adicionais

- [README.md](../README.md) - Visão geral do projeto
- [docs/DOCUMENTACAO_COMPLETA.md](DOCUMENTACAO_COMPLETA.md) - Documentação completa
- [docs/LAYOUT_PRESERVATION.md](LAYOUT_PRESERVATION.md) - Preservação de layout
- [docs/GUIA_CLI.md](GUIA_CLI.md) - Guia da interface de linha de comando
- [docs/GUIA_GUI.md](GUIA_GUI.md) - Guia da interface gráfica
- [docs/GUIA_TUI.md](GUIA_TUI.md) - Guia da interface terminal
- [docs/GUIA_API.md](GUIA_API.md) - Guia da API Python
