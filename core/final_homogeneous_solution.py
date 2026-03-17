#!/usr/bin/env python3
"""
Solução Final Homogênea - Remove completamente o texto original e reescreve
"""

import fitz
from typing import Tuple, Optional


class FinalHomogeneousRewriter:
    """Solução final para reescrita homogênea completa"""
    
    def __init__(self):
        self.document: Optional[fitz.Document] = None
    
    def load(self, file_path: str) -> bool:
        """Carrega documento PDF"""
        try:
            self.document = fitz.open(file_path)
            return True
        except Exception as e:
            print(f"Erro ao carregar: {e}")
            return False
    
    def apply_complete_homogeneous_rewrite(self, replacements: dict) -> bool:
        """Aplica reescrita homogênea completa usando redação"""
        if not self.document:
            return False
        
        page = self.document[0]
        
        # Texto completo original
        original_text = ("Atesto para os devidos fins que, Marcelo de Freitas Ferreira, "
                        "nascido em 19 de agosto de 1979, 46 anos de idade, encontra-se "
                        "apto a praticar atividades físicas sem nenhuma restrição.")
        
        # Aplicar todas as substituições
        new_text = original_text
        for old, new in replacements.items():
            new_text = new_text.replace(old, new)
        
        print(f"Texto original: {original_text}")
        print(f"Texto novo: {new_text}")
        
        # Encontrar todas as instâncias do texto original para redação
        search_results = page.search_for("Atesto para os devidos fins")
        
        if not search_results:
            print("Texto não encontrado para redação")
            return False
        
        # Aplicar redação em todas as instâncias encontradas
        for rect in search_results:
            print(f"Aplicando redação em: {rect}")
            
            # Expandir retângulo para cobrir todo o parágrafo
            expanded_rect = fitz.Rect(
                rect.x0 - 10,
                rect.y0 - 5,
                rect.x0 + 400,  # Largura suficiente para todo o parágrafo
                rect.y0 + 50    # Altura suficiente para múltiplas linhas
            )
            
            # Criar anotação de redação com o novo texto
            redact_annot = page.add_redact_annot(
                expanded_rect,
                text=new_text,
                fontname="helv",
                fontsize=12,
                text_color=(0, 0, 0),
                fill=(1, 1, 1),
                align=fitz.TEXT_ALIGN_LEFT
            )
            redact_annot.update()
        
        # Aplicar todas as redações
        page.apply_redactions()
        print("Redações aplicadas com sucesso!")
        
        return True
    
    def save(self, output_path: str) -> bool:
        """Salva documento"""
        if not self.document:
            return False
        try:
            self.document.save(output_path)
            return True
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            return False
    
    def close(self):
        """Fecha documento"""
        if self.document:
            self.document.close()


def main():
    """Executa solução final"""
    rewriter = FinalHomogeneousRewriter()
    
    # Todas as substituições necessárias
    replacements = {
        "Marcelo de Freitas Ferreira": "Fernando Augusto Vargas Rodrigues Paes",
        "46 anos": "36 anos",
        "agosto de 1979": "maio de 1989"
    }
    
    input_file = "pdfs/Fernando_Augusto_Vargas_Rodrigues_Paes.pdf"
    output_file = "pdfs/Fernando_Augusto_Vargas_Rodrigues_Paes_FINAL.pdf"
    
    print("=== SOLUÇÃO FINAL HOMOGÊNEA ===")
    print(f"Entrada: {input_file}")
    print(f"Saída: {output_file}")
    print("\nSubstituições:")
    for old, new in replacements.items():
        print(f"  • '{old}' → '{new}'")
    print()
    
    if rewriter.load(input_file):
        print("✅ PDF carregado")
        
        if rewriter.apply_complete_homogeneous_rewrite(replacements):
            print("✅ Reescrita homogênea aplicada")
            
            if rewriter.save(output_file):
                print("✅ Arquivo salvo")
                print(f"\n🎉 CONCLUÍDO! Arquivo final: {output_file}")
                print("📝 Todo o texto foi reescrito de forma homogênea com fonte Helvetica 12pt")
                print("🔧 Todas as três alterações foram aplicadas simultaneamente")
            else:
                print("❌ Erro ao salvar")
        else:
            print("❌ Erro na reescrita")
        
        rewriter.close()
    else:
        print("❌ Erro ao carregar PDF")


if __name__ == "__main__":
    main()
