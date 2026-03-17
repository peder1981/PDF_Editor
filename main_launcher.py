#!/usr/bin/env python3
"""
PDF Editor - Launcher Principal
Permite escolher entre GUI, TUI ou CLI
"""

import argparse
import sys
from pathlib import Path


def show_menu():
    """Exibe menu de seleção de interface"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              📄 PDF EDITOR - EDITOR DE PDFs                  ║
║                                                              ║
║          Edição de texto em PDFs com preservação             ║
║              de estrutura e fontes homogêneas                  ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Escolha a interface desejada:                               ║
║                                                              ║
║  [1] 🖥️  GUI - Interface Gráfica (Recomendado)              ║
║      Ideal para usuários que preferem interface visual         ║
║      com botões, formulários e seleção de arquivos           ║
║                                                              ║
║  [2] 📟 TUI - Interface Terminal                             ║
║      Para usuários que preferem interface no terminal        ║
║      com navegação por teclado e abas                        ║
║                                                              ║
║  [3] ⌨️  CLI - Linha de Comando                              ║
║      Para automação e scripts. Use --help para opções        ║
║                                                              ║
║  [4] ❌ Sair                                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


def launch_gui():
    """Inicia interface gráfica"""
    print("🖥️  Iniciando Interface Gráfica...")
    try:
        from unified_gui import PDFEditorUnifiedGUI
        app = PDFEditorUnifiedGUI()
        app.run()
    except ImportError as e:
        print(f"❌ Erro ao carregar GUI: {e}")
        print("⚠️  Verifique se o tkinter está instalado:")
        print("   Ubuntu/Debian: sudo apt-get install python3-tk")
        print("   CentOS/RHEL: sudo yum install python3-tkinter")
        sys.exit(1)


def launch_tui():
    """Inicia interface de terminal"""
    print("📟 Iniciando Interface Terminal...")
    try:
        from unified_tui import UnifiedTUIMain
        app = UnifiedTUIMain()
        app.run()
    except ImportError as e:
        print(f"❌ Erro ao carregar TUI: {e}")
        print("⚠️  Verifique as dependências:")
        print("   pip install textual")
        sys.exit(1)


def launch_cli():
    """Inicia linha de comando"""
    print("⌨️  Iniciando Interface de Linha de Comando...")
    try:
        # Importa e executa CLI
        sys.path.insert(0, str(Path(__file__).parent / "interfaces"))
        from cli import app
        app()
    except ImportError as e:
        print(f"❌ Erro ao carregar CLI: {e}")
        sys.exit(1)


def main():
    """Função principal do launcher"""
    parser = argparse.ArgumentParser(
        description="PDF Editor - Escolha a interface desejada",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s           # Mostra menu interativo
  %(prog)s --gui     # Inicia diretamente a GUI
  %(prog)s --tui     # Inicia diretamente a TUI
  %(prog)s --cli     # Inicia diretamente a CLI
        """
    )
    
    parser.add_argument(
        "--gui", "-g",
        action="store_true",
        help="Inicia interface gráfica (GUI)"
    )
    
    parser.add_argument(
        "--tui", "-t",
        action="store_true",
        help="Inicia interface de terminal (TUI)"
    )
    
    parser.add_argument(
        "--cli", "-c",
        action="store_true",
        help="Inicia interface de linha de comando (CLI)"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="%(prog)s 1.0.0 - PDF Editor Unificado"
    )
    
    args = parser.parse_args()
    
    # Verificar argumentos de linha de comando
    if args.gui:
        launch_gui()
        return
    
    if args.tui:
        launch_tui()
        return
    
    if args.cli:
        launch_cli()
        return
    
    # Menu interativo
    while True:
        show_menu()
        choice = input("Escolha uma opção [1-4]: ").strip()
        
        if choice == "1":
            launch_gui()
            break
        elif choice == "2":
            launch_tui()
            break
        elif choice == "3":
            launch_cli()
            break
        elif choice == "4":
            print("👋 Até logo!")
            sys.exit(0)
        else:
            print("❌ Opção inválida. Tente novamente.\n")


if __name__ == "__main__":
    main()
