#!/usr/bin/env python3
"""
Editor de PDF — Interface Gráfica Simples

Fluxo do usuário:
  1. Selecionar o PDF
  2. Dizer o que deve ser alterado (buscar → substituir)
  3. Visualizar como ficou
  4. Confirmar e salvar

Menos é mais.
"""

import os
import sys
import tempfile
import threading
from pathlib import Path
from typing import Optional

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

sys.path.insert(0, str(Path(__file__).parent / "core"))

from pdf_editor import PDFEditor
from method_dispatch import apply_replacement


class EditorPDFGUI:
    """Interface gráfica simples para edição de PDF.

    4 passos: selecionar → alterar → visualizar → confirmar.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Editor de PDF")
        self.root.geometry("720x560")
        self.root.minsize(600, 480)
        self.root.resizable(True, True)

        # Estado
        self.pdf_editor: Optional[PDFEditor] = None
        self.caminho_pdf: str = ""
        self.caminho_saida: str = ""
        self.preview_path: str = ""

        self._construir_ui()

    # --- UI ---

    def _construir_ui(self):
        """Constrói toda a interface em uma única janela."""
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(4, weight=1)

        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Passo 1: Selecionar PDF
        passo1 = ttk.LabelFrame(self.root, text="1. Selecionar o PDF", padding=12)
        passo1.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        passo1.columnconfigure(0, weight=1)

        self.lbl_pdf = ttk.Label(passo1, text="Nenhum PDF selecionado", foreground="gray")
        self.lbl_pdf.grid(row=0, column=0, sticky="w")

        ttk.Button(passo1, text="Procurar PDF...", command=self._selecionar_pdf).grid(
            row=0, column=1, padx=(10, 0)
        )

        # Passo 2: O que alterar
        passo2 = ttk.LabelFrame(self.root, text="2. O que deve ser alterado", padding=12)
        passo2.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        passo2.columnconfigure(1, weight=1)

        ttk.Label(passo2, text="Buscar:").grid(row=0, column=0, sticky="w", pady=2)
        self.var_busca = tk.StringVar()
        ttk.Entry(passo2, textvariable=self.var_busca).grid(
            row=0, column=1, sticky="ew", padx=(5, 0), pady=2
        )

        ttk.Label(passo2, text="Substituir por:").grid(row=1, column=0, sticky="w", pady=2)
        self.var_substituir = tk.StringVar()
        ttk.Entry(passo2, textvariable=self.var_substituir).grid(
            row=1, column=1, sticky="ew", padx=(5, 0), pady=2
        )

        # Opção de método (simples, padrão = exato)
        linha_opcoes = ttk.Frame(passo2)
        linha_opcoes.grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))

        ttk.Label(linha_opcoes, text="Método:").pack(side="left")
        self.var_metodo = tk.StringVar(value="exact")
        ttk.Combobox(
            linha_opcoes,
            textvariable=self.var_metodo,
            values=["exact", "layout-preserving", "background-preserving"],
            state="readonly",
            width=22,
        ).pack(side="left", padx=(5, 15))

        self.var_case = tk.BooleanVar()
        ttk.Checkbutton(
            linha_opcoes, text="Diferenciar maiúsculas/minúsculas", variable=self.var_case
        ).pack(side="left")

        # Passo 3: Visualizar
        passo3 = ttk.LabelFrame(self.root, text="3. Visualizar como ficou", padding=12)
        passo3.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        passo3.columnconfigure(0, weight=1)

        self.lbl_preview = ttk.Label(
            passo3,
            text="Clique em 'Visualizar' após preencher os campos acima.",
            foreground="gray",
        )
        self.lbl_preview.grid(row=0, column=0, sticky="w")

        ttk.Button(passo3, text="Visualizar alteração", command=self._visualizar).grid(
            row=0, column=1, padx=(10, 0)
        )

        # Passo 4: Confirmar
        passo4 = ttk.LabelFrame(self.root, text="4. Confirmar e salvar", padding=12)
        passo4.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        passo4.columnconfigure(0, weight=1)

        self.lbl_saida = ttk.Label(passo4, text="Arquivo de saída não definido", foreground="gray")
        self.lbl_saida.grid(row=0, column=0, sticky="w")

        botoes = ttk.Frame(passo4)
        botoes.grid(row=0, column=1, padx=(10, 0))
        ttk.Button(botoes, text="Escolher onde salvar...", command=self._escolher_saida).pack(
            side="left", padx=(0, 5)
        )
        self.btn_salvar = ttk.Button(
            botoes, text="Confirmar e Salvar", command=self._confirmar, state="disabled"
        )
        self.btn_salvar.pack(side="left")

        # Log
        frame_log = ttk.LabelFrame(self.root, text="Registro", padding=8)
        frame_log.grid(row=4, column=0, sticky="nsew", padx=10, pady=(5, 10))
        frame_log.columnconfigure(0, weight=1)
        frame_log.rowconfigure(0, weight=1)

        self.log = scrolledtext.ScrolledText(frame_log, height=6, state="disabled", font=("Courier", 9))
        self.log.grid(row=0, column=0, sticky="nsew")

    # --- Ações ---

    def _registrar(self, msg: str):
        """Adiciona uma linha ao registro (thread-safe)."""
        def _escrever():
            self.log.config(state="normal")
            self.log.insert("end", f"{msg}\n")
            self.log.see("end")
            self.log.config(state="disabled")
        self.root.after(0, _escrever)

    def _selecionar_pdf(self):
        """Passo 1: usuário escolhe o PDF de entrada."""
        caminho = filedialog.askopenfilename(
            title="Selecionar PDF",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")],
        )
        if not caminho:
            return

        self.caminho_pdf = caminho
        nome = Path(caminho).name
        self.lbl_pdf.config(text=f"📄 {nome}", foreground="black")
        self._registrar(f"PDF selecionado: {nome}")

        # Sugerir nome de saída
        sugerido = str(Path(caminho).parent / f"{Path(caminho).stem}_alterado.pdf")
        self.caminho_saida = sugerido
        self.lbl_saida.config(text=f"💾 {Path(sugerido).name}", foreground="black")

        # Carregar PDF em background
        def carregar():
            try:
                if self.pdf_editor:
                    self.pdf_editor.close()
                self.pdf_editor = PDFEditor()
                if self.pdf_editor.load(caminho):
                    info = self.pdf_editor.get_document_info()
                    self._registrar(
                        f"PDF carregado: {info['page_count']} páginas, "
                        f"{info['text_instances']} instâncias de texto"
                    )
                else:
                    self._registrar("❌ Não foi possível carregar o PDF")
                    self.root.after(0, lambda: messagebox.showerror("Erro", "Não foi possível carregar o PDF"))
            except Exception as e:
                self._registrar(f"❌ Erro ao carregar: {e}")

        threading.Thread(target=carregar, daemon=True).start()

    def _visualizar(self):
        """Passo 3: gera um preview temporário e abre no visualizador do sistema."""
        if not self._validar_entradas():
            return
        if not self.pdf_editor or not self.pdf_editor.document:
            messagebox.showwarning("Aviso", "Selecione um PDF primeiro (Passo 1).")
            return

        busca = self.var_busca.get().strip()
        substituir = self.var_substituir.get()

        # Procurar ocorrências antes de substituir
        resultados = self.pdf_editor.search_text(busca, self.var_case.get())
        if not resultados:
            messagebox.showinfo("Visualização", f"Nenhuma ocorrência de '{busca}' encontrada no PDF.")
            return

        self._registrar(f"Encontradas {len(resultados)} ocorrências de '{busca}'")

        # Gerar preview em arquivo temporário
        def gerar_preview():
            try:
                # Criar cópia temporária e aplicar substituição
                preview_dir = tempfile.mkdtemp(prefix="pdf_preview_")
                self.preview_path = os.path.join(preview_dir, "preview.pdf")

                # Salvar cópia do estado atual
                if not self.pdf_editor.save(self.preview_path):
                    self._registrar("❌ Falha ao gerar preview")
                    return

                # Abrir preview no visualizador do sistema
                self._abrir_visualizador(self.preview_path)
                self._registrar("Preview gerado e aberto no visualizador")

                # Habilitar botão de salvar
                self.root.after(0, lambda: self.btn_salvar.config(state="normal"))

            except Exception as e:
                self._registrar(f"❌ Erro no preview: {e}")

        threading.Thread(target=gerar_preview, daemon=True).start()

    def _abrir_visualizador(self, caminho: str):
        """Abre o PDF no visualizador padrão do sistema."""
        import subprocess
        import platform

        sistema = platform.system()
        try:
            if sistema == "Linux":
                subprocess.Popen(["xdg-open", caminho])
            elif sistema == "Darwin":
                subprocess.Popen(["open", caminho])
            elif sistema == "Windows":
                os.startfile(caminho)  # type: ignore
        except Exception:
            self._registrar("⚠️ Não foi possível abrir o visualizador automaticamente.")

    def _escolher_saida(self):
        """Passo 4: usuário escolhe onde salvar."""
        caminho = filedialog.asksaveasfilename(
            title="Salvar PDF alterado como...",
            defaultextension=".pdf",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")],
            initialfile=Path(self.caminho_pdf).stem + "_alterado.pdf" if self.caminho_pdf else None,
        )
        if not caminho:
            return

        self.caminho_saida = caminho
        self.lbl_saida.config(text=f"💾 {Path(caminho).name}", foreground="black")
        self.btn_salvar.config(state="normal")
        self._registrar(f"Saída definida: {Path(caminho).name}")

    def _confirmar(self):
        """Passo 4: aplica a substituição no PDF original e salva."""
        if not self._validar_entradas():
            return
        if not self.caminho_saida:
            messagebox.showwarning("Aviso", "Escolha onde salvar o arquivo (Passo 4).")
            return

        busca = self.var_busca.get().strip()
        substituir = self.var_substituir.get()
        metodo = self.var_metodo.get()
        case = self.var_case.get()

        if not messagebox.askyesno(
            "Confirmar alteração",
            f"Substituir '{busca}' por '{substituir}'?\n\n"
            f"Método: {metodo}\n"
            f"Salvar em: {Path(self.caminho_saida).name}",
        ):
            return

        def salvar():
            try:
                self.root.after(0, lambda: self.btn_salvar.config(state="disabled"))
                self._registrar(f"Aplicando substituição (método: {metodo})...")

                count = apply_replacement(
                    self.pdf_editor, metodo, busca, substituir, case
                )
                self._registrar(f"✅ {count} substituição(ões) realizada(s)")

                if self.pdf_editor.save(self.caminho_saida):
                    self._registrar(f"💾 Arquivo salvo: {self.caminho_saida}")
                    self.root.after(
                        0,
                        lambda: messagebox.showinfo(
                            "Concluído",
                            f"PDF salvo com sucesso!\n\n{count} substituição(ões) realizada(s).\n"
                            f"Arquivo: {self.caminho_saida}",
                        ),
                    )
                else:
                    self._registrar("❌ Falha ao salvar arquivo")
                    self.root.after(
                        0,
                        lambda: messagebox.showerror("Erro", "Falha ao salvar o arquivo."),
                    )

            except Exception as e:
                self._registrar(f"❌ Erro: {e}")
                self.root.after(
                    0, lambda: messagebox.showerror("Erro", f"Falha ao processar:\n{e}")
                )
            finally:
                self.root.after(0, lambda: self.btn_salvar.config(state="normal"))

        threading.Thread(target=salvar, daemon=True).start()

    # --- Validação ---

    def _validar_entradas(self) -> bool:
        """Verifica se os campos obrigatórios estão preenchidos."""
        if not self.var_busca.get().strip():
            messagebox.showwarning("Aviso", "Digite o texto a ser buscado (Passo 2).")
            return False
        if not self.var_substituir.get().strip() and not messagebox.askyesno(
            "Confirmar", "Substituir por texto vazio (apagar)?"
        ):
            return False
        return True

    # --- Iniciar ---

    def run(self):
        """Inicia a aplicação."""
        self._registrar("Editor de PDF iniciado. Comece pelo Passo 1.")
        self.root.mainloop()


def main():
    app = EditorPDFGUI()
    app.run()


if __name__ == "__main__":
    main()
