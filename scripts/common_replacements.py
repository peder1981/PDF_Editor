#!/usr/bin/env python3
"""Ferramenta para substituições comuns em certificados PDF.

Este script automatiza casos recorrentes (nome, data, idade, atividade)
utilizando o PDFEditor principal. É possível combinar argumentos rápidos
com arquivos de configuração JSON para cenários personalizados.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable, List

# Permite importar core.pdf_editor quando o script for executado diretamente
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from core.pdf_editor import PDFEditor, EditOperation  # noqa: E402

DEFAULT_FIELDS = {
    "name": {
        "search": "Marcelo de Freitas Ferreira",
        "help": "Novo nome do paciente"
    },
    "birthdate": {
        "search": "nascido em 19 de agosto de 1979",
        "help": "Texto completo da data de nascimento"
    },
    "age": {
        "search": "46 anos de idade",
        "help": "Texto contendo a idade a ser atualizada"
    },
    "issue_date": {
        "search": "Niterói, 28 de janeiro de 2026.",
        "help": "Linha de data e local"
    },
    "activity": {
        "search": "atividades físicas sem",
        "help": "Trecho da atividade (permite acrescentar por ex. (jiu-jitsu))"
    }
}

SUPPORTED_METHODS = {
    "exact": lambda editor, op: editor.replace_text_exact(op.search_text, op.replace_text, op.case_sensitive),
    "layout-preserving": lambda editor, op: editor.replace_text_layout_preserving(op.search_text, op.replace_text, op.case_sensitive),
    "background-preserving": lambda editor, op: editor.replace_text_background_preserving(op.search_text, op.replace_text, op.case_sensitive)
}


def load_operations_from_config(config_path: Path) -> List[EditOperation]:
    data = json.loads(config_path.read_text(encoding="utf-8"))
    operations = []
    for entry in data.get("operations", []):
        operations.append(
            EditOperation(
                search_text=entry["search"],
                replace_text=entry["replace"],
                case_sensitive=entry.get("case_sensitive", False),
                regex=entry.get("regex", False)
            )
        )
    return operations


def build_operations_from_args(args: argparse.Namespace) -> List[EditOperation]:
    operations: List[EditOperation] = []
    for field, meta in DEFAULT_FIELDS.items():
        value = getattr(args, field)
        if value:
            search = getattr(args, f"{field}_search") or meta["search"]
            operations.append(EditOperation(search_text=search, replace_text=value, case_sensitive=args.case_sensitive))
    return operations


def execute_operations(editor: PDFEditor, operations: Iterable[EditOperation], method: str) -> int:
    if method not in SUPPORTED_METHODS:
        raise ValueError(f"Método não suportado: {method}")
    total = 0
    for operation in operations:
        replacements = SUPPORTED_METHODS[method](editor, operation)
        total += replacements
        print(f"→ {operation.search_text!r} → {operation.replace_text!r}: {replacements} ocorrência(s)")
    return total


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Substituições guiadas para certificados PDF")
    parser.add_argument("input_pdf", type=Path, help="PDF de entrada")
    parser.add_argument("output_pdf", type=Path, help="PDF de saída")
    parser.add_argument("--method", choices=SUPPORTED_METHODS.keys(), default="exact", help="Método de substituição")
    parser.add_argument("--config", type=Path, help="Arquivo JSON com operações personalizadas")
    parser.add_argument("--case-sensitive", action="store_true", help="Força busca case sensitive nas substituições rápidas")

    for field, meta in DEFAULT_FIELDS.items():
        parser.add_argument(f"--{field}", help=meta["help"])
        parser.add_argument(
            f"--{field}-search",
            dest=f"{field}_search",
            help=f"Texto original a ser buscado (default: {meta['search']!r})"
        )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    operations = build_operations_from_args(args)

    if args.config:
        if not args.config.exists():
            raise SystemExit(f"Config não encontrada: {args.config}")
        operations.extend(load_operations_from_config(args.config))

    if not operations:
        raise SystemExit("Nenhuma substituição informada. Use --name, --issue-date etc. ou --config.")

    editor = PDFEditor()
    if not editor.load(str(args.input_pdf)):
        raise SystemExit(f"Não foi possível abrir {args.input_pdf}")

    total = execute_operations(editor, operations, args.method)

    if total == 0:
        print("⚠️ Nenhuma ocorrência encontrada. Verifique os textos originais.")

    if editor.save(str(args.output_pdf)):
        print(f"✅ PDF salvo em {args.output_pdf}")
    else:
        raise SystemExit("Falha ao salvar PDF de saída")

    editor.close()


if __name__ == "__main__":
    main()
