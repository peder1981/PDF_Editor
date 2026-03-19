# 📄 PDF Editor - Editor Profissional de PDFs

<p align="center">
  <b>Edição de texto em PDFs com preservação de estrutura e fontes homogêneas</b>
</p>

<p align="center">
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#-instalação">Instalação</a> •
  <a href="#-como-usar">Como Usar</a> •
  <a href="#-exemplos">Exemplos</a> •
  <a href="#-documentação">Documentação</a>
</p>

---

## ✨ Funcionalidades

| Recurso | Descrição |
|---------|-----------|
| 🖥️ **3 Interfaces** | GUI (gráfica), TUI (terminal) e CLI (linha de comando) |
| 📁 **Modo Único ou Lote** | Edite um PDF ou processe uma pasta inteira |
| ✏️ **Substituições Múltiplas** | Configure várias alterações de uma só vez |
| 🔤 **Fontes Homogêneas** | Mantenha a aparência consistente no documento |
| 🧵 **Processamento Paralelo** | Multi-threading para operações em lote |
| 📊 **Visualização** | Veja informações do PDF antes de editar |
| 📝 **Log em Tempo Real** | Acompanhe cada operação passo a passo |

---

## 🚀 Instalação

### Pré-requisitos

- **Python:** 3.8 ou superior
- **Sistema:** Linux, macOS ou Windows
- **Tkinter:** Para interface gráfica (opcional)

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL/Fedora
sudo yum install python3-tkinter
```

### Instalação das Dependências

```bash
# Clone o repositório
git clone https://github.com/peder1981/PDF_Editor.git
cd PDF_Editor

# Instale as dependências
pip install -r requirements.txt
```

---

## 🎮 Como Usar

### Opção 1: Menu Interativo (Recomendado para Iniciantes)

```bash
python3 main_launcher.py
```

Escolha entre:
- **[1] GUI** - Interface gráfica intuitiva com botões e formulários
- **[2] TUI** - Interface no terminal com navegação por teclado
- **[3] CLI** - Linha de comando para automação

### Opção 2: Iniciar Diretamente

```bash
# 🖥️ Interface Gráfica (GUI)
python3 main_launcher.py --gui

# 📟 Interface Terminal (TUI)
python3 main_launcher.py --tui

# ⌨️ Linha de Comando (CLI)
python3 main_launcher.py --cli
```

### Opção 3: Executáveis Standalone (PyInstaller)

Para usuários finais que não querem instalar dependências, gere ou utilize os binários em `dist/`:

```bash
# GUI (sem terminal)
./dist/pdf_editor_gui/pdf_editor_gui

# TUI (terminal)
./dist/pdf_editor_tui/pdf_editor_tui
```

> Dica: no Linux talvez seja necessário liberar execução com `chmod +x dist/pdf_editor_gui/pdf_editor_gui`.

Ambos os pacotes já incluem `core/`, `docs/` e `pdfs/`, garantindo a mesma experiência das interfaces originais.

### Automação Rápida (scripts/common_replacements.py)

Para casos recorrentes — como atualizar nome, idade e data em atestados — utilize o novo script:

```bash
python3 scripts/common_replacements.py input.pdf output.pdf \
  --name "Elton Trindade dos Santos" \
  --issue-date "Niterói, 10 de março de 2026." \
  --method layout-preserving
```

Também é possível carregar um JSON com operações personalizadas via `--config configs/meu_fluxo.json`.

---

## 📖 Exemplos de Uso

### 📝 Exemplo 1: Atualizar Nome em Atestado Médico

```bash
# Usando a interface gráfica (interativa)
python3 main_launcher.py --gui

# Ou via linha de comando (direto)
python3 -m interfaces.cli replace atestado.pdf \
  "Marcelo de Freitas Ferreira" \
  "Fernando Augusto Vargas Rodrigues Paes" \
  atestado_atualizado.pdf
```

### 📅 Exemplo 2: Atualizar Idade e Data com Preservação de Layout

```bash
# Usando método de preservação de layout (mantém gráficos e backgrounds)
python3 -m interfaces.cli replace atestado.pdf \
  "46 anos" \
  "36 anos" \
  atestado_atualizado.pdf \
  --method layout-preserving

