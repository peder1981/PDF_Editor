# Editor de PDF

Substituição de texto em arquivos PDF com preservação de layout, fontes e elementos gráficos.

## O que faz

- Busca um texto no PDF e substitui por outro
- Preserva fontes, cores, imagens e layout original
- Funciona com PDFs de múltiplas páginas
- Permite visualizar o resultado antes de confirmar

## Como usar (interface gráfica)

```bash
python main_launcher.py
```

A interface tem 4 passos simples:

1. **Selecionar o PDF** — clique em "Procurar PDF..." e escolha o arquivo
2. **O que alterar** — digite o texto a buscar e o texto substituto
3. **Visualizar** — clique em "Visualizar alteração" para ver o resultado no visualizador do sistema
4. **Confirmar e salvar** — escolha onde salvar e clique em "Confirmar e Salvar"

## Como usar (linha de comando)

Substituição simples:

```bash
python -m interfaces.cli replace entrada.pdf "texto antigo" "texto novo" saida.pdf
```

Substituição em lote (a partir de arquivo JSON):

```bash
python -m interfaces.cli batch entrada.pdf substituicoes.json saida.pdf
```

Exemplo de arquivo JSON para lote:

```json
[
  {"search": "João da Silva", "replace": "Maria Santos", "case_sensitive": false},
  {"search": "2023", "replace": "2024", "case_sensitive": false}
]
```

Buscar texto no PDF (sem alterar):

```bash
python -m interfaces.cli search entrada.pdf "texto"
```

Ver informações do PDF:

```bash
python -m interfaces.cli info entrada.pdf
```

## Métodos de substituição

| Método | Descrição |
|---|---|
| `exact` | Substituição exata, posição por posição (padrão) |
| `layout-preserving` | Preserva gráficos, imagens e elementos de fundo |
| `background-preserving` | Preserva apenas o fundo, substitui texto |

## Instalação

```bash
pip install -r requirements.txt
```

Dependências: PyMuPDF, rich, textual, typer, pillow, tqdm

## Estrutura do projeto

```
PDF_Editor/
├── main_launcher.py          # Ponto de entrada — inicia a interface gráfica
├── unified_gui.py            # Interface gráfica (4 passos)
├── unified_tui.py            # Interface de terminal (abas)
├── interfaces/
│   └── cli.py                # Linha de comando
├── core/
│   ├── pdf_editor.py         # Núcleo — carrega, busca e substitui texto
│   ├── method_dispatch.py    # Dispatch de métodos (tabela única)
│   ├── batch_processor.py    # Processamento em lote
│   ├── layout_preserving_editor.py   # Editor de preservação de layout
│   └── improved_layout_editor.py     # Editor de layout aprimorado
├── scripts/
│   └── common_replacements.py  # Substituições guiadas para certificados
├── tests/
│   └── test_pdf_editor.py    # Testes automatizados
└── requirements.txt
```

## Testes

```bash
cd tests && python test_pdf_editor.py
```

## Licença

MIT
