#!/usr/bin/env python3
"""
Advanced PDF Editor - Terminal User Interface
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Button, Header, Footer, Input, Label, DataTable, 
    TextLog, ProgressBar, Select, Checkbox, Static, RichLog
)
from textual.screen import ModalScreen
from textual.message import Message
from typing import Optional
from pathlib import Path
import asyncio
from rich.text import Text

from pdf_editor import PDFEditor, EditOperation


class FileSelectModal(ModalScreen):
    """Modal for file selection"""
    
    def compose(self) -> ComposeResult:
        yield Container(
            Label("Enter PDF file path:", classes="label"),
            Input(placeholder="path/to/your.pdf", classes="input"),
            Horizontal(
                Button("Cancel", variant="primary", id="cancel"),
                Button("Open", variant="success", id="open"),
                classes="buttons"
            ),
            classes="dialog"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
        elif event.button.id == "open":
            input_widget = self.query_one(Input)
            self.dismiss(input_widget.value)


class ReplaceModal(ModalScreen):
    """Modal for text replacement configuration"""
    
    def compose(self) -> ComposeResult:
        yield Container(
            Label("Text Replacement", classes="title"),
            Label("Search for:", classes="label"),
            Input(placeholder="Text to find...", id="search_input"),
            Label("Replace with:", classes="label"),
            Input(placeholder="Replacement text...", id="replace_input"),
            Label("Method:", classes="label"),
            Select([
                ("Exact Positioning", "exact"),
                ("Comprehensive", "comprehensive"),
                ("Structure Preserving", "structure")
            ], value="exact", id="method_select"),
            Checkbox("Case sensitive", id="case_checkbox"),
            Checkbox("Preview before applying", id="preview_checkbox", value=True),
            Horizontal(
                Button("Cancel", variant="primary", id="cancel"),
                Button("Replace", variant="success", id="replace"),
                classes="buttons"
            ),
            classes="dialog"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
        elif event.button.id == "replace":
            search_input = self.query_one("#search_input", Input)
            replace_input = self.query_one("#replace_input", Input)
            method_select = self.query_one("#method_select", Select)
            case_checkbox = self.query_one("#case_checkbox", Checkbox)
            preview_checkbox = self.query_one("#preview_checkbox", Checkbox)
            
            result = {
                "search": search_input.value,
                "replace": replace_input.value,
                "method": method_select.value,
                "case_sensitive": case_checkbox.value,
                "preview": preview_checkbox.value
            }
            self.dismiss(result)


class PDFEditorTUI(App):
    """Main TUI Application for PDF Editor"""
    
    CSS = """
    .dialog {
        width: 60%;
        height: auto;
        background: $surface;
        border: thick $primary;
        padding: 1;
        margin: 2;
    }
    
    .buttons {
        width: 100%;
        height: auto;
        align: center middle;
        margin-top: 1;
    }
    
    .buttons Button {
        margin: 0 1;
    }
    
    .info-panel {
        height: 8;
        border: solid $primary;
        padding: 1;
    }
    
    .search-results {
        height: 1fr;
        border: solid $secondary;
    }
    
    .log-panel {
        height: 12;
        border: solid $accent;
    }
    
    .controls {
        height: auto;
        dock: bottom;
        padding: 1;
        background: $surface;
    }
    
    .title {
        text-style: bold;
        color: $primary;
        margin-bottom: 1;
    }
    
    .label {
        margin-top: 1;
        margin-bottom: 0;
    }
    
    .input {
        margin-bottom: 1;
    }
    """
    
    TITLE = "Advanced PDF Editor"
    SUB_TITLE = "Structure-preserving PDF text editing"
    
    def __init__(self):
        super().__init__()
        self.pdf_editor: Optional[PDFEditor] = None
        self.current_file: Optional[str] = None
        
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Container():
            # Info panel
            with Container(classes="info-panel"):
                yield Label("No PDF loaded", id="file_info")
                yield Label("Ready", id="status_info")
                
            # Main content area
            with Horizontal():
                # Left panel - Controls
                with Vertical(classes="controls"):
                    yield Button("📁 Open PDF", id="open_btn", variant="primary")
                    yield Button("🔍 Search Text", id="search_btn")
                    yield Button("✏️  Replace Text", id="replace_btn")
                    yield Button("📊 Document Info", id="info_btn")
                    yield Button("💾 Save As", id="save_btn")
                    yield Button("🔄 Reload", id="reload_btn")
                    
                # Right panel - Results
                with Vertical():
                    yield Label("Search Results", classes="title")
                    with Container(classes="search-results"):
                        yield DataTable(id="results_table")
                    
                    # Log panel
                    with Container(classes="log-panel"):
                        yield RichLog(id="log", highlight=True, markup=True)
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize the application"""
        # Setup results table
        table = self.query_one("#results_table", DataTable)
        table.add_columns("Page", "Text", "Position", "Font")
        
        # Initial log message
        log = self.query_one("#log", RichLog)
        log.write("🚀 PDF Editor ready! Open a PDF file to start editing.")
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        button_id = event.button.id
        log = self.query_one("#log", RichLog)
        
        if button_id == "open_btn":
            await self._open_file()
        elif button_id == "search_btn":
            await self._search_text()
        elif button_id == "replace_btn":
            await self._replace_text()
        elif button_id == "info_btn":
            await self._show_info()
        elif button_id == "save_btn":
            await self._save_file()
        elif button_id == "reload_btn":
            await self._reload_file()
        else:
            log.write(f"[yellow]Unknown button: {button_id}[/yellow]")
    
    async def _open_file(self) -> None:
        """Open a PDF file"""
        log = self.query_one("#log", RichLog)
        
        file_path = await self.push_screen_wait(FileSelectModal())
        if not file_path:
            return
        
        if not Path(file_path).exists():
            log.write(f"[red]❌ File not found: {file_path}[/red]")
            return
        
        try:
            log.write(f"[blue]📖 Loading: {file_path}[/blue]")
            
            # Close previous document
            if self.pdf_editor:
                self.pdf_editor.close()
            
            # Load new document
            self.pdf_editor = PDFEditor()
            if self.pdf_editor.load(file_path):
                self.current_file = file_path
                
                # Update UI
                file_info = self.query_one("#file_info", Label)
                file_info.update(f"📄 {Path(file_path).name}")
                
                status_info = self.query_one("#status_info", Label)
                doc_info = self.pdf_editor.get_document_info()
                status_info.update(f"Pages: {doc_info['page_count']}, Text instances: {doc_info['text_instances']}")
                
                log.write(f"[green]✅ Loaded successfully![/green]")
                log.write(f"[cyan]📊 {doc_info['page_count']} pages, {doc_info['text_instances']} text instances[/cyan]")
            else:
                log.write(f"[red]❌ Failed to load PDF[/red]")
                
        except Exception as e:
            log.write(f"[red]❌ Error loading file: {str(e)}[/red]")
    
    async def _search_text(self) -> None:
        """Search for text in the PDF"""
        if not self.pdf_editor:
            log = self.query_one("#log", RichLog)
            log.write("[yellow]⚠️  No PDF loaded[/yellow]")
            return
        
        # Simple search input (could be enhanced with a modal)
        search_term = await self._get_input("Enter search term:")
        if not search_term:
            return
        
        log = self.query_one("#log", RichLog)
        log.write(f"[blue]🔍 Searching for: '{search_term}'[/blue]")
        
        try:
            results = self.pdf_editor.search_text(search_term)
            
            # Update results table
            table = self.query_one("#results_table", DataTable)
            table.clear()
            
            for instance in results:
                table.add_row(
                    str(instance.page_num + 1),
                    instance.text[:30] + "..." if len(instance.text) > 30 else instance.text,
                    f"({instance.rect.x0:.1f}, {instance.rect.y0:.1f})",
                    instance.font
                )
            
            log.write(f"[green]✅ Found {len(results)} instances[/green]")
            
        except Exception as e:
            log.write(f"[red]❌ Search error: {str(e)}[/red]")
    
    async def _replace_text(self) -> None:
        """Replace text in the PDF"""
        if not self.pdf_editor:
            log = self.query_one("#log", RichLog)
            log.write("[yellow]⚠️  No PDF loaded[/yellow]")
            return
        
        # Get replacement parameters
        config = await self.push_screen_wait(ReplaceModal())
        if not config:
            return
        
        log = self.query_one("#log", RichLog)
        log.write(f"[blue]✏️  Replacing '{config['search']}' with '{config['replace']}'[/blue]")
        
        try:
            # Preview if requested
            if config['preview']:
                results = self.pdf_editor.search_text(config['search'], config['case_sensitive'])
                if not results:
                    log.write("[yellow]⚠️  No instances found to replace[/yellow]")
                    return
                
                log.write(f"[cyan]👀 Preview: {len(results)} instances will be replaced[/cyan]")
                
                # Update table with preview
                table = self.query_one("#results_table", DataTable)
                table.clear()
                for instance in results:
                    table.add_row(
                        str(instance.page_num + 1),
                        instance.text[:30] + "..." if len(instance.text) > 30 else instance.text,
                        f"({instance.rect.x0:.1f}, {instance.rect.y0:.1f})",
                        instance.font
                    )
            
            # Perform replacement
            if config['method'] == "exact":
                count = self.pdf_editor.replace_text_exact(
                    config['search'], 
                    config['replace'], 
                    config['case_sensitive']
                )
            elif config['method'] == "comprehensive":
                count = self.pdf_editor.replace_text_comprehensive(
                    config['search'], 
                    config['replace']
                )
            elif config['method'] == "structure":
                count = self.pdf_editor.replace_text_structure_preserving(
                    config['search'], 
                    config['replace']
                )
            else:
                count = 0
            
            log.write(f"[green]✅ Replaced {count} instances using {config['method']} method[/green]")
            
        except Exception as e:
            log.write(f"[red]❌ Replacement error: {str(e)}[/red]")
    
    async def _show_info(self) -> None:
        """Show document information"""
        if not self.pdf_editor:
            log = self.query_one("#log", RichLog)
            log.write("[yellow]⚠️  No PDF loaded[/yellow]")
            return
        
        info = self.pdf_editor.get_document_info()
        log = self.query_one("#log", RichLog)
        
        log.write("[cyan]📊 Document Information:[/cyan]")
        log.write(f"  📄 Pages: {info['page_count']}")
        log.write(f"  📝 Text instances: {info['text_instances']}")
        log.write(f"  💾 File size: {info['file_size']:,} bytes")
        
        if info.get('metadata'):
            log.write("  📋 Metadata:")
            for key, value in info['metadata'].items():
                if value:
                    log.write(f"    {key}: {str(value)[:50]}")
    
    async def _save_file(self) -> None:
        """Save the edited PDF"""
        if not self.pdf_editor:
            log = self.query_one("#log", RichLog)
            log.write("[yellow]⚠️  No PDF loaded[/yellow]")
            return
        
        output_path = await self._get_input("Enter output file path:")
        if not output_path:
            return
        
        log = self.query_one("#log", RichLog)
        log.write(f"[blue]💾 Saving to: {output_path}[/blue]")
        
        try:
            if self.pdf_editor.save(output_path):
                log.write(f"[green]✅ Saved successfully![/green]")
            else:
                log.write(f"[red]❌ Failed to save file[/red]")
        except Exception as e:
            log.write(f"[red]❌ Save error: {str(e)}[/red]")
    
    async def _reload_file(self) -> None:
        """Reload the current file"""
        if not self.current_file:
            log = self.query_one("#log", RichLog)
            log.write("[yellow]⚠️  No file to reload[/yellow]")
            return
        
        log = self.query_one("#log", RichLog)
        log.write(f"[blue]🔄 Reloading: {self.current_file}[/blue]")
        
        # Reload the file
        if self.pdf_editor:
            self.pdf_editor.close()
        
        self.pdf_editor = PDFEditor()
        if self.pdf_editor.load(self.current_file):
            doc_info = self.pdf_editor.get_document_info()
            status_info = self.query_one("#status_info", Label)
            status_info.update(f"Pages: {doc_info['page_count']}, Text instances: {doc_info['text_instances']}")
            log.write("[green]✅ Reloaded successfully![/green]")
        else:
            log.write("[red]❌ Failed to reload file[/red]")
    
    async def _get_input(self, prompt: str) -> Optional[str]:
        """Get input from user (simplified version)"""
        # This is a simplified implementation
        # In a full implementation, you'd create a proper input modal
        return await self.push_screen_wait(FileSelectModal())


def main():
    """Run the TUI application"""
    app = PDFEditorTUI()
    app.run()


if __name__ == "__main__":
    main()