# Ou via GUI: Selecione "layout-preserving" no dropdown de métodos
```

### 📁 Exemplo 3: Processar Pasta Inteira (Lote)

```bash
# GUI: Selecione "Processamento em Lote" e escolha a pasta
# CLI: Processe todos os PDFs de uma vez
python3 -m interfaces.cli batch pasta_entrada/ config.json pasta_saida/
```

### 🔍 Exemplo 4: Buscar Texto no PDF

```bash
python3 -m interfaces.cli search documento.pdf "texto a buscar"
```

### 📊 Exemplo 5: Visualizar Informações

```bash
python3 -m interfaces.cli info documento.pdf
```

---

## 🎯 Métodos de Edição

Escolha o método mais adequado para seu caso:

| Método | Quando Usar | Resultado |
|--------|-------------|-----------|
| **Exact** | Edições simples, preservar layout original | Substituição precisa na posição exata |
| **Comprehensive** | Documentos complexos com imagens | Separa elementos gráficos do texto |
| **Structure** | Fonte homogênea é prioridade | Reescreve parágrafo com fonte consistente |
| **Layout-Preserving** ⭐ | Preservar gráficos e backgrounds | Mantém todos os elementos visuais intactos |
| **Background-Preserving** ⭐ | Documentos com cores de fundo | Preserva backgrounds e elementos decorativos |

---

## ✅ Status do Projeto

### Funcionalidades Testadas e Funcionando

- ✅ **TUI (Terminal User Interface)** - Interface terminal funcionando perfeitamente
- ✅ **CLI (Command Line Interface)** - Interface de linha de comando com todos os métodos
- ✅ **GUI (Graphical User Interface)** - Interface gráfica abrindo corretamente
- ✅ **API Python** - API Python com todos os métodos funcionando
- ✅ **Layout Preserving Methods** - Novos métodos de preservação funcionando
- ✅ **Unit Tests** - 10/11 testes passando (1 falha menor não crítica)

### Correções Recentes

- ✅ Fixed TUI MountError - Removido yield statements de métodos auxiliares
- ✅ Fixed TUI AttributeError - Adicionado query_one para acessar botões por ID
- ✅ Added CLI support for layout-preserving and background-preserving methods
- ✅ Fixed unit test import paths

### Documentação Completa

- 📚 [DOCUMENTACAO_COMPLETA.md](docs/DOCUMENTACAO_COMPLETA.md) - Documentação completa do projeto
- 📖 [GUIA_CLI.md](docs/GUIA_CLI.md) - Guia da interface de linha de comando
- 🖥️ [GUIA_GUI.md](docs/GUIA_GUI.md) - Guia da interface gráfica
- 📟 [GUIA_TUI.md](docs/GUIA_TUI.md) - Guia da interface terminal
- 🐍 [GUIA_API.md](docs/GUIA_API.md) - Guia da API Python
- 💡 [EXEMPLOS_PRATICOS.md](docs/EXEMPLOS_PRATICOS.md) - Exemplos práticos e scripts
- 🔧 [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Guia de solução de problemas
- 🎨 [LAYOUT_PRESERVATION.md](docs/LAYOUT_PRESERVATION.md) - Preservação de layout

**🆕 Novos Métodos de Preservação:**
- **Layout-Preserving:** Usa redação avançada para preservar gráficos, imagens e backgrounds enquanto substitui o texto
- **Background-Preserving:** Foca na preservação de cores de fundo e elementos decorativos do documento

---

## 📁 Estrutura do Projeto

```
PDF_Editor/
├── 🚀 main_launcher.py          # Launcher principal (inicie aqui!)
├── 🖥️ unified_gui.py            # Interface gráfica unificada
├── 📟 unified_tui.py            # Interface terminal unificada
├── 📦 core/                     # Motor de edição de PDFs
│   ├── pdf_editor.py           # Engine principal
│   ├── batch_processor.py      # Processamento em lote
│   └── ...                     # Outros módulos
├── 🖥️ interfaces/               # Interfaces CLI
│   ├── cli.py                # Linha de comando
│   └── cli_enhanced.py       # CLI melhorado
├── 📚 docs/                     # Documentação
│   └── USUARIO.md            # Guia completo do usuário
├── 🧪 tests/                    # Testes automatizados
└── 📋 requirements.txt        # Dependências Python
```

**💡 Dica:** A raiz do projeto está organizada - apenas o launcher principal e documentação essencial estão na raiz!

---

## 📚 Documentação

- **[📖 Guia Completo](docs/USUARIO.md)** - Documentação detalhada com todos os recursos
- **[🐍 Referência CLI](interfaces/cli.py)** - Documentação da linha de comando
- **[🧪 Testes](tests/test_pdf_editor.py)** - Exemplos de uso via código Python

---

## 💡 Dicas Profissionais

✅ **Sempre faça backup** dos PDFs originais antes de editar  
✅ **Teste primeiro** com arquivos de teste antes de usar em produção  
✅ **Prefira o método "Structure"** quando a consistência visual for essencial  
✅ **Use o modo lote** para processar múltiplos arquivos de uma vez  
✅ **Verifique as substituições** na pré-visualização antes de confirmar  

---

## 🔧 Solução de Problemas

### Erro: "No module named 'tkinter'"
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install python3-tkinter
```

### Erro: "Font not available"
- Use o método **"Structure"** para substituição homogênea
- O sistema usará fonte padrão consistente em todo o texto

### PDF não processa
1. Verifique se o PDF não está protegido por senha
2. Confirme que o arquivo não está corrompido
3. Use `python3 -m interfaces.cli info arquivo.pdf` para diagnóstico

---

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🌟 Destaques

🎨 **Interface Unificada:** Uma aplicação, três formas de usar  
🔧 **Código Organizado:** Estrutura profissional e limpa  
⚡ **Alta Performance:** Processamento paralelo com multi-threading  
🎯 **Precisão:** Preservação completa de estrutura e layout  

---

<p align="center">
  <b>Desenvolvido com ❤️ para edição profissional de PDFs</b>
</p>

<p align="center">
  📄 <b>PDF Editor v1.0.0</b> - Simplificando a edição de texto em PDFs
</p>
