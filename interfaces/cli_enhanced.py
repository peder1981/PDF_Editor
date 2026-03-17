#!/usr/bin/env python3
"""
Advanced PDF Editor - Enhanced CLI with Improved Font Preservation
"""

import typer
from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from improved_pdf_editor import ImprovedPDFEditor

app = typer.Typer(help="Advanced PDF Editor - Enhanced version with improved font preservation")
console = Console()


@app.command()
def replace_enhanced(
    input_file: Path = typer.Argument(..., help="Input PDF file"),
    search_text: str = typer.Argument(..., help="Text to search for"),
    replace_text: str = typer.Argument(..., help="Replacement text"),
    output_file: Optional[Path] = typer.Argument(None, help="Output PDF file"),
    case_sensitive: bool = typer.Option(False, "--case-sensitive", "-c", help="Case sensitive search"),
    preview: bool = typer.Option(False, "--preview", "-p", help="Preview changes before applying")
):
    """Replace text with enhanced font preservation"""
    
    if not input_file.exists():
        console.print(f"[red]Error: Input file '{input_file}' not found[/red]")
        raise typer.Exit(1)
    
    if output_file is None:
        output_file = input_file.parent / f"{input_file.stem}_enhanced{input_file.suffix}"
    
    with console.status(f"[bold green]Loading PDF: {input_file}"):
        editor = ImprovedPDFEditor()
        if not editor.load(str(input_file)):
            console.print(f"[red]Error: Could not load PDF file[/red]")
            raise typer.Exit(1)
    
    # Show font information
    console.print(f"[cyan]Available fonts in document: {len(editor.font_mapping)}[/cyan]")
    if editor.font_mapping:
        font_table = Table(title="Document Fonts")
        font_table.add_column("Font Name", style="green")
        for font in list(editor.font_mapping.keys())[:10]:  # Show first 10 fonts
            font_table.add_row(font)
        if len(editor.font_mapping) > 10:
            font_table.add_row("... and more")
        console.print(font_table)
    
    # Preview mode
    if preview:
        search_results = editor.search_text(search_text, case_sensitive)
        if not search_results:
            console.print(f"[yellow]No instances of '{search_text}' found[/yellow]")
            return
        
        table = Table(title=f"Preview: '{search_text}' → '{replace_text}' (Enhanced)")
        table.add_column("Page", justify="right", style="cyan")
        table.add_column("Text", style="magenta", max_width=40)
        table.add_column("Font", style="blue")
        table.add_column("Size", justify="right", style="green")
        table.add_column("Position", style="yellow")
        
        for instance in search_results:
            table.add_row(
                str(instance.page_num + 1),
                instance.text[:37] + "..." if len(instance.text) > 40 else instance.text,
                instance.font,
                f"{instance.fontsize:.1f}",
                f"({instance.rect.x0:.1f}, {instance.rect.y0:.1f})"
            )
        
        console.print(table)
        
        if not typer.confirm(f"Apply {len(search_results)} replacements with enhanced font preservation?"):
            console.print("[yellow]Operation cancelled[/yellow]")
            return
    
    # Perform enhanced replacement
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Replacing text with enhanced font preservation...", total=None)
        
        replacements = editor.replace_text_enhanced(search_text, replace_text, case_sensitive)
        
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
        f"🔧 Method used: [yellow]enhanced font preservation[/yellow]\n"
        f"🎨 Font matching: [blue]improved algorithm[/blue]",
        title="Enhanced Operation Complete",
        border_style="green"
    ))


@app.command()
def analyze_fonts(
    input_file: Path = typer.Argument(..., help="Input PDF file")
):
    """Analyze fonts used in a PDF document"""
    
    if not input_file.exists():
        console.print(f"[red]Error: Input file '{input_file}' not found[/red]")
        raise typer.Exit(1)
    
    with console.status(f"[bold green]Analyzing PDF: {input_file}"):
        editor = ImprovedPDFEditor()
        if not editor.load(str(input_file)):
            console.print(f"[red]Error: Could not load PDF file[/red]")
            raise typer.Exit(1)
    
    # Display font analysis
    console.print(f"\n[bold]Font Analysis for: {input_file.name}[/bold]")
    
    # Font mapping table
    if editor.font_mapping:
        font_table = Table(title="Available Fonts")
        font_table.add_column("Font Name", style="green")
        font_table.add_column("Type", style="blue")
        
        for font_name in editor.font_mapping.keys():
            font_type = "System" if font_name in ["helv", "times", "cour"] else "Embedded"
            font_table.add_row(font_name, font_type)
        
        console.print(font_table)
    
    # Text instances by font
    font_usage = {}
    for instance in editor.text_instances:
        font = instance.font
        if font not in font_usage:
            font_usage[font] = []
        font_usage[font].append(instance)
    
    usage_table = Table(title="Font Usage Statistics")
    usage_table.add_column("Font", style="cyan")
    usage_table.add_column("Instances", justify="right", style="green")
    usage_table.add_column("Avg Size", justify="right", style="yellow")
    
    for font, instances in font_usage.items():
        avg_size = sum(inst.fontsize for inst in instances) / len(instances)
        usage_table.add_row(font, str(len(instances)), f"{avg_size:.1f}")
    
    console.print(usage_table)
    
    editor.close()


