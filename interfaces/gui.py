#!/usr/bin/env python3
"""
Advanced PDF Editor - Graphical User Interface
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.font import Font
import threading
from typing import Optional, List
from pathlib import Path
import json

from pdf_editor import PDFEditor, EditOperation, TextInstance


class PDFEditorGUI:
    """Graphical User Interface for PDF Editor"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.pdf_editor: Optional[PDFEditor] = None
        self.current_file: Optional[str] = None
        self.search_results: List[TextInstance] = []
        
        self._setup_ui()
        self._setup_styles()
    
    def _setup_ui(self):
        """Setup the main UI components"""
        self.root.title("Advanced PDF Editor - Structure Preserving Text Editor")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        
        # Create menu bar
        self._create_menubar()
        
        # Create toolbar
        self._create_toolbar()
        
        # Create main content area
        self._create_main_content()
        
        # Create status bar
        self._create_statusbar()
    
    def _setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Action.TButton', font=('Arial', 9, 'bold'))
        style.configure('Success.TButton', background='#28a745')
        style.configure('Warning.TButton', background='#ffc107')
        style.configure('Danger.TButton', background='#dc3545')
    
    def _create_menubar(self):
        """Create the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open PDF...", command=self._open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save As...", command=self._save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Reload", command=self._reload_file, accelerator="F5")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Search Text...", command=self._search_dialog, accelerator="Ctrl+F")
        edit_menu.add_command(label="Replace Text...", command=self._replace_dialog, accelerator="Ctrl+H")
        edit_menu.add_separator()
        edit_menu.add_command(label="Batch Replace...", command=self._batch_replace_dialog)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Document Info", command=self._show_document_info)
        view_menu.add_command(label="Clear Results", command=self._clear_results)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self._open_file())
        self.root.bind('<Control-s>', lambda e: self._save_file())
        self.root.bind('<Control-f>', lambda e: self._search_dialog())
        self.root.bind('<Control-h>', lambda e: self._replace_dialog())
        self.root.bind('<F5>', lambda e: self._reload_file())
    
    def _create_toolbar(self):
        """Create the toolbar"""
        toolbar_frame = ttk.Frame(self.root)
        toolbar_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # File operations
        ttk.Button(toolbar_frame, text="📁 Open", command=self._open_file, style='Action.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar_frame, text="💾 Save", command=self._save_file, style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(toolbar_frame, orient='vertical').pack(side=tk.LEFT, fill='y', padx=5)
        
        # Search operations
        ttk.Button(toolbar_frame, text="🔍 Search", command=self._search_dialog, style='Action.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar_frame, text="✏️ Replace", command=self._replace_dialog, style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(toolbar_frame, orient='vertical').pack(side=tk.LEFT, fill='y', padx=5)
        
        # Info
        ttk.Button(toolbar_frame, text="📊 Info", command=self._show_document_info).pack(side=tk.LEFT, padx=2)
        
        # File info label (right side)
        self.file_info_label = ttk.Label(toolbar_frame, text="No PDF loaded", font=('Arial', 9, 'italic'))
        self.file_info_label.pack(side=tk.RIGHT, padx=10)
    
    def _create_main_content(self):
        """Create the main content area"""
        # Create paned window for resizable sections
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Left panel - Controls
        self._create_left_panel()
        
        # Right panel - Results and preview
        self._create_right_panel()
    
    def _create_left_panel(self):
        """Create the left control panel"""
        left_frame = ttk.Frame(self.paned_window, width=300)
        self.paned_window.add(left_frame, weight=1)
        
        # Search section
        search_group = ttk.LabelFrame(left_frame, text="Search & Replace", padding=10)
        search_group.pack(fill='x', pady=5)
        
        # Search input
        ttk.Label(search_group, text="Search for:").pack(anchor='w')
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_group, textvariable=self.search_var)
        self.search_entry.pack(fill='x', pady=(0, 5))
        
        # Replace input
        ttk.Label(search_group, text="Replace with:").pack(anchor='w')
        self.replace_var = tk.StringVar()
        self.replace_entry = ttk.Entry(search_group, textvariable=self.replace_var)
        self.replace_entry.pack(fill='x', pady=(0, 5))
        
        # Options
        options_frame = ttk.Frame(search_group)
        options_frame.pack(fill='x', pady=5)
        
        self.case_sensitive_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Case sensitive", variable=self.case_sensitive_var).pack(anchor='w')
        
        self.preview_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Preview changes", variable=self.preview_var).pack(anchor='w')
        
        # Method selection
        ttk.Label(search_group, text="Method:").pack(anchor='w', pady=(10, 0))
        self.method_var = tk.StringVar(value="exact")
        method_frame = ttk.Frame(search_group)
        method_frame.pack(fill='x', pady=5)
        
        ttk.Radiobutton(method_frame, text="Exact Positioning", variable=self.method_var, value="exact").pack(anchor='w')
        ttk.Radiobutton(method_frame, text="Comprehensive", variable=self.method_var, value="comprehensive").pack(anchor='w')
        ttk.Radiobutton(method_frame, text="Structure Preserving", variable=self.method_var, value="structure").pack(anchor='w')
        
        # Action buttons
        button_frame = ttk.Frame(search_group)
        button_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(button_frame, text="Search", command=self._perform_search).pack(side='left', padx=(0, 5))
        ttk.Button(button_frame, text="Replace", command=self._perform_replace).pack(side='left')
        
        # Document info section
        info_group = ttk.LabelFrame(left_frame, text="Document Information", padding=10)
        info_group.pack(fill='both', expand=True, pady=5)
        
        self.info_text = scrolledtext.ScrolledText(info_group, height=8, state='disabled')
        self.info_text.pack(fill='both', expand=True)
    
    def _create_right_panel(self):
        """Create the right results panel"""
        right_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(right_frame, weight=2)
        
        # Results section
        results_group = ttk.LabelFrame(right_frame, text="Search Results", padding=5)
        results_group.pack(fill='both', expand=True)
        
        # Create treeview for results
        columns = ('Page', 'Text', 'Font', 'Size', 'Position')
        self.results_tree = ttk.Treeview(results_group, columns=columns, show='tree headings', height=15)
        
        # Configure columns
        self.results_tree.heading('#0', text='#')
        self.results_tree.column('#0', width=50, minwidth=30)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            if col == 'Text':
                self.results_tree.column(col, width=200, minwidth=100)
            elif col in ['Font', 'Position']:
                self.results_tree.column(col, width=120, minwidth=80)
            else:
                self.results_tree.column(col, width=80, minwidth=50)
        
        # Add scrollbars
        tree_scroll_v = ttk.Scrollbar(results_group, orient='vertical', command=self.results_tree.yview)
        tree_scroll_h = ttk.Scrollbar(results_group, orient='horizontal', command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=tree_scroll_v.set, xscrollcommand=tree_scroll_h.set)
        
        # Pack treeview and scrollbars
        self.results_tree.grid(row=0, column=0, sticky='nsew')
        tree_scroll_v.grid(row=0, column=1, sticky='ns')
        tree_scroll_h.grid(row=1, column=0, sticky='ew')
        
        results_group.rowconfigure(0, weight=1)
        results_group.columnconfigure(0, weight=1)
        
        # Log section
        log_group = ttk.LabelFrame(right_frame, text="Activity Log", padding=5)
        log_group.pack(fill='x', pady=(5, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_group, height=8, state='disabled')
        self.log_text.pack(fill='both', expand=True)
    
    def _create_statusbar(self):
        """Create the status bar"""
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief='sunken', anchor='w')
        self.status_bar.grid(row=2, column=0, sticky='ew')
    
    def _log_message(self, message: str):
        """Add message to activity log"""
        self.log_text.config(state='normal')
        self.log_text.insert('end', f"{message}\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')
        self.root.update_idletasks()
    
    def _open_file(self):
        """Open a PDF file"""
        file_path = filedialog.askopenfilename(
            title="Open PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        def load_file():
            try:
                self.status_var.set("Loading PDF...")
                self._log_message(f"Loading: {Path(file_path).name}")
                
                # Close previous document
                if self.pdf_editor:
                    self.pdf_editor.close()
                
                # Load new document
                self.pdf_editor = PDFEditor()
                if self.pdf_editor.load(file_path):
                    self.current_file = file_path
                    
                    # Update UI on main thread
                    self.root.after(0, self._update_file_info)
                    self._log_message("✅ PDF loaded successfully!")
                else:
                    self._log_message("❌ Failed to load PDF")
                    self.status_var.set("Error loading PDF")
                    
            except Exception as e:
                self._log_message(f"❌ Error: {str(e)}")
                self.status_var.set("Error")
        
        # Run in background thread
        threading.Thread(target=load_file, daemon=True).start()
    
    def _update_file_info(self):
        """Update file information display"""
        if not self.pdf_editor:
            return
        
        info = self.pdf_editor.get_document_info()
        file_name = Path(self.current_file).name if self.current_file else "Unknown"
        
        # Update toolbar label
        self.file_info_label.config(text=f"📄 {file_name}")
        
        # Update info panel
        self.info_text.config(state='normal')
        self.info_text.delete('1.0', 'end')
        self.info_text.insert('end', f"File: {file_name}\n")
        self.info_text.insert('end', f"Pages: {info['page_count']}\n")
        self.info_text.insert('end', f"Text instances: {info['text_instances']}\n")
        self.info_text.insert('end', f"File size: {info['file_size']:,} bytes\n\n")
        
        if info.get('metadata'):
            self.info_text.insert('end', "Metadata:\n")
            for key, value in info['metadata'].items():
                if value:
                    self.info_text.insert('end', f"  {key}: {str(value)[:50]}\n")
        
        self.info_text.config(state='disabled')
        self.status_var.set("PDF loaded")
    
    def _perform_search(self):
        """Perform text search"""
        if not self.pdf_editor:
            messagebox.showwarning("Warning", "No PDF file loaded")
            return
        
        search_text = self.search_var.get().strip()
        if not search_text:
            messagebox.showwarning("Warning", "Enter text to search for")
            return
        
        def search_task():
            try:
                self.status_var.set("Searching...")
                self._log_message(f"🔍 Searching for: '{search_text}'")
                
                results = self.pdf_editor.search_text(search_text, self.case_sensitive_var.get())
                self.search_results = results
                
                # Update results on main thread
                self.root.after(0, lambda: self._update_search_results(results))
                
            except Exception as e:
                self._log_message(f"❌ Search error: {str(e)}")
                self.status_var.set("Search error")
        
        threading.Thread(target=search_task, daemon=True).start()
    
    def _update_search_results(self, results: List[TextInstance]):
        """Update search results display"""
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Add new results
        for i, instance in enumerate(results, 1):
            text_preview = instance.text[:50] + "..." if len(instance.text) > 50 else instance.text
            self.results_tree.insert('', 'end', text=str(i), values=(
                str(instance.page_num + 1),
                text_preview,
                instance.font,
                f"{instance.fontsize:.1f}",
                f"({instance.rect.x0:.1f}, {instance.rect.y0:.1f})"
            ))
        
        self._log_message(f"✅ Found {len(results)} instances")
        self.status_var.set(f"Found {len(results)} results")
    
    def _perform_replace(self):
        """Perform text replacement"""
        if not self.pdf_editor:
            messagebox.showwarning("Warning", "No PDF file loaded")
            return
        
        search_text = self.search_var.get().strip()
        replace_text = self.replace_var.get()
        
        if not search_text:
            messagebox.showwarning("Warning", "Enter text to search for")
            return
        
        # Preview if requested
        if self.preview_var.get():
            preview_results = self.pdf_editor.search_text(search_text, self.case_sensitive_var.get())
            if not preview_results:
                messagebox.showinfo("Info", "No instances found to replace")
                return
            
            if not messagebox.askyesno("Confirm Replace", 
                                     f"Replace {len(preview_results)} instances of '{search_text}' with '{replace_text}'?"):
                return
        
        def replace_task():
            try:
                self.status_var.set("Replacing text...")
                method = self.method_var.get()
                
                self._log_message(f"✏️ Replacing '{search_text}' → '{replace_text}' using {method} method")
                
                if method == "exact":
                    count = self.pdf_editor.replace_text_exact(search_text, replace_text, self.case_sensitive_var.get())
                elif method == "comprehensive":
                    count = self.pdf_editor.replace_text_comprehensive(search_text, replace_text)
                elif method == "structure":
                    count = self.pdf_editor.replace_text_structure_preserving(search_text, replace_text)
                else:
                    count = 0
                
                self._log_message(f"✅ Replaced {count} instances")
                self.status_var.set(f"Replaced {count} instances")
                
                # Refresh search results if any
                if self.search_results:
                    self.root.after(0, self._perform_search)
                
            except Exception as e:
                self._log_message(f"❌ Replace error: {str(e)}")
                self.status_var.set("Replace error")
        
        threading.Thread(target=replace_task, daemon=True).start()
    
    def _save_file(self):
        """Save the edited PDF"""
        if not self.pdf_editor:
            messagebox.showwarning("Warning", "No PDF file loaded")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        def save_task():
            try:
                self.status_var.set("Saving PDF...")
                self._log_message(f"💾 Saving to: {Path(file_path).name}")
                
                if self.pdf_editor.save(file_path):
                    self._log_message("✅ Saved successfully!")
                    self.status_var.set("Saved")
                else:
                    self._log_message("❌ Failed to save file")
                    self.status_var.set("Save error")
                    
            except Exception as e:
                self._log_message(f"❌ Save error: {str(e)}")
                self.status_var.set("Save error")
        
        threading.Thread(target=save_task, daemon=True).start()
    
    def _reload_file(self):
        """Reload the current file"""
        if not self.current_file:
            messagebox.showinfo("Info", "No file to reload")
            return
        
        self._log_message(f"🔄 Reloading: {Path(self.current_file).name}")
        
        if self.pdf_editor:
            self.pdf_editor.close()
        
        self.pdf_editor = PDFEditor()
        if self.pdf_editor.load(self.current_file):
            self._update_file_info()
            self._log_message("✅ Reloaded successfully!")
        else:
            self._log_message("❌ Failed to reload file")
    
    def _search_dialog(self):
        """Open search dialog"""
        self.search_entry.focus()
    
    def _replace_dialog(self):
        """Open replace dialog"""
        self.search_entry.focus()
    
    def _batch_replace_dialog(self):
        """Open batch replace dialog"""
        messagebox.showinfo("Batch Replace", "Use CLI for batch operations:\npython cli.py batch input.pdf replacements.json")
    
    def _show_document_info(self):
        """Show detailed document information"""
        if not self.pdf_editor:
            messagebox.showwarning("Warning", "No PDF file loaded")
            return
        
        info = self.pdf_editor.get_document_info()
        
        info_text = f"""Document Information:

