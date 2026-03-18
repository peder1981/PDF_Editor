#!/usr/bin/env python3
"""
PDF Editor - Unified TUI Application
Terminal User Interface unificada, robusta e intuitiva
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Button, Header, Footer, Input, Label, DataTable, 
    RichLog, Select, Checkbox, Static, DirectoryTree, 
    TabbedContent, TabPane
)
from textual.screen import ModalScreen
from textual.reactive import reactive
from pathlib import Path
import threading
from typing import List, Dict, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent / "core"))

from pdf_editor import PDFEditor, EditOperation
from batch_processor import BatchProcessor


class FileBrowserModal(ModalScreen):
    """Modal para seleção de arquivos/pastas"""
    
    def __init__(self, mode: str = "file"):
        super().__init__()
        self.mode = mode  # "file" ou "directory"
        self.selected_path = None
    
    def compose(self) -> ComposeResult:
        with Container(classes="dialog"):
            yield Label(f"Selecione {'o arquivo PDF' if self.mode == 'file' else 'a pasta'}:", classes="title")
            
            # Input manual
            yield Label("Caminho:", classes="label")
            self.path_input = Input(placeholder="/caminho/do/arquivo.pdf", classes="input")
            yield self.path_input
            
            # Botões
            with Horizontal(classes="buttons"):
                yield Button("❌ Cancelar", variant="error", id="cancel")
                yield Button("✅ Confirmar", variant="success", id="confirm")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
        elif event.button.id == "confirm":
            self.dismiss(self.path_input.value)


class UnifiedTUIMain(App):
    """TUI Unificada Principal"""
    
    CSS = """
    .dialog {
        width: 80%;
        height: auto;
        background: $surface;
        border: thick $primary;
        padding: 2;
        margin: 2;
    }
    
    .title {
        text-style: bold;
        color: $primary;
        margin-bottom: 1;
    }
    
    .label {
        margin-top: 1;
    }
    
    .input {
        margin-bottom: 1;
    }
    
    .buttons {
        margin-top: 2;
        align: center middle;
    }
    
    .buttons Button {
        margin: 0 1;
    }
    
    .main-container {
        padding: 1;
    }
    
    .section {
        border: solid $primary;
        padding: 1;
        margin: 1 0;
    }
    
    .path-display {
        color: $success;
        text-style: bold;
    }
    
    .replacements-list {
        height: 8;
        border: solid $secondary;
    }
    
    .log-area {
        height: 12;
        border: solid $accent;
    }
    """
    
    TITLE = "PDF Editor - TUI Unificada"
    SUB_TITLE = "Edição de texto em PDFs - Modo Terminal"
    
    # Reactive variables
    source_path = reactive("")
    dest_path = reactive("")
    replacements = reactive(list)
    
    def __init__(self):
        super().__init__()
        self.source_mode = "single"  # "single" ou "batch"
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container(classes="main-container"):
            # Título
            yield Label("📄 PDF Editor - Interface Terminal Unificada", classes="title")
            
            # Abas principais
            with TabbedContent():
                # Aba: Origem e Destino
                with TabPane("📁 Origem & Destino", id="source-tab"):
                    yield self._create_source_section()
                
                # Aba: Substituições
                with TabPane("✏️ Substituições", id="replace-tab"):
                    yield self._create_replacements_section()
                
                # Aba: Opções e Processamento
                with TabPane("⚙️ Opções & Processar", id="process-tab"):
                    yield self._create_process_section()
            
            # Área de log
            yield Label("📋 Log de Operações:")
            yield RichLog(id="log", classes="log-area", highlight=True, markup=True)
        
        yield Footer()
    
    def _create_source_section(self) -> Container:
        """Cria seção de origem e destino"""
        widgets = [
            Label("🎯 Modo de Operação:", classes="label"),
            Horizontal(
                Button("📄 Arquivo Único", variant="primary", id="single-mode"),
                Button("📁 Processamento em Lote", id="batch-mode")
            ),
            Label("📁 Origem:", classes="label"),
            Horizontal(
                Static(id="source-display", classes="path-display"),
                Button("🔍 Selecionar", id="select-source")
            ),
            Label("💾 Destino:", classes="label"),
            Horizontal(
                Static(id="dest-display", classes="path-display"),
                Button("🔍 Selecionar", id="select-dest")
            )
        ]
        
        return Container(*widgets, classes="section")
    
    def _create_replacements_section(self) -> Container:
        """Cria seção de substituições"""
        widgets = [
            Label("➕ Adicionar Substituição:", classes="label"),
            Horizontal(
                Label("Buscar:"),
                Input(placeholder="Texto a ser encontrado...", id="search-input"),
                Label("Substituir por:"),
                Input(placeholder="Novo texto...", id="replace-input"),
                Button("➕ Adicionar", id="add-replacement")
            ),
            Label("📋 Substituições Configuradas:"),
            DataTable(id="replacements-table", classes="replacements-list"),
            Horizontal(
                Button("🗑️ Remover Selecionado", id="remove-replacement"),
                Button("🗑️ Limpar Todos", id="clear-replacements")
            )
        ]
        
        return Container(*widgets, classes="section")
    
    def _create_process_section(self) -> Container:
        """Cria seção de processamento"""
        widgets = [
            Label("⚙️ Opções:", classes="label"),
            Horizontal(
                Label("Método:"),
                Select(
                    [("Exato (Exact)", "exact"), 
                     ("Compreensivo", "comprehensive"),
                     ("Estrutura", "structure"),
                     ("Inteligente (Smart)", "smart"),
                     ("Heurístico", "heuristic"),
                     ("Integral", "integral"),
                     ("Template", "template"),
                     ("Preservar Layout", "layout-preserving"),
                     ("Preservar Background", "background-preserving")],
                    value="exact",
                    id="method-select"
                ),
                Checkbox("Diferenciar maiúsculas/minúsculas", id="case-sensitive")
            ),
            Label(""),  # Espaço
            Horizontal(
                Button("📊 Visualizar Informações", id="preview-info"),
                Button("🚀 Processar", variant="success", id="process")
            ),
            Label(""),  # Espaço
            Static(id="status-display", classes="path-display")
        ]
        
        return Container(*widgets, classes="section")
    
    def on_mount(self) -> None:
        """Inicialização"""
        self._log("🚀 PDF Editor - TUI Unificada iniciada")
        self._log("📖 Use as abas para navegar entre as funcionalidades")
        self._log("📁 Comece selecionando a origem na aba 'Origem & Destino'")
        
        # Configurar tabela
        table = self.query_one("#replacements-table", DataTable)
        table.add_columns("Buscar", "Substituir por")
        
        # Atualizar displays
        self._update_displays()
    
    def _log(self, message: str):
        """Adiciona mensagem ao log"""
        log = self.query_one("#log", RichLog)
        log.write(message)
    
    def _update_displays(self):
        """Atualiza displays de caminho"""
        source_display = self.query_one("#source-display", Static)
        dest_display = self.query_one("#dest-display", Static)
        status_display = self.query_one("#status-display", Static)
        
        source_display.update(f"📁 {self.source_path or 'Não selecionado'}")
        dest_display.update(f"💾 {self.dest_path or 'Não selecionado'}")
        
        if self.source_path and self.dest_path:
            status_display.update("✅ Pronto para processar")
        else:
            status_display.update("⚠️ Selecione origem e destino")
    
    def watch_source_path(self, path: str):
        """Observa mudanças no caminho de origem"""
        self._update_displays()
    
    def watch_dest_path(self, path: str):
        """Observa mudanças no caminho de destino"""
        self._update_displays()
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handler de botões"""
        button_id = event.button.id
        
        if button_id == "single-mode":
            self.source_mode = "single"
            self.single_mode_btn.variant = "primary"
            self.batch_mode_btn.variant = "default"
            self._log("📄 Modo selecionado: Arquivo único")
        
        elif button_id == "batch-mode":
            self.source_mode = "batch"
            self.batch_mode_btn.variant = "primary"
            self.single_mode_btn.variant = "default"
            self._log("📁 Modo selecionado: Processamento em lote")
        
        elif button_id == "select-source":
            path = await self.push_screen_wait(FileBrowserModal(mode=self.source_mode))
            if path:
                self.source_path = path
                self._log(f"📁 Origem selecionada: {path}")
        
        elif button_id == "select-dest":
            path = await self.push_screen_wait(FileBrowserModal(mode="directory"))
            if path:
                self.dest_path = path
                self._log(f"💾 Destino selecionado: {path}")
        
        elif button_id == "add-replacement":
            self._add_replacement()
        
        elif button_id == "remove-replacement":
            self._remove_replacement()
        
        elif button_id == "clear-replacements":
            self._clear_replacements()
        
        elif button_id == "preview-info":
            self._preview_info()
        
        elif button_id == "process":
            self._process()
    
    def _add_replacement(self):
        """Adiciona substituição"""
        search_input = self.query_one("#search-input", Input)
        replace_input = self.query_one("#replace-input", Input)
        
        search = search_input.value.strip()
        replace = replace_input.value.strip()
        
        if not search:
            self._log("❌ Digite o texto a ser buscado")
            return
        
        self.replacements.append({"search": search, "replace": replace})
        
        table = self.query_one("#replacements-table", DataTable)
        table.add_row(search, replace)
        
        self._log(f"➕ Adicionada: '{search}' → '{replace}'")
        
        # Limpar inputs
        search_input.value = ""
        replace_input.value = ""
    
    def _remove_replacement(self):
        """Remove substituição selecionada"""
        table = self.query_one("#replacements-table", DataTable)
        
        if table.cursor_row is not None and table.cursor_row < len(self.replacements):
            removed = self.replacements.pop(table.cursor_row)
            table.remove_row(table.cursor_row)
            self._log(f"🗑️ Removida: '{removed['search']}' → '{removed['replace']}'")
    
    def _clear_replacements(self):
        """Limpa todas as substituições"""
        self.replacements.clear()
        table = self.query_one("#replacements-table", DataTable)
        table.clear()
        self._log("🗑️ Todas as substituições removidas")
    
    def _preview_info(self):
        """Visualiza informações do PDF"""
        if not self.source_path:
            self._log("❌ Selecione uma origem primeiro")
            return
        
        if not Path(self.source_path).exists():
            self._log("❌ Arquivo/pasta não existe")
            return
        
        if Path(self.source_path).is_dir():
            self._log("📁 Visualização disponível apenas para arquivos únicos")
            return
        
        try:
            editor = PDFEditor()
            if editor.load(self.source_path):
                info = editor.get_document_info()
                
                self._log("📄 Informações do PDF:")
                self._log(f"   📊 Páginas: {info['page_count']}")
                self._log(f"   📝 Instâncias de texto: {info['text_instances']}")
                self._log(f"   💾 Tamanho: {info['file_size']:,} bytes")
                
                if info.get('metadata'):
                    self._log("   📋 Metadados:")
                    for key, value in info['metadata'].items():
                        if value:
                            self._log(f"      • {key}: {value}")
                
                editor.close()
            else:
                self._log("❌ Falha ao carregar PDF")
        except Exception as e:
            self._log(f"❌ Erro: {str(e)}")
    
    def _validate(self) -> bool:
        """Valida configurações"""
        if not self.source_path:
            self._log("❌ Selecione a origem")
            return False
        
        if not self.dest_path:
            self._log("❌ Selecione o destino")
            return False
        
        if not self.replacements:
            self._log("❌ Adicione pelo menos uma substituição")
            return False
        
        if not Path(self.source_path).exists():
            self._log("❌ Origem não existe")
            return False
        
        return True
    
    def _process(self):
        """Inicia processamento"""
        if not self._validate():
            return
        
        self._log("🚀 Iniciando processamento...")
        self._log(f"📁 Origem: {self.source_path}")
        self._log(f"💾 Destino: {self.dest_path}")
        self._log(f"📊 {len(self.replacements)} substituições configuradas")
        
        # Executar em thread
        thread = threading.Thread(target=self._process_thread)
        thread.daemon = True
        thread.start()
    
    def _process_thread(self):
        """Thread de processamento"""
        try:
            method = self.query_one("#method-select", Select).value
            case_sensitive = self.query_one("#case-sensitive", Checkbox).value
            
            if self.source_mode == "single":
                self._process_single(method, case_sensitive)
            else:
                self._process_batch(method, case_sensitive)
            
            self._log("✅ Processamento concluído!")
            
        except Exception as e:
            self._log(f"❌ Erro no processamento: {str(e)}")
    
    def _process_single(self, method: str, case_sensitive: bool):
        """Processa arquivo único"""
        self._log("📄 Processando arquivo único...")
        
        editor = PDFEditor()
        
        if not editor.load(self.source_path):
            raise Exception("Falha ao carregar PDF")
        
        self._log(f"✅ PDF carregado: {len(editor.text_instances)} instâncias de texto")
        
        for rep in self.replacements:
            search_text = rep["search"]
            replace_text = rep["replace"]
            
            self._log(f"✏️ Substituindo: '{search_text}' → '{replace_text}'")
            
            if method == "exact":
                count = editor.replace_text_exact(search_text, replace_text, case_sensitive)
            elif method == "comprehensive":
                count = editor.replace_text_comprehensive(search_text, replace_text)
            elif method == "structure":
                count = editor.replace_text_structure_preserving(search_text, replace_text)
            elif method == "smart":
                count = editor.replace_text_smart(search_text, replace_text)
            elif method == "heuristic":
                count = editor.replace_text_heuristic(search_text, replace_text)
            elif method == "integral":
                count = editor.replace_text_integral(search_text, replace_text)
            elif method == "template":
                count = editor.replace_text_template(search_text, replace_text)
            else:
                count = 0
            
            self._log(f"   → {count} substituições realizadas")
        
        output_file = Path(self.dest_path) / f"{Path(self.source_path).stem}_edited.pdf"
        Path(self.dest_path).mkdir(parents=True, exist_ok=True)
        
        if editor.save(str(output_file)):
            self._log(f"✅ Arquivo salvo: {output_file}")
        else:
            raise Exception("Falha ao salvar arquivo")
        
        editor.close()
    
    def _process_batch(self, method: str, case_sensitive: bool):
        """Processamento em lote"""
        self._log("📁 Iniciando processamento em lote...")
        
        processor = BatchProcessor(max_workers=4)
        
        operations = []
        for rep in self.replacements:
            operations.append(EditOperation(
                search_text=rep["search"],
                replace_text=rep["replace"],
                case_sensitive=case_sensitive
            ))
        
        jobs_added = processor.process_directory(
            input_dir=self.source_path,
            output_dir=self.dest_path,
            operations=operations,
            method=method
        )
        
        self._log(f"📊 {jobs_added} arquivos adicionados à fila")
        
        results = processor.process_jobs()
        
        self._log(f"✅ Concluído: {results['completed']} de {results['total']} arquivos")
        if results['failed'] > 0:
            self._log(f"❌ Falhas: {results['failed']} arquivos")
        
        self._log(f"📊 Total de substituições: {results['total_replacements']}")


def main():
    """Função principal"""
    app = UnifiedTUIMain()
    app.run()


if __name__ == "__main__":
    main()
