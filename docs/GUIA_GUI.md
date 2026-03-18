# 🖥️ Guia da Interface Gráfica (GUI)

## 📋 Índice

1. [Introdução](#introdução)
2. [Instalação](#instalação)
3. [Como Usar](#como-usar)
4. [Funcionalidades](#funcionalidades)
5. [Exemplos Práticos](#exemplos-práticos)
6. [Dicas e Truques](#dicas-e-truques)

---

## 🚀 Introdução

A Interface Gráfica (GUI) do PDF Editor oferece uma experiência intuitiva e visual para editar PDFs, ideal para usuários que preferem interfaces gráficas com mouse e clique.

### **Vantagens da GUI**

✅ **Intuitiva** - Interface fácil de usar com mouse  
✅ **Visual** - Pré-visualização de alterações  
✅ **Interativa** - Feedback em tempo real  
✅ **Amigável** - Ideal para usuários iniciantes  
✅ **Completa** - Todas as funcionalidades disponíveis  

---

## 📦 Instalação

### **Pré-requisitos**

```bash
# Python 3.8 ou superior
python3 --version

# Tkinter (para interface gráfica)
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL/Fedora
sudo yum install python3-tkinter

# macOS (já incluído)
# Windows (já incluído)

# Instalar dependências
pip install -r requirements.txt
```

### **Verificar Instalação**

```bash
# Testar GUI
python3 main_launcher.py --gui

# Deve abrir uma janela gráfica
```

---

## 🎯 Como Usar

### **1. Iniciar a GUI**

```bash
# Opção 1: Via launcher com menu
python3 main_launcher.py

# Selecione [1] GUI

# Opção 2: Diretamente
python3 main_launcher.py --gui
```

### **2. Interface Principal**

A interface é dividida em seções:

#### **📁 Seção de Origem e Destino**
- **Modo de Operação:** Arquivo Único ou Processamento em Lote
- **Origem:** Arquivo PDF ou pasta de entrada
- **Destino:** Diretório de saída

#### **➕ Seção de Substituições**
- **Campo "Texto a Buscar":** Digite o texto a substituir
- **Campo "Texto de Substituição":** Digite o novo texto
- **Botão "➕ Adicionar":** Adiciona a substituição à lista
- **Lista de Substituições:** Mostra todas as substituições configuradas
- **Botão "🗑️ Remover selecionado":** Remove substituição selecionada
- **Botão "🗑️ Limpar todos":** Remove todas as substituições

#### **⚙️ Seção de Opções**
- **Método:** Dropdown com métodos de edição
  - **exact** - Substituição precisa
  - **comprehensive** - Separa elementos gráficos
  - **structure** - Fonte homogênea
  - **smart** - Seleção inteligente
  - **heuristic** - Substituição heurística
  - **integral** - Substituição integral
  - **template** - Cria template limpo
  - **layout-preserving** ⭐ - Preserva gráficos e backgrounds
  - **background-preserving** ⭐ - Preserva backgrounds coloridos
- **Diferenciar maiúsculas/minúsculas:** Checkbox para busca sensível

#### **🚀 Botões de Ação**
- **🚀 Processar PDF(s):** Inicia o processamento
- **📊 Visualizar PDF:** Mostra informações do documento
- **❌ Sair:** Fecha a aplicação

#### **📋 Área de Log**
- Mostra o progresso e resultados das operações
- Log em tempo real do processamento

#### **📊 Barra de Status**
- Mostra o status atual da aplicação
- Informações sobre o processamento

---

## 📖 Funcionalidades

### **1. Seleção de Origem**

#### **Arquivo Único**
1. Clique em "📄 Arquivo Único"
2. Clique em "🔍 Selecionar" ao lado de Origem
3. Escolha um arquivo PDF
4. O caminho será exibido

#### **Processamento em Lote**
1. Clique em "📁 Processamento em Lote"
2. Clique em "🔍 Selecionar" ao lado de Origem
3. Escolha uma pasta contendo PDFs
4. O caminho da pasta será exibido

### **2. Seleção de Destino**

1. Clique em "🔍 Selecionar" ao lado de Destino
2. Escolha o diretório de saída
3. O caminho será exibido

**Nota:** Para processamento em lote, todos os PDFs processados serão salvos neste diretório.

### **3. Adicionar Substituições**

#### **Substituição Simples**
1. Digite o texto a buscar em "Texto a Buscar"
2. Digite o texto de substituição em "Texto de Substituição"
3. Clique em "➕ Adicionar"
4. A substituição aparecerá na lista

#### **Múltiplas Substituições**
1. Adicione a primeira substituição
2. Repita o processo para cada substituição adicional
3. Todas serão processadas na ordem da lista

#### **Remover Substituições**
- **Remover selecionada:** Selecione uma substituição na lista e clique em "🗑️ Remover selecionado"
- **Limpar todas:** Clique em "🗑️ Limpar todos" para remover todas

### **4. Configurar Opções**

#### **Selecionar Método**
1. Clique no dropdown "Método"
2. Selecione o método desejado:
   - **exact** - Para substituições simples
   - **layout-preserving** - Para documentos com imagens/gráficos
   - **background-preserving** - Para documentos com backgrounds coloridos
   - **structure** - Para consistência visual

#### **Case-Sensitive**
1. Marque "Diferenciar maiúsculas/minúsculas" se necessário
2. Isso fará a busca considerar maiúsculas e minúsculas

### **5. Processar PDFs**

#### **Processar Arquivo Único**
1. Configure todas as substituições
2. Selecione o método desejado
3. Clique em "🚀 Processar PDF(s)"
4. Acompanhe o progresso no log
5. O PDF processado será salvo no diretório de destino

#### **Processar em Lote**
1. Configure as substituições
2. Selecione o método desejado
3. Clique em "🚀 Processar PDF(s)"
4. Todos os PDFs na pasta de origem serão processados
5. Acompanhe o progresso no log
6. Os PDFs processados serão salvos no diretório de destino

### **6. Visualizar Informações**

1. Selecione um arquivo de origem
2. Clique em "📊 Visualizar PDF"
3. As informações do documento serão exibidas no log:
   - Número de páginas
   - Instâncias de texto
   - Tamanho do arquivo
   - Metadados

---

## 💡 Exemplos Práticos

### **Exemplo 1: Atualizar Atestado Médico**

#### **Passo a Passo**

1. **Iniciar GUI**
   ```bash
   python3 main_launcher.py --gui
   ```

2. **Selecionar Origem**
   - Clique em "📄 Arquivo Único"
   - Clique em "🔍 Selecionar" (Origem)
   - Escolha `atestado.pdf`

3. **Selecionar Destino**
   - Clique em "🔍 Selecionar" (Destino)
   - Escolha o diretório de saída

4. **Adicionar Substituição 1**
   - Texto a Buscar: `Marcelo de Freitas Ferreira`
   - Texto de Substituição: `Fernando Augusto Vargas Rodrigues Paes`
   - Clique em "➕ Adicionar"

5. **Adicionar Substituição 2**
   - Texto a Buscar: `46 anos`
   - Texto de Substituição: `36 anos`
   - Clique em "➕ Adicionar"

6. **Adicionar Substituição 3**
   - Texto a Buscar: `19 de agosto de 1979`
   - Texto de Substituição: `29 de maio de 1989`
   - Clique em "➕ Adicionar"

7. **Configurar Método**
   - Selecione `layout-preserving` no dropdown
   - Isso preservará gráficos e backgrounds

8. **Processar**
   - Clique em "🚀 Processar PDF(s)"
   - Acompanhe o progresso no log

9. **Resultado**
   - O PDF processado será salvo no diretório de destino
   - Verifique no log se todas as substituições foram aplicadas

### **Exemplo 2: Processar Contratos em Lote**

#### **Passo a Passo**

1. **Iniciar GUI**
   ```bash
   python3 main_launcher.py --gui
   ```

2. **Selecionar Modo**
   - Clique em "📁 Processamento em Lote"

3. **Selecionar Origem**
   - Clique em "🔍 Selecionar" (Origem)
   - Escolha a pasta `contratos/`

4. **Selecionar Destino**
   - Clique em "🔍 Selecionar" (Destino)
   - Escolha a pasta `contratos_atualizados/`

5. **Adicionar Substituição 1**
   - Texto a Buscar: `ACME Corporation`
   - Texto de Substituição: `TechStart Inc.`
   - Clique em "➕ Adicionar"

6. **Adicionar Substituição 2**
   - Texto a Buscar: `2023`
   - Texto de Substituição: `2024`
   - Clique em "➕ Adicionar"

7. **Adicionar Substituição 3**
   - Texto a Buscar: `João Silva`
   - Texto de Substituição: `Maria Santos`
   - Clique em "➕ Adicionar"

8. **Configurar Método**
   - Selecione `layout-preserving` no dropdown

9. **Processar**
   - Clique em "🚀 Processar PDF(s)"
   - Acompanhe o progresso no log
   - Todos os contratos serão processados

10. **Resultado**
    - Todos os contratos processados estarão em `contratos_atualizados/`
    - Verifique no log se todas as substituições foram aplicadas

### **Exemplo 3: Atualizar Formulário com Background**

#### **Passo a Passo**

1. **Iniciar GUI**
   ```bash
   python3 main_launcher.py --gui
   ```

2. **Selecionar Origem**
   - Clique em "📄 Arquivo Único"
   - Clique em "🔍 Selecionar" (Origem)
   - Escolha `formulario.pdf`

3. **Selecionar Destino**
   - Clique em "🔍 Selecionar" (Destino)
   - Escolha o diretório de saída

4. **Adicionar Substituição 1**
   - Texto a Buscar: `Nome: João`
   - Texto de Substituição: `Nome: Maria`
   - Clique em "➕ Adicionar"

5. **Adicionar Substituição 2**
   - Texto a Buscar: `Idade: 30`
   - Texto de Substituição: `Idade: 25`
   - Clique em "➕ Adicionar"

6. **Configurar Método**
   - Selecione `background-preserving` no dropdown
   - Isso preservará cores de fundo do formulário

7. **Processar**
   - Clique em "🚀 Processar PDF(s)"
   - Acompanhe o progresso no log

8. **Resultado**
   - O formulário processado terá os dados atualizados
   - As cores de fundo serão preservadas

---

## 🎨 Dicas e Truques

### **1. Usar Preview Antes de Processar**

Antes de processar, visualize as informações do documento:

1. Selecione o arquivo de origem
2. Clique em "📊 Visualizar PDF"
3. Verifique se o texto a ser substituído existe
4. Depois prossiga com o processamento

### **2. Escolher o Método Certo**

| Método | Quando Usar |
|--------|-------------|
| **exact** | Documentos simples, sem elementos visuais |
| **layout-preserving** ⭐ | Documentos com imagens, gráficos, backgrounds |
| **background-preserving** ⭐ | Documentos com cores de fundo, highlights |
| **structure** | Quando a consistência visual é importante |
| **comprehensive** | Documentos complexos com múltiplos elementos |

### **3. Ordem das Substituições**

A ordem das substituições na lista é importante:

```python
# Ordem correta
1. "João Silva" → "Maria Santos"
2. "Silva" → "Santos"  # Isso funcionará

# Ordem incorreta
1. "Silva" → "Santos"
2. "João Silva" → "Maria Santos"  # Isso não funcionará (João Silva já foi alterado)
```

### **4. Usar Case-Sensitive com Cuidado**

Marque "Diferenciar maiúsculas/minúsculas" apenas quando necessário:

- ✅ Use quando o texto tem variações de maiúsculas/minúsculas específicas
- ❌ Não use para substituições genéricas

### **5. Backup Automático**

Antes de processar documentos importantes:

1. Faça uma cópia do original
2. Processe a cópia
3. Verifique o resultado
4. Se estiver correto, use o original

### **6. Processamento em Lote Eficiente**

Para processamento em lote:

- Organize PDFs em pastas por tipo
- Use configurações consistentes
- Monitore o log para erros
- Verifique os resultados

### **7. Validação de Resultados**

Após processar:

1. Abra o PDF processado
2. Verifique se as substituições foram aplicadas
3. Confirme que elementos visuais foram preservados
4. Compare com o original se necessário

### **8. Troubleshooting**

#### **Substituição Não Funciona**

- Verifique se o texto a buscar está correto
- Tente usar case-sensitive
- Use preview para verificar se o texto existe

#### **Elementos Visuais Não Preservados**

- Use `layout-preserving` em vez de `exact`
- Verifique se o PDF tem elementos visuais
- Teste com `background-preserving`

#### **Erro ao Processar**

- Verifique se o arquivo PDF não está corrompido
- Confirme que o arquivo não está protegido por senha
- Tente usar um método diferente

---

## 📚 Recursos Adicionais

- [README.md](../README.md) - Visão geral do projeto
- [docs/DOCUMENTACAO_COMPLETA.md](DOCUMENTACAO_COMPLETA.md) - Documentação completa
- [docs/LAYOUT_PRESERVATION.md](LAYOUT_PRESERVATION.md) - Preservação de layout
- [docs/GUIA_CLI.md](GUIA_CLI.md) - Guia da interface de linha de comando
- [docs/GUIA_TUI.md](GUIA_TUI.md) - Guia da interface terminal
- [docs/GUIA_API.md](GUIA_API.md) - Guia da API Python
