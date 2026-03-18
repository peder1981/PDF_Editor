#!/usr/bin/env python3
"""
PDF Editor - Unified GUI Application
Interface gráfica unificada, robusta e intuitiva
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.font import Font
import threading
import os
from pathlib import Path
from typing import Optional, List, Dict
import json

import sys
sys.path.insert(0, str(Path(__file__).parent / "core"))

from pdf_editor import PDFEditor, EditOperation
from batch_processor import BatchProcessor


class PDFEditorUnifiedGUI:
    """GUI unificada para edição de PDFs"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Editor - Interface Unificada")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Variáveis de estado
        self.source_mode = tk.StringVar(value="single")  # "single" ou "batch"
        self.source_path = tk.StringVar()
        self.dest_path = tk.StringVar()
        self.pdf_editor: Optional[PDFEditor] = None
        self.replacements: List[Dict] = []
        
        self._setup_ui()
        self._setup_styles()
    
    def _setup_styles(self):
        """Configurar estilos visuais"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores do tema
        self.primary_color = "#2196F3"
        self.secondary_color = "#4CAF50"
        self.warning_color = "#FF9800"
        self.error_color = "#f44336"
        
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
    
    def _setup_ui(self):
        """Configurar interface do usuário"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="📄 PDF Editor - Edição de Texto em PDFs", 
                             style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # === SEÇÃO DE ORIGEM ===
        source_frame = ttk.LabelFrame(main_frame, text="📁 Origem", padding=10)
        source_frame.grid(row=1, column=0, sticky="ew", pady=5)
        source_frame.columnconfigure(1, weight=1)
        
        # Modo de origem
        ttk.Radiobutton(source_frame, text="Arquivo único", variable=self.source_mode, 
                       value="single", command=self._update_source_ui).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(source_frame, text="Processamento em lote (diretório)", 
                       variable=self.source_mode, value="batch", 
                       command=self._update_source_ui).grid(row=0, column=1, sticky="w")
        
        # Seleção de arquivo/diretório
        ttk.Label(source_frame, text="Caminho:").grid(row=1, column=0, sticky="w", pady=5)
        source_entry_frame = ttk.Frame(source_frame)
        source_entry_frame.grid(row=1, column=1, sticky="ew", padx=5)
        source_entry_frame.columnconfigure(0, weight=1)
        
        self.source_entry = ttk.Entry(source_entry_frame, textvariable=self.source_path)
        self.source_entry.grid(row=0, column=0, sticky="ew")
        
        self.browse_source_btn = ttk.Button(source_entry_frame, text="🔍 Procurar", 
                                            command=self._browse_source)
        self.browse_source_btn.grid(row=0, column=1, padx=(5, 0))
        
        # === SEÇÃO DE DESTINO ===
        dest_frame = ttk.LabelFrame(main_frame, text="💾 Destino", padding=10)
        dest_frame.grid(row=2, column=0, sticky="ew", pady=5)
        dest_frame.columnconfigure(1, weight=1)
        
        ttk.Label(dest_frame, text="Pasta de saída:").grid(row=0, column=0, sticky="w")
        dest_entry_frame = ttk.Frame(dest_frame)
        dest_entry_frame.grid(row=0, column=1, sticky="ew", padx=5)
        dest_entry_frame.columnconfigure(0, weight=1)
        
        self.dest_entry = ttk.Entry(dest_entry_frame, textvariable=self.dest_path)
        self.dest_entry.grid(row=0, column=0, sticky="ew")
        
        ttk.Button(dest_entry_frame, text="🔍 Procurar", 
                  command=self._browse_dest).grid(row=0, column=1, padx=(5, 0))
        
        # === SEÇÃO DE SUBSTITUIÇÕES ===
        replace_frame = ttk.LabelFrame(main_frame, text="✏️ Substituições de Texto", padding=10)
        replace_frame.grid(row=3, column=0, sticky="ew", pady=5)
        replace_frame.columnconfigure(0, weight=1)
        
        # Frame para adicionar substituições
        add_frame = ttk.Frame(replace_frame)
        add_frame.grid(row=0, column=0, sticky="ew", pady=5)
        add_frame.columnconfigure(1, weight=1)
        add_frame.columnconfigure(3, weight=1)
        
        ttk.Label(add_frame, text="Buscar:").grid(row=0, column=0, sticky="w")
        self.search_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.search_var).grid(row=0, column=1, sticky="ew", padx=5)
        
        ttk.Label(add_frame, text="Substituir por:").grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.replace_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.replace_var).grid(row=0, column=3, sticky="ew", padx=5)
        
        ttk.Button(add_frame, text="➕ Adicionar", command=self._add_replacement).grid(row=0, column=4, padx=(5, 0))
        
        # Lista de substituições
        self.replacements_listbox = tk.Listbox(replace_frame, height=4)
        self.replacements_listbox.grid(row=1, column=0, sticky="ew", pady=5)
        
        scrollbar = ttk.Scrollbar(replace_frame, orient="vertical", 
                                 command=self.replacements_listbox.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.replacements_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Botões de gerenciamento
        btn_frame = ttk.Frame(replace_frame)
        btn_frame.grid(row=2, column=0, sticky="ew")
        
        ttk.Button(btn_frame, text="🗑️ Remover selecionado", 
                  command=self._remove_replacement).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="🗑️ Limpar todos", 
                  command=self._clear_replacements).pack(side="left")
        
        # === OPÇÕES ===
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Opções", padding=10)
        options_frame.grid(row=4, column=0, sticky="ew", pady=5)
        
        self.method_var = tk.StringVar(value="exact")
        ttk.Label(options_frame, text="Método:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(options_frame, textvariable=self.method_var, 
                    values=["exact", "comprehensive", "structure", "smart", "heuristic", "integral", "template", "layout-preserving", "background-preserving"], 
                    state="readonly", width=25).grid(row=0, column=1, sticky="w", padx=5)
        
        self.case_sensitive_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Diferenciar maiúsculas/minúsculas", 
                       variable=self.case_sensitive_var).grid(row=0, column=2, padx=(20, 0))
        
        # === BOTÕES DE AÇÃO ===
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=5, column=0, pady=20)
        
        self.process_btn = ttk.Button(action_frame, text="🚀 Processar PDF(s)", 
                                     command=self._process, style='Action.TButton')
        self.process_btn.pack(side="left", padx=5)
        
        ttk.Button(action_frame, text="📊 Visualizar PDF", 
                  command=self._preview_pdf).pack(side="left", padx=5)
        
        ttk.Button(action_frame, text="❌ Sair", 
                  command=self.root.quit).pack(side="left", padx=5)
        
        # === ÁREA DE LOG ===
        log_frame = ttk.LabelFrame(main_frame, text="📋 Log de Operações", padding=5)
        log_frame.grid(row=6, column=0, sticky="nsew", pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, state='disabled')
        self.log_text.grid(row=0, column=0, sticky="nsew")
        
        # Barra de status
        self.status_var = tk.StringVar(value="Pronto para iniciar")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief='sunken', anchor='w')
        status_bar.grid(row=7, column=0, sticky="ew", pady=(5, 0))
    
    def _log(self, message: str):
        """Adiciona mensagem ao log"""
        self.log_text.config(state='normal')
        self.log_text.insert('end', f"{message}\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')
    
    def _update_source_ui(self):
        """Atualiza interface baseada no modo de origem"""
        mode = self.source_mode.get()
        if mode == "single":
            self.browse_source_btn.config(text="📄 Selecionar PDF")
        else:
            self.browse_source_btn.config(text="📁 Selecionar Pasta")
    
    def _browse_source(self):
        """Abre diálogo para seleção de origem"""
        mode = self.source_mode.get()
        
        if mode == "single":
            path = filedialog.askopenfilename(
                title="Selecionar PDF",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
        else:
            path = filedialog.askdirectory(title="Selecionar Pasta com PDFs")
        
        if path:
            self.source_path.set(path)
            self._log(f"📁 Origem selecionada: {path}")
            
            # Sugerir destino automaticamente
            if not self.dest_path.get():
                if mode == "single":
                    suggested_dest = str(Path(path).parent)
                else:
                    suggested_dest = str(Path(path) / "output")
                self.dest_path.set(suggested_dest)
    
    def _browse_dest(self):
        """Abre diálogo para seleção de destino"""
        path = filedialog.askdirectory(title="Selecionar Pasta de Destino")
        if path:
            self.dest_path.set(path)
            self._log(f"💾 Destino selecionado: {path}")
    
    def _add_replacement(self):
        """Adiciona uma substituição à lista"""
        search = self.search_var.get().strip()
        replace = self.replace_var.get().strip()
        
        if not search:
            messagebox.showwarning("Aviso", "Digite o texto a ser buscado")
            return
        
        replacement = {"search": search, "replace": replace}
        self.replacements.append(replacement)
        
        display_text = f"'{search}' → '{replace}'"
        self.replacements_listbox.insert('end', display_text)
        
        self._log(f"➕ Adicionada substituição: {display_text}")
        
        # Limpar campos
        self.search_var.set("")
        self.replace_var.set("")
    
    def _remove_replacement(self):
        """Remove a substituição selecionada"""
        selection = self.replacements_listbox.curselection()
        if selection:
            index = selection[0]
            removed = self.replacements.pop(index)
            self.replacements_listbox.delete(index)
            self._log(f"🗑️ Removida substituição: '{removed['search']}' → '{removed['replace']}'")
    
    def _clear_replacements(self):
        """Limpa todas as substituições"""
        self.replacements.clear()
        self.replacements_listbox.delete(0, 'end')
        self._log("🗑️ Todas as substituições removidas")
    
    def _validate_inputs(self) -> bool:
        """Valida entradas do usuário"""
        if not self.source_path.get():
            messagebox.showerror("Erro", "Selecione a origem (arquivo ou pasta)")
            return False
        
        if not self.dest_path.get():
            messagebox.showerror("Erro", "Selecione o destino")
            return False
        
        if not self.replacements:
            messagebox.showerror("Erro", "Adicione pelo menos uma substituição")
            return False
        
        if not os.path.exists(self.source_path.get()):
            messagebox.showerror("Erro", "Origem não existe")
            return False
        
        return True
    
    def _process(self):
        """Processa o(s) PDF(s)"""
        if not self._validate_inputs():
            return
        
        # Confirmar operação
        count = len(self.replacements)
        mode_text = "arquivo" if self.source_mode.get() == "single" else "pasta"
        
        if not messagebox.askyesno("Confirmar", 
                                  f"Processar {mode_text} com {count} substituições?"):
            return
        
        # Executar em thread separada
        thread = threading.Thread(target=self._process_thread)
        thread.daemon = True
        thread.start()
    
    def _process_thread(self):
        """Thread de processamento"""
        try:
            self.process_btn.config(state='disabled')
            self.status_var.set("Processando...")
            
            source = self.source_path.get()
            dest = self.dest_path.get()
            method = self.method_var.get()
            case_sensitive = self.case_sensitive_var.get()
            
            self._log(f"🚀 Iniciando processamento...")
            self._log(f"📁 Origem: {source}")
            self._log(f"💾 Destino: {dest}")
            self._log(f"🔧 Método: {method}")
            
            if self.source_mode.get() == "single":
                self._process_single(source, dest, method, case_sensitive)
            else:
                self._process_batch(source, dest, method, case_sensitive)
            
            self.status_var.set("Processamento concluído!")
            messagebox.showinfo("Sucesso", "Processamento concluído com sucesso!")
            
        except Exception as e:
            self._log(f"❌ Erro: {str(e)}")
            self.status_var.set("Erro no processamento")
            messagebox.showerror("Erro", f"Falha no processamento:\n{str(e)}")
        
        finally:
            self.process_btn.config(state='normal')
    
    def _process_single(self, source: str, dest: str, method: str, case_sensitive: bool):
        """Processa arquivo único"""
        self._log("📄 Processando arquivo único...")
        
        editor = PDFEditor()
        
        if not editor.load(source):
            raise Exception("Falha ao carregar PDF")
        
        self._log(f"✅ PDF carregado: {len(editor.text_instances)} instâncias de texto")
        
        # Aplicar substituições
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
        
        # Salvar resultado
        output_file = Path(dest) / f"{Path(source).stem}_edited.pdf"
        os.makedirs(dest, exist_ok=True)
        
        if editor.save(str(output_file)):
            self._log(f"✅ Arquivo salvo: {output_file}")
        else:
            raise Exception("Falha ao salvar arquivo")
        
        editor.close()
    
    def _process_batch(self, source: str, dest: str, method: str, case_sensitive: bool):
        """Processamento em lote"""
        self._log("📁 Iniciando processamento em lote...")
        
        processor = BatchProcessor(max_workers=4)
        
        # Criar operações
        operations = []
        for rep in self.replacements:
            operations.append(EditOperation(
                search_text=rep["search"],
                replace_text=rep["replace"],
                case_sensitive=case_sensitive
            ))
        
        # Processar diretório
        jobs_added = processor.process_directory(
            input_dir=source,
            output_dir=dest,
            operations=operations,
            method=method
        )
        
        self._log(f"📊 {jobs_added} arquivos adicionados à fila")
        
        # Executar processamento
        results = processor.process_jobs()
        
        self._log(f"✅ Concluído: {results['completed']} de {results['total']} arquivos")
        if results['failed'] > 0:
            self._log(f"❌ Falhas: {results['failed']} arquivos")
        
        self._log(f"📊 Total de substituições: {results['total_replacements']}")
    
    def _preview_pdf(self):
        """Visualiza informações do PDF"""
        source = self.source_path.get()
        if not source or not os.path.exists(source):
            messagebox.showwarning("Aviso", "Selecione um arquivo PDF válido")
            return
        
        if os.path.isdir(source):
            messagebox.showwarning("Aviso", "Visualização disponível apenas para arquivos únicos")
            return
        
        try:
            editor = PDFEditor()
            if editor.load(source):
                info = editor.get_document_info()
                
                info_text = f"""📄 Informações do PDF:

📊 Páginas: {info['page_count']}
📝 Instâncias de texto: {info['text_instances']}
💾 Tamanho do arquivo: {info['file_size']:,} bytes

📋 Metadados:
"""
                if info.get('metadata'):
                    for key, value in info['metadata'].items():
                        if value:
                            info_text += f"  • {key}: {value}\n"
                
                messagebox.showinfo("Informações do PDF", info_text)
                editor.close()
            else:
                messagebox.showerror("Erro", "Falha ao carregar PDF")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na visualização:\n{str(e)}")
    
    def run(self):
        """Inicia a aplicação"""
        self._log("🚀 PDF Editor - Interface Unificada iniciada")
        self._log("📖 Selecione a origem, destino e adicione substituições")
        self.root.mainloop()


def main():
    """Função principal"""
    app = PDFEditorUnifiedGUI()
    app.run()


if __name__ == "__main__":
    main()