@app.command()
def test_enhanced(
    input_file: Path = typer.Argument(..., help="Input PDF file"),
    search_text: str = typer.Argument(..., help="Text to search for"),
    replace_text: str = typer.Argument(..., help="Replacement text")
):
    """Test enhanced font preservation on the user's PDF"""
    
    if not input_file.exists():
        console.print(f"[red]Error: Input file '{input_file}' not found[/red]")
        raise typer.Exit(1)
    
    output_file = input_file.parent / f"{input_file.stem}_test_enhanced.pdf"
    
    console.print("[bold blue]Testing Enhanced Font Preservation[/bold blue]")
    console.print(f"Input: {input_file}")
    console.print(f"Output: {output_file}")
    console.print(f"Search: '{search_text}' → '{replace_text}'")
    console.print()
    
    with console.status("[bold green]Loading and analyzing PDF..."):
        editor = ImprovedPDFEditor()
        if not editor.load(str(input_file)):
            console.print(f"[red]Error: Could not load PDF file[/red]")
            raise typer.Exit(1)
    
    # Show document analysis
    console.print(f"[cyan]Document loaded successfully![/cyan]")
    console.print(f"Pages: {len(editor.document)}")
    console.print(f"Text instances: {len(editor.text_instances)}")
    console.print(f"Available fonts: {len(editor.font_mapping)}")
    
    # Search for target text
    search_results = editor.search_text(search_text, case_sensitive=False)
    
    if not search_results:
        console.print(f"[yellow]No instances of '{search_text}' found[/yellow]")
        editor.close()
        return
    
    console.print(f"[green]Found {len(search_results)} instances to replace[/green]")
    
    # Show detailed analysis of found text
    for i, instance in enumerate(search_results, 1):
        console.print(f"\nInstance {i}:")
        console.print(f"  Text: '{instance.text}'")
        console.print(f"  Font: {instance.font}")
        console.print(f"  Size: {instance.fontsize}")
        console.print(f"  Position: ({instance.rect.x0:.1f}, {instance.rect.y0:.1f})")
        
        # Show font matching
        best_font = editor._get_best_font_match(instance.font)
        adjusted_size = editor._calculate_adjusted_fontsize(
            instance.fontsize, instance.font, best_font, 
            len(search_text), len(replace_text)
        )
        console.print(f"  → Will use font: {best_font}")
        console.print(f"  → Adjusted size: {adjusted_size:.1f}")
    
    # Confirm replacement
    if not typer.confirm(f"\nProceed with enhanced replacement?"):
        console.print("[yellow]Test cancelled[/yellow]")
        editor.close()
        return
    
    # Perform replacement
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Applying enhanced font preservation...", total=None)
        
        replacements = editor.replace_text_enhanced(search_text, replace_text, case_sensitive=False)
        
        progress.update(task, description="Saving test result...")
        
        if editor.save(str(output_file)):
            progress.update(task, description="Test complete!")
        else:
            console.print("[red]Error: Could not save test file[/red]")
            raise typer.Exit(1)
    
    editor.close()
    
    console.print(Panel(
        f"🧪 Test completed successfully!\n"
        f"✅ Replaced [cyan]{replacements}[/cyan] instances\n"
        f"📄 Test result saved to: [green]{output_file}[/green]\n"
        f"🔍 Compare with original to verify font preservation\n"
        f"💡 If satisfied, use this enhanced version for production",
        title="Enhanced Font Preservation Test",
        border_style="blue"
    ))


if __name__ == "__main__":
    app()
