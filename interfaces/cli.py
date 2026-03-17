#!/usr/bin/env python3
"""
Advanced PDF Editor - Command Line Interface
"""

import typer
from typing import Optional, List
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
import json

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from pdf_editor import PDFEditor, EditOperation
from batch_processor import BatchProcessor

app = typer.Typer(help="Advanced PDF Editor - Edit PDFs while preserving structure")
console = Console()


@app.command()
def replace(
    input_file: Path = typer.Argument(..., help="Input PDF file"),
    search_text: str = typer.Argument(..., help="Text to search for"),
    replace_text: str = typer.Argument(..., help="Replacement text"),
    output_file: Optional[Path] = typer.Argument(None, help="Output PDF file"),
    method: str = typer.Option("exact", help="Replacement method: exact, comprehensive, structure"),
    case_sensitive: bool = typer.Option(False, "--case-sensitive", "-c", help="Case sensitive search"),
    preview: bool = typer.Option(False, "--preview", "-p", help="Preview changes before applying")
):
    """Replace text in a PDF file"""
    
    if not input_file.exists():
        console.print(f"[red]Error: Input file '{input_file}' not found[/red]")
        raise typer.Exit(1)
    
    if output_file is None:
        output_file = input_file.parent / f"{input_file.stem}_edited{input_file.suffix}"
    
    with console.status(f"[bold green]Loading PDF: {input_file}"):
        editor = PDFEditor()
        if not editor.load(str(input_file)):
            console.print(f"[red]Error: Could not load PDF file[/red]")
            raise typer.Exit(1)
    
    # Preview mode
    if preview:
        search_results = editor.search_text(search_text, case_sensitive)
        if not search_results:
            console.print(f"[yellow]No instances of '{search_text}' found[/yellow]")
            return
        
        table = Table(title=f"Preview: '{search_text}' → '{replace_text}'")
        table.add_column("Page", justify="right", style="cyan")
        table.add_column("Text", style="magenta", max_width=50)
        table.add_column("Position", style="green")
        
        for instance in search_results:
            table.add_row(
                str(instance.page_num + 1),
                instance.text[:47] + "..." if len(instance.text) > 50 else instance.text,
                f"({instance.rect.x0:.1f}, {instance.rect.y0:.1f})"
            )
        
        console.print(table)
        
        if not typer.confirm(f"Apply {len(search_results)} replacements?"):
            console.print("[yellow]Operation cancelled[/yellow]")
            return
    
    # Perform replacement
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Replacing text using {method} method...", total=None)
        
        if method == "exact":
            replacements = editor.replace_text_exact(search_text, replace_text, case_sensitive)
        elif method == "comprehensive":
            replacements = editor.replace_text_comprehensive(search_text, replace_text)
        elif method == "structure":
            replacements = editor.replace_text_structure_preserving(search_text, replace_text)
        else:
            console.print(f"[red]Error: Unknown method '{method}'[/red]")
            raise typer.Exit(1)
        
        progress.update(task, description="Saving PDF...")
        
        if editor.save(str(output_file)):
            progress.update(task, description="Complete!")
        else:
            console.print("[red]Error: Could not save output file[/red]")
            raise typer.Exit(1)
    
    editor.close()
    
    console.print(Panel(
        f"✅ Successfully replaced [cyan]{replacements}[/cyan] instances\n"
        f"📄 Output saved to: [green]{output_file}[/green]\n"
        f"🔧 Method used: [yellow]{method}[/yellow]",
        title="Operation Complete",
        border_style="green"
    ))


@app.command()
def batch(
    input_file: Path = typer.Argument(..., help="Input PDF file"),
    replacements_file: Path = typer.Argument(..., help="JSON file with replacements"),
    output_file: Optional[Path] = typer.Argument(None, help="Output PDF file"),
    method: str = typer.Option("exact", help="Replacement method: exact, comprehensive, structure")
):
    """Perform batch text replacements from a JSON file"""
    
    if not input_file.exists():
        console.print(f"[red]Error: Input file '{input_file}' not found[/red]")
        raise typer.Exit(1)
    
    if not replacements_file.exists():
        console.print(f"[red]Error: Replacements file '{replacements_file}' not found[/red]")
        raise typer.Exit(1)
    
    if output_file is None:
        output_file = input_file.parent / f"{input_file.stem}_batch_edited{input_file.suffix}"
    
    # Load replacements
    try:
        with open(replacements_file, 'r') as f:
            replacements_data = json.load(f)
    except Exception as e:
        console.print(f"[red]Error reading replacements file: {e}[/red]")
        raise typer.Exit(1)
    
    # Convert to EditOperation objects
    operations = []
    for item in replacements_data:
        operations.append(EditOperation(
            search_text=item["search"],
            replace_text=item["replace"],
            case_sensitive=item.get("case_sensitive", False)
        ))
    
    # Load PDF
    with console.status(f"[bold green]Loading PDF: {input_file}"):
        editor = PDFEditor()
        if not editor.load(str(input_file)):
            console.print(f"[red]Error: Could not load PDF file[/red]")
            raise typer.Exit(1)
    
    # Perform batch replacements
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Processing {len(operations)} replacements...", total=None)
        
        results = editor.batch_replace(operations, method)
        
        progress.update(task, description="Saving PDF...")
        
        if editor.save(str(output_file)):
            progress.update(task, description="Complete!")
        else:
            console.print("[red]Error: Could not save output file[/red]")
            raise typer.Exit(1)
    
    editor.close()
    
    # Show results table
    table = Table(title="Batch Replacement Results")
    table.add_column("Operation", style="cyan")
    table.add_column("Replacements", justify="right", style="green")
    
    total_replacements = 0
    for operation, count in results.items():
        table.add_row(operation, str(count))
        total_replacements += count
    
    console.print(table)
    console.print(Panel(
        f"✅ Total replacements: [cyan]{total_replacements}[/cyan]\n"
        f"📄 Output saved to: [green]{output_file}[/green]",
        title="Batch Operation Complete",
        border_style="green"
    ))


