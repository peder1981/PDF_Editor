#!/usr/bin/env python3
"""
Editor de PDF — Ponto de entrada

Inicia a interface gráfica diretamente.
Para CLI, use: python -m interfaces.cli --help
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from unified_gui import EditorPDFGUI


def main():
    app = EditorPDFGUI()
    app.run()


if __name__ == "__main__":
    main()
