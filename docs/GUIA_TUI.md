# 📟 Guia da Interface Terminal (TUI)

## 📋 Índice

1. [Introdução](#introdução)
2. [Instalação](#instalação)
3. [Como Usar](#como-usar)
4. [Funcionalidades](#funcionalidades)
5. [Exemplos Práticos](#exemplos-práticos)
6. [Dicas e Truques](#dicas-e-truques)

---

## 🚀 Introdução

A Interface Terminal (TUI) do PDF Editor oferece uma experiência interativa no terminal, ideal para usuários que preferem navegação por teclado e ambientes de linha de comando.

### **Vantagens da TUI**

✅ **Interativa** - Navegação por teclado intuitiva  
✅ **Visual** - Interface colorida e organizada  
✅ **Eficiente** - Rápida e responsiva  
✅ **Profissional** - Ideal para ambientes de servidor  
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

### **Verificar Instalação**

```bash
# Testar TUI
python3 main_launcher.py --tui

# Deve abrir uma interface terminal interativa
```

---

## 🎯 Como Usar

### **1. Iniciar a TUI**

```bash
# Opção 1: Via launcher com menu
python3 main_launcher.py

# Selecione [2] TUI

# Opção 2: Diretamente
python3 main_launcher.py --tui
```

### **2. Interface Principal**

A interface é dividida em seções:

#### **🎯 Modo de Operação**
- **[1] Arquivo Único** - Processar um PDF específico
- **[2] Processamento em Lote** - Processar múltiplos PDFs

#### **📁 Origem e Destino**
- **Origem:** Arquivo PDF ou pasta de entrada
- **Destino:** Diretório de saída

#### **➕ Adicionar Substituição**
- **Campo "Texto a Buscar":** Digite o texto a substituir
- **Campo "Texto de Substituição":** Digite o novo texto
- **Botão "➕ Adicionar":** Adiciona a substituição

#### **📋 Lista de Substituições**
- Mostra todas as substituições configuradas
- Navegação com setas do teclado

#### **⚙️ Opções**
- **Método:** Menu de seleção de métodos
  - **Exato (Exact)**
  - **Compreensivo**
  - **Estrutura**
  - **Inteligente (Smart)**
  - **Heurístico**
  - **Integral**
  - **Template**
  - **Preservar Layout** ⭐
  - **Preservar Background** ⭐
- **Case-Sensitive:** Checkbox para busca sensível

#### **🚀 Botões de Ação**
- **📊 Visualizar Informações** - Mostra informações do documento
- **🚀 Processar** - Inicia o processamento

#### **📋 Área de Log**
- Mostra o progresso e resultados das operações
- Log em tempo real com cores

---

## 📖 Funcionalidades

### **1. Navegação**

#### **Teclas de Navegação**

| Tecla | Ação |
|-------|------|
| `↑` `↓` | Navegar entre opções |
| `Enter` | Selecionar opção |
| `Tab` | Alternar entre campos |
| `Esc` | Voltar/Sair |
| `Space` | Marcar/desmarcar checkbox |

### **2. Selecionar Modo de Operação**

#### **Arquivo Único**
1. Pressione `1` ou use as setas para selecionar "📄 Arquivo Único"
2. Pressione `Enter`

#### **Processamento em Lote**
1. Pressione `2` ou use as setas para selecionar "📁 Processamento em Lote"
2. Pressione `Enter`

### **3. Selecionar Origem**

#### **Arquivo Único**
1. Use as setas para navegar até "🔍 Selecionar" (Origem)
2. Pressione `Enter`
3. Navegue até o arquivo PDF desejado
4. Pressione `Enter` para selecionar

#### **Processamento em Lote**
1. Use as setas para navegar até "🔍 Selecionar" (Origem)
2. Pressione `Enter`
3. Navegue até a pasta desejada
4. Pressione `Enter` para selecionar

### **4. Selecionar Destino**

1. Use as setas para navegar até "🔍 Selecionar" (Destino)
2. Pressione `Enter`
3. Navegue até o diretório de saída desejado
4. Pressione `Enter` para selecionar

### **5. Adicionar Substituições**

#### **Substituição Simples**
1. Use `Tab` para navegar até "Texto a Buscar"
2. Digite o texto a buscar
3. Use `Tab` para ir para "Texto de Substituição"
4. Digite o texto de substituição
5. Use `Tab` para ir até "➕ Adicionar"
6. Pressione `Enter`

#### **Múltiplas Substituições**
1. Adicione a primeira substituição
2. Repita o processo para cada substituição adicional
3. Todas serão processadas na ordem da lista

### **6. Configurar Opções**

#### **Selecionar Método**
1. Use `Tab` para navegar até o menu "Método"
2. Use as setas para selecionar o método desejado:
   - **Exato (Exact)** - Para substituições simples
   - **Preservar Layout** - Para documentos com imagens/gráficos
   - **Preservar Background** - Para documentos com backgrounds coloridos
   - **Estrutura** - Para consistência visual

#### **Case-Sensitive**
1. Use `Tab` para navegar até "Diferenciar maiúsculas/minúsculas"
2. Pressione `Space` para marcar/desmarcar

### **7. Processar PDFs**

#### **Processar Arquivo Único**
1. Configure todas as substituições
2. Selecione o método desejado
3. Use as setas para navegar até "🚀 Processar"
4. Pressione `Enter`
5. Acompanhe o progresso no log

#### **Processar em Lote**
1. Configure as substituições
2. Selecione o método desejado
3. Use as setas para navegar até "🚀 Processar"
4. Pressione `Enter`
5. Acompanhe o progresso no log

### **8. Visualizar Informações**

1. Selecione um arquivo de origem
2. Use as setas para navegar até "📊 Visualizar Informações"
3. Pressione `Enter`
4. As informações do documento serão exibidas no log

---

## 💡 Exemplos Práticos

### **Exemplo 1: Atualizar Atestado Médico**

#### **Passo a Passo**

1. **Iniciar TUI**
   ```bash
   python3 main_launcher.py --tui
   ```

2. **Selecionar Modo**
   - Pressione `1` para "📄 Arquivo Único"
   - Pressione `Enter`

3. **Selecionar Origem**
   - Use as setas para navegar até "🔍 Selecionar" (Origem)
   - Pressione `Enter`
   - Navegue até `atestado.pdf`
   - Pressione `Enter`

4. **Selecionar Destino**
   - Use as setas para navegar até "🔍 Selecionar" (Destino)
   - Pressione `Enter`
   - Navegue até o diretório de saída
   - Pressione `Enter`

5. **Adicionar Substituição 1**
   - Use `Tab` para ir para "Texto a Buscar"
   - Digite: `Marcelo de Freitas Ferreira`
   - Use `Tab` para ir para "Texto de Substituição"
   - Digite: `Fernando Augusto Vargas Rodrigues Paes`
   - Use `Tab` para ir até "➕ Adicionar"
   - Pressione `Enter`

6. **Adicionar Substituição 2**
   - Use `Tab` para ir para "Texto a Buscar"
   - Digite: `46 anos`
   - Use `Tab` para ir para "Texto de Substituição"
   - Digite: `36 anos`
   - Use `Tab` para ir até "➕ Adicionar"
   - Pressione `Enter`

7. **Adicionar Substituição 3**
   - Use `Tab` para ir para "Texto a Buscar"
   - Digite: `19 de agosto de 1979`
   - Use `Tab` para ir para "Texto de Substituição"
   - Digite: `29 de maio de 1989`
   - Use `Tab` para ir até "➕ Adicionar"
   - Pressione `Enter`

8. **Configurar Método**
   - Use `Tab` para ir até o menu "Método"
   - Use as setas para selecionar "Preservar Layout"
   - Pressione `Enter`

9. **Processar**
   - Use as setas para navegar até "🚀 Processar"
   - Pressione `Enter`
   - Acompanhe o progresso no log

10. **Resultado**
    - O PDF processado será salvo no diretório de destino
    - Verifique no log se todas as substituições foram aplicadas

### **Exemplo 2: Processar Contratos em Lote**

#### **Passo a Passo**

1. **Iniciar TUI**
   ```bash
   python3 main_launcher.py --tui
   ```

2. **Selecionar Modo**
   - Pressione `2` para "📁 Processamento em Lote"
   - Pressione `Enter`

3. **Selecionar Origem**
   - Use as setas para navegar até "🔍 Selecionar" (Origem)
   - Pressione `Enter`
   - Navegue até a pasta `contratos/`
   - Pressione `Enter`

4. **Selecionar Destino**
   - Use as setas para navegar até "🔍 Selecionar" (Destino)
   - Pressione `Enter`
   - Navegue até a pasta `contratos_atualizados/`
   - Pressione `Enter`

5. **Adicionar Substituição 1**
   - Use `Tab` para ir para "Texto a Buscar"
   - Digite: `ACME Corporation`
   - Use `Tab` para ir para "Texto de Substituição"
   - Digite: `TechStart Inc.`
   - Use `Tab` para ir até "➕ Adicionar"
   - Pressione `Enter`

6. **Adicionar Substituição 2**
   - Use `Tab` para ir para "Texto a Buscar"
   - Digite: `2023`
   - Use `Tab` para ir para "Texto de Substituição"
   - Digite: `2024`
   - Use `Tab` para ir até "➕ Adicionar"
   - Pressione `Enter`

7. **Adicionar Substituição 3**
   - Use `Tab` para ir para "Texto a Buscar"
   - Digite: `João Silva`
   - Use `Tab` para ir para "Texto de Substituição"
   - Digite: `Maria Santos`
   - Use `Tab` para ir até "➕ Adicionar"
   - Pressione `Enter`

8. **Configurar Método**
   - Use `Tab` para ir até o menu "Método"
   - Use as setas para selecionar "Preservar Layout"
   - Pressione `Enter`

9. **Processar**
   - Use as setas para navegar até "🚀 Processar"
   - Pressione `Enter`
   - Acompanhe o progresso no log

10. **Resultado**
    - Todos os contratos processados estarão em `contratos_atualizados/`
    - Verifique no log se todas as substituições foram aplicadas

### **Exemplo 3: Atualizar Formulário com Background**

#### **Passo a Passo**

1. **Iniciar TUI**
   ```bash
   python3 main_launcher.py --tui
   ```

2. **Selecionar Modo**
   - Pressione `1` para "📄 Arquivo Único"
   - Pressione `Enter`

3. **Selecionar Origem**
   - Use as setas para navegar até "🔍 Selecionar" (Origem)
   - Pressione `Enter`
   - Navegue até `formulario.pdf`
   - Pressione `Enter`

4. **Selecionar Destino**
   - Use as setas para navegar até "🔍 Selecionar" (Destino)
   - Pressione `Enter`
   - Navegue até o diretório de saída
   - Pressione `Enter`

5. **Adicionar Substituição 1**
   - Use `Tab` para ir para "Texto a Buscar"
   - Digite: `Nome: João`
   - Use `Tab` para ir para "Texto de Substituição"
   - Digite: `Nome: Maria`
   - Use `Tab` para ir até "➕ Adicionar"
   - Pressione `Enter`

6. **Adicionar Substituição 2**
   - Use `Tab` para ir para "Texto a Buscar"
   - Digite: `Idade: 30`
   - Use `Tab` para ir para "Texto de Substituição"
   - Digite: `Idade: 25`
   - Use `Tab` para ir até "➕ Adicionar"
   - Pressione `Enter`

7. **Configurar Método**
   - Use `Tab` para ir até o menu "Método"
   - Use as setas para selecionar "Preservar Background"
   - Pressione `Enter`

8. **Processar**
   - Use as setas para navegar até "🚀 Processar"
   - Pressione `Enter`
   - Acompanhe o progresso no log

9. **Resultado**
    - O formulário processado terá os dados atualizados
    - As cores de fundo serão preservadas

---

## 🎨 Dicas e Truques

### **1. Navegação Eficiente**

#### **Atalhos de Teclado**

| Atalho | Ação |
|--------|------|
| `q` | Sair da aplicação |
| `Ctrl+C` | Cancelar operação atual |
| `Ctrl+L` | Limpar tela |
| `F1` | Mostrar ajuda |

### **2. Usar Visualizar Informações**

Antes de processar, visualize as informações do documento:

1. Selecione o arquivo de origem
2. Navegue até "📊 Visualizar Informações"
3. Pressione `Enter`
4. Verifique se o texto a ser substituído existe
5. Depois prossiga com o processamento

### **3. Escolher o Método Certo**

| Método | Quando Usar |
|--------|-------------|
| **Exato (Exact)** | Documentos simples, sem elementos visuais |
| **Preservar Layout** ⭐ | Documentos com imagens, gráficos, backgrounds |
| **Preservar Background** ⭐ | Documentos com cores de fundo, highlights |
| **Estrutura** | Quando a consistência visual é importante |
| **Compreensivo** | Documentos complexos com múltiplos elementos |

### **4. Ordem das Substituições**

A ordem das substituições na lista é importante:

```python
# Ordem correta
1. "João Silva" → "Maria Santos"
2. "Silva" → "Santos"  # Isso funcionará

# Ordem incorreta
1. "Silva" → "Santos"
2. "João Silva" → "Maria Santos"  # Isso não funcionará
```

### **5. Usar Case-Sensitive com Cuidado**

Marque "Diferenciar maiúsculas/minúsculas" apenas quando necessário:

- ✅ Use quando o texto tem variações de maiúsculas/minúsculas específicas
- ❌ Não use para substituições genéricas

### **6. Backup Automático**

Antes de processar documentos importantes:

1. Faça uma cópia do original
2. Processe a cópia
3. Verifique o resultado
4. Se estiver correto, use o original

### **7. Processamento em Lote Eficiente**

Para processamento em lote:

- Organize PDFs em pastas por tipo
- Use configurações consistentes
- Monitore o log para erros
- Verifique os resultados

### **8. Validação de Resultados**

Após processar:

1. Abra o PDF processado
2. Verifique se as substituições foram aplicadas
3. Confirme que elementos visuais foram preservados
4. Compare com o original se necessário

### **9. Troubleshooting**

#### **Substituição Não Funciona**

- Verifique se o texto a buscar está correto
- Tente usar case-sensitive
- Use "Visualizar Informações" para verificar se o texto existe

#### **Elementos Visuais Não Preservados**

- Use "Preservar Layout" em vez de "Exato"
- Verifique se o PDF tem elementos visuais
- Teste com "Preservar Background"

#### **Erro ao Processar**

- Verifique se o arquivo PDF não está corrompido
- Confirme que o arquivo não está protegido por senha
- Tente usar um método diferente

#### **Navegação Difícil**

- Use `Tab` para alternar entre campos
- Use as setas para navegar em menus
- Pressione `Esc` para voltar
- Pressione `q` para sair

---

## 📚 Recursos Adicionais

- [README.md](../README.md) - Visão geral do projeto
- [docs/DOCUMENTACAO_COMPLETA.md](DOCUMENTACAO_COMPLETA.md) - Documentação completa
- [docs/LAYOUT_PRESERVATION.md](LAYOUT_PRESERVATION.md) - Preservação de layout
- [docs/GUIA_CLI.md](GUIA_CLI.md) - Guia da interface de linha de comando
- [docs/GUIA_GUI.md](GUIA_GUI.md) - Guia da interface gráfica
- [docs/GUIA_API.md](GUIA_API.md) - Guia da API Python