@app.command()
def search(
    input_file: Path = typer.Argument(..., help="Input PDF file"),
    search_text: str = typer.Argument(..., help="Text to search for"),
    case_sensitive: bool = typer.Option(False, "--case-sensitive", "-c", help="Case sensitive search"),
    regex: bool = typer.Option(False, "--regex", "-r", help="Use regular expression")
):
    """Search for text in a PDF file"""
    
    if not input_file.exists():
        console.print(f"[red]Error: Input file '{input_file}' not found[/red]")
        raise typer.Exit(1)
    
    with console.status(f"[bold green]Loading PDF: {input_file}"):
        editor = PDFEditor()
        if not editor.load(str(input_file)):
            console.print(f"[red]Error: Could not load PDF file[/red]")
            raise typer.Exit(1)
    
    # Search for text
    results = editor.search_text(search_text, case_sensitive, regex)
    
    if not results:
        console.print(f"[yellow]No instances of '{search_text}' found[/yellow]")
        return
    
    # Display results
    table = Table(title=f"Search Results: '{search_text}'")
    table.add_column("Page", justify="right", style="cyan")
    table.add_column("Text", style="magenta", max_width=60)
    table.add_column("Font", style="blue")
    table.add_column("Size", justify="right", style="green")
    table.add_column("Position", style="yellow")
    
    for instance in results:
        table.add_row(
            str(instance.page_num + 1),
            instance.text[:57] + "..." if len(instance.text) > 60 else instance.text,
            instance.font,
            f"{instance.fontsize:.1f}",
            f"({instance.rect.x0:.1f}, {instance.rect.y0:.1f})"
        )
    
    console.print(table)
    console.print(f"\n[green]Found {len(results)} instances[/green]")
    
    editor.close()


@app.command()
def info(
    input_file: Path = typer.Argument(..., help="Input PDF file")
):
    """Display information about a PDF file"""
    
    if not input_file.exists():
        console.print(f"[red]Error: Input file '{input_file}' not found[/red]")
        raise typer.Exit(1)
    
    with console.status(f"[bold green]Analyzing PDF: {input_file}"):
        editor = PDFEditor()
        if not editor.load(str(input_file)):
            console.print(f"[red]Error: Could not load PDF file[/red]")
            raise typer.Exit(1)
        
        info = editor.get_document_info()
    
    # Display document information
    table = Table(title=f"PDF Information: {input_file.name}")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Pages", str(info["page_count"]))
    table.add_row("Text Instances", str(info["text_instances"]))
    table.add_row("File Size", f"{info['file_size']:,} bytes")
    
    # Add metadata if available
    if info.get("metadata"):
        for key, value in info["metadata"].items():
            if value:
                table.add_row(f"Meta: {key}", str(value)[:50])
    
    console.print(table)
    editor.close()


@app.command()
def create_sample_config():
    """Create a sample batch replacements JSON file"""
    
    sample_config = [
        {
            "search": "Old Company Name",
            "replace": "New Company Name",
            "case_sensitive": False
        },
        {
            "search": "2023",
            "replace": "2024",
            "case_sensitive": False
        },
        {
            "search": "John Doe",
            "replace": "Jane Smith",
            "case_sensitive": True
        }
    ]
    
    config_file = Path("sample_replacements.json")
    
    with open(config_file, 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    console.print(f"[green]Sample configuration created: {config_file}[/green]")
    console.print("\nEdit this file with your replacements and use with:")
    console.print("[cyan]pdf-editor batch input.pdf sample_replacements.json[/cyan]")


@app.command()
def tui():
    """Launch the Terminal User Interface"""
    try:
        from tui import PDFEditorTUI
        app_tui = PDFEditorTUI()
        app_tui.run()
    except ImportError:
        console.print("[red]TUI not available. Install textual: pip install textual[/red]")
        raise typer.Exit(1)


@app.command()
def gui():
    """Launch the Graphical User Interface"""
    try:
        from gui import PDFEditorGUI
        app_gui = PDFEditorGUI()
        app_gui.run()
    except ImportError:
        console.print("[red]GUI not available. Install required packages[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
