# 🆕 Novos Métodos de Preservação de Layout

## 📋 Visão Geral

O PDF Editor agora inclui métodos avançados de preservação de layout que mantêm gráficos, backgrounds e outros elementos visuais intactos enquanto substituem apenas o texto solicitado.

## 🎯 Métodos Disponíveis

### 1. **Layout-Preserving** (Preservar Layout)

**Descrição:** Usa redação avançada para preservar todos os elementos visuais do documento enquanto substitui o texto.

**Quando Usar:**
- Documentos com imagens e gráficos
- PDFs com backgrounds coloridos
- Documentos com elementos decorativos
- Quando a integridade visual é crítica

**Como Funciona:**
1. Detecta e preserva imagens e gráficos vetoriais
2. Identifica cores de fundo e backgrounds
3. Usa redação transparente para manter o background original
4. Substitui apenas o texto solicitado

**Exemplo de Uso:**
```bash
python3 -m interfaces.cli replace documento.pdf \
  "texto antigo" \
  "texto novo" \
  output.pdf \
  --method layout-preserving
```

### 2. **Background-Preserving** (Preservar Background)

**Descrição:** Foca na preservação de cores de fundo e elementos decorativos do documento.

**Quando Usar:**
- Documentos com cores de fundo específicas
- PDFs com highlights ou marcações
- Documentos com elementos decorativos coloridos
- Quando o background é mais importante que gráficos complexos

**Como Funciona:**
1. Detecta cores de fundo e backgrounds
2. Preserva retângulos coloridos e highlights
3. Usa redação com background transparente
4. Mantém elementos decorativos intactos

**Exemplo de Uso:**
```bash
python3 -m interfaces.cli replace documento.pdf \
  "texto antigo" \
  "texto novo" \
  output.pdf \
  --method background-preserving
```

## 🔬 Comparação de Métodos

| Método | Preserva Imagens | Preserva Backgrounds | Preserva Gráficos | Velocidade | Complexidade |
|--------|------------------|---------------------|------------------|------------|--------------|
| **Exact** | ❌ | ❌ | ❌ | ⚡ Rápido | Simples |
| **Comprehensive** | ⚠️ Parcial | ❌ | ⚠️ Parcial | 🐌 Lento | Média |
| **Structure** | ❌ | ❌ | ❌ | ⚡ Rápido | Simples |
| **Layout-Preserving** | ✅ Sim | ✅ Sim | ✅ Sim | 🚀 Médio | Alta |
| **Background-Preserving** | ❌ | ✅ Sim | ⚠️ Parcial | 🚀 Médio | Média |

## 💡 Dicas de Uso

### Quando usar Layout-Preserving:
✅ Documentos com logotipos e imagens  
✅ PDFs com backgrounds complexos  
✅ Documentos com gráficos vetoriais  
✅ Quando a integridade visual é essencial  

### Quando usar Background-Preserving:
✅ Documentos com cores de fundo  
✅ PDFs com highlights e marcações  
✅ Documentos com elementos decorativos  
✅ Quando o background é mais importante  

### Quando usar métodos tradicionais:
✅ Documentos de texto simples  
✅ Quando a velocidade é prioridade  
✅ Documentos sem elementos visuais  
✅ Para substituições rápidas e simples  

## 🧪 Testes Realizados

### Teste 1: Substituição com Layout-Preserving
```bash
# Input: PDF com nome "Fernando"
# Método: layout-preserving
# Resultado: ✅ 1 substituição, gráficos preservados
```

### Teste 2: Substituição com Background-Preserving
```bash
# Input: PDF com idade "36 anos"
# Método: background-preserving
# Resultado: ✅ 1 substituição, backgrounds preservados
```

## 📊 Performance

Os novos métodos de preservação foram otimizados para:

- **Velocidade:** Processamento eficiente com detecção inteligente de elementos
- **Precisão:** Substituição exata do texto solicitado
- **Integridade:** Preservação completa de elementos visuais
- **Compatibilidade:** Funciona com PDFs de diferentes origens

## 🔧 Implementação Técnica

### Layout-Preserving Editor
- Detecta imagens usando `page.get_images(full=True)`
- Extrai desenhos vetoriais com `page.get_drawings()`
- Usa redação transparente com `fill=None`
- Preserva fontes e cores originais

### Background-Preserving Editor
- Detecta cores de fundo em elementos de desenho
- Identifica retângulos coloridos
- Usa redação com background transparente
- Mantém elementos decorativos intactos

## 🚀 Integração

Os novos métodos estão disponíveis em todas as interfaces:

- **CLI:** `--method layout-preserving` ou `--method background-preserving`
- **GUI:** Dropdown de métodos inclui as novas opções
- **TUI:** Menu de seleção inclui os novos métodos
- **Python API:** `replace_text_layout_preserving()` e `replace_text_background_preserving()`

## 📝 Exemplos de Código

### Python API
```python
from core.pdf_editor import PDFEditor

editor = PDFEditor()
editor.load("documento.pdf")

# Usar layout preserving
editor.replace_text_layout_preserving("texto antigo", "texto novo")

# Usar background preserving
editor.replace_text_background_preserving("texto antigo", "texto novo")

editor.save("output.pdf")
```

### Batch Processing
```python
operations = [
    EditOperation("texto1", "novo1"),
    EditOperation("texto2", "novo2")
]

results = editor.batch_replace(operations, method="layout-preserving")
```

## 🎯 Melhorias Futuras

- [ ] Detecção automática do melhor método
- [ ] Preservação de tabelas complexas
- [ ] Suporte para PDFs digitalizados
- [ ] Pré-visualização avançada de alterações
- [ ] Detecção inteligente de elementos

## 📞 Suporte

Para mais informações, consulte:
- [README.md](../README.md) - Documentação principal
- [docs/USUARIO.md](docs/USUARIO.md) - Guia do usuário
- [core/improved_layout_editor.py](core/improved_layout_editor.py) - Código fonte