File: {Path(self.current_file).name if self.current_file else 'Unknown'}
Pages: {info['page_count']}
Text instances: {info['text_instances']}
File size: {info['file_size']:,} bytes
"""
        
        if info.get('metadata'):
            info_text += "\nMetadata:\n"
            for key, value in info['metadata'].items():
                if value:
                    info_text += f"  {key}: {str(value)}\n"
        
        messagebox.showinfo("Document Information", info_text)
    
    def _clear_results(self):
        """Clear search results"""
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.search_results.clear()
        self._log_message("🗑️ Results cleared")
    
    def _show_about(self):
        """Show about dialog"""
        about_text = """Advanced PDF Editor v1.0

A robust PDF editing application that preserves document structure while modifying text content.

Features:
• Text editing with structure preservation
• Multiple editing methods (Exact, Comprehensive, Structure)
• Visual preview functionality
• Batch processing capabilities

Built with PyMuPDF for reliable PDF manipulation.
"""
        messagebox.showinfo("About PDF Editor", about_text)
    
    def run(self):
        """Start the GUI application"""
        self._log_message("🚀 Advanced PDF Editor ready!")
        self._log_message("📁 Open a PDF file to start editing")
        self.root.mainloop()


def main():
    """Run the GUI application"""
    app = PDFEditorGUI()
    app.run()


if __name__ == "__main__":
    main()
