# PDF Editor - Documentação Completa

## 🚀 Guia de Início Rápido

### Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Para interface gráfica (opcional)
# Ubuntu/Debian:
sudo apt-get install python3-tk

# CentOS/RHEL:
sudo yum install python3-tkinter
```

### Como Usar

#### Opção 1: Menu Interativo (Recomendado)
```bash
python3 main_launcher.py
```

Escolha entre:
- **[1] GUI** - Interface Gráfica com botões e formulários
- **[2] TUI** - Interface no Terminal com navegação por teclado
- **[3] CLI** - Linha de comando para automação

#### Opção 2: Iniciar Diretamente
```bash
# Interface Gráfica
python3 main_launcher.py --gui

# Interface Terminal
python3 main_launcher.py --tui

# Linha de Comando
python3 main_launcher.py --cli
```

---

## 📁 Estrutura do Projeto

```
PDF_Editor/
├── main_launcher.py          # 🚀 Launcher Principal
├── unified_gui.py         # 🖥️ Interface Gráfica
├── unified_tui.py         # 📟 Interface Terminal
├── core/                  # 📦 Código Core
│   ├── pdf_editor.py     # Engine principal
│   ├── batch_processor.py # Processamento em lote
│   └── ...
├── interfaces/            # 🖥️ Interfaces CLI
│   ├── cli.py            # Linha de comando
│   └── cli_enhanced.py   # CLI melhorado
├── examples/              # 📚 Exemplos
│   └── create_sample_pdfs.py
├── tests/                 # 🧪 Testes
│   └── test_pdf_editor.py
├── samples/               # 📄 PDFs de exemplo
├── requirements.txt     # 📋 Dependências
└── README.md            # 📖 Documentação
```

---

## 🖥️ Interface Gráfica (GUI)

### Funcionalidades

✅ **Seleção intuitiva** de arquivos e pastas  
✅ **Modo único ou lote** - Escolha entre editar um PDF ou processar uma pasta inteira  
✅ **Gerenciamento de substituições** - Adicione múltiplas substituições de texto  
✅ **Visualização de informações** - Veja metadados do PDF antes de processar  
✅ **Log de operações** - Acompanhe o processamento em tempo real  

### Como Usar a GUI

1. **Selecione a Origem:**
   - Escolha "Arquivo único" para editar um PDF
   - Escolha "Processamento em lote" para editar vários PDFs

2. **Selecione o Destino:**
   - Escolha a pasta onde os arquivos editados serão salvos

3. **Adicione Substituições:**
   - Digite o texto a ser buscado
   - Digite o novo texto
   - Clique em "Adicionar"
   - Repita para todas as substituições necessárias

4. **Configure Opções:**
   - Escolha o método (Exact, Comprehensive, Structure)
   - Marque "Diferenciar maiúsculas/minúsculas" se necessário

5. **Processe:**
   - Clique em "Processar PDF(s)"
   - Aguarde o processamento
   - Verifique o log de operações

---

## 📟 Interface Terminal (TUI)

### Funcionalidades

✅ **Interface elegante** no terminal com abas  
✅ **Navegação por teclado** - Sem necessidade de mouse  
✅ **Mesmas funcionalidades** da GUI em modo texto  
✅ **Ideal para servidores** ou ambientes sem interface gráfica  

### Como Usar a TUI

1. **Inicie:**
   ```bash
   python3 main_launcher.py --tui
   ```

2. **Navegue pelas Abas:**
   - Use `Tab` para navegar entre abas
   - **Aba 1:** Selecione origem e destino
   - **Aba 2:** Adicione substituições
   - **Aba 3:** Configure opções e processe

3. **Atalhos do Teclado:**
   - `Tab` - Próximo elemento
   - `Shift+Tab` - Elemento anterior
   - `Enter` - Confirmar/Ativar
   - `Esc` - Cancelar/Voltar

---

## ⌨️ Interface de Linha de Comando (CLI)

### Comandos Principais

```bash
# Buscar texto em PDF
python3 -m interfaces.cli search arquivo.pdf "texto a buscar"

# Substituir texto
python3 -m interfaces.cli replace arquivo.pdf "texto antigo" "texto novo" saida.pdf

# Processar em lote
python3 -m interfaces.cli batch arquivo.pdf substituicoes.json saida.pdf

# Ver informações
python3 -m interfaces.cli info arquivo.pdf
```

### Exemplos Práticos

```bash
# Exemplo 1: Substituir nome em atestado
python3 -m interfaces.cli replace atestado.pdf \
  "João da Silva" "Maria Oliveira" atestado_editado.pdf

# Exemplo 2: Atualizar data em múltiplos arquivos
python3 -m interfaces.cli batch contratos.pdf substituicoes.json

# Exemplo 3: Buscar com diferenciação de maiúsculas
python3 -m interfaces.cli search documento.pdf "Empresa" --case-sensitive
```

---

## 🔧 Métodos de Edição

### Exact (Recomendado)
- **Uso:** Substituições precisas com preservação de posição
- **Vantagem:** Mantém layout original
- **Quando usar:** Edições simples de texto

### Comprehensive
- **Uso:** Edições complexas com múltiplos elementos
- **Vantagem:** Separa elementos gráficos e texto
- **Quando usar:** Documentos com layouts complexos

### Structure
- **Uso:** Reescrita completa de parágrafos
- **Vantagem:** Fonte homogênea em todo o texto
- **Quando usar:** Quando a consistência visual é prioridade

---

## 📋 Formato de Configuração JSON

Para processamento em lote, crie um arquivo JSON:

```json
[
  {
    "search": "Texto Antigo",
    "replace": "Texto Novo",
    "case_sensitive": false
  },
  {
    "search": "2023",
    "replace": "2024",
    "case_sensitive": false
  }
]
```

---

## 🎯 Casos de Uso

### 1. Atualização de Atestados
```bash
python3 -m interfaces.cli replace atestado.pdf \
  "Marcelo de Freitas Ferreira" "Fernando Augusto Vargas Rodrigues Paes" \
  atestado_novo.pdf
```

### 2. Atualização em Lote de Contratos
- Selecione pasta com contratos
- Configure substituições (nome da empresa, datas, valores)
- Processe todos de uma vez

### 3. Reescrita Homogênea
- Use método "Structure" para fonte consistente
- Ideal quando a aparência uniforme é essencial

---

## ❓ Solução de Problemas

### Erro: "No module named 'tkinter'"
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL/Fedora
sudo yum install python3-tkinter
```

### Erro: "Font not available"
- Use método "Structure" para substituição homogênea
- O sistema usará fonte padrão consistente

### PDF não processa
1. Verifique se o PDF não está protegido
2. Confirme que o arquivo não está corrompido
3. Use a opção de visualização para verificar informações

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação completa em docs/
2. Consulte os exemplos em examples/
3. Execute testes com samples/sample_*.pdf

---

## 🎓 Dicas Profissionais

✅ **Sempre faça backup** antes de processar PDFs importantes  
✅ **Teste primeiro** com cópias de trabalho  
✅ **Use a visualização** para confirmar o conteúdo antes de processar  
✅ **Prefira modo lote** para processar múltiplos arquivos  
✅ **Escolha método "Structure"** quando a consistência visual for prioridade  

---

## 🚀 Atualizações Futuras

- [ ] Suporte a OCR para PDFs escaneados
- [ ] Editor visual WYSIWYG
- [ ] Plugin para editores de texto
- [ ] Suporte a assinaturas digitais

---

**PDF Editor v1.0.0** - Edição profissional de texto em PDFs
