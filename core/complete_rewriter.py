#!/usr/bin/env python3
"""
Complete PDF Text Rewriter - Versão Final
Remove completamente o texto original e reescreve de forma homogênea
"""

import fitz
import re
from typing import List, Tuple, Optional


class CompletePDFRewriter:
    """Reescritor completo de PDF com remoção total do texto original"""
    
    def __init__(self):
        self.document: Optional[fitz.Document] = None
        self.file_path: Optional[str] = None
    
    def load(self, file_path: str) -> bool:
        """Carrega um documento PDF"""
        try:
            self.file_path = file_path
            self.document = fitz.open(file_path)
            return True
        except Exception as e:
            print(f"Erro ao carregar PDF: {e}")
            return False
    
    def find_main_text_area(self) -> Optional[fitz.Rect]:
        """Encontra a área do texto principal para remoção completa"""
        if not self.document:
            return None
        
        page = self.document[0]
        text_dict = page.get_text("dict")
        
        # Encontrar limites do parágrafo principal
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = 0, 0
        found_main_text = False
        
        for block in text_dict["blocks"]:
            if "lines" in block:
                block_text = ""
                for line in block["lines"]:
                    for span in line["spans"]:
                        block_text += span["text"] + " "
                
                # Se contém o texto principal
                if "Atesto para os devidos fins" in block_text:
                    found_main_text = True
                    for line in block["lines"]:
                        for span in line["spans"]:
                            bbox = span["bbox"]
                            min_x = min(min_x, bbox[0])
                            min_y = min(min_y, bbox[1])
                            max_x = max(max_x, bbox[2])
                            max_y = max(max_y, bbox[3])
        
        if found_main_text:
            # Expandir área para garantir remoção completa
            return fitz.Rect(
                min_x - 10,
                min_y - 10,
                max_x + 10,
                max_y + 20
            )
        
        return None
    
    def extract_original_text(self) -> str:
        """Extrai o texto original do parágrafo principal"""
        if not self.document:
            return ""
        
        page = self.document[0]
        text_dict = page.get_text("dict")
        
        for block in text_dict["blocks"]:
            if "lines" in block:
                full_text = ""
                for line in block["lines"]:
                    for span in line["spans"]:
                        full_text += span["text"] + " "
                
                if "Atesto para os devidos fins" in full_text:
                    return full_text.strip()
        
        return ""
    
    def rewrite_complete_homogeneous(self, replacements: dict, 
                                   font_name: str = "helv", 
                                   font_size: float = 12.0,
                                   text_color: Tuple[float, float, float] = (0, 0, 0)) -> bool:
        """Reescreve completamente o texto de forma homogênea"""
        if not self.document:
            return False
        
        # Extrair texto original
        original_text = self.extract_original_text()
        if not original_text:
            print("Texto original não encontrado")
            return False
        
        print(f"Texto original: {original_text[:100]}...")
        
        # Aplicar substituições
        updated_text = original_text
        for old_text, new_text in replacements.items():
            updated_text = updated_text.replace(old_text, new_text)
            print(f"Substituindo: '{old_text}' → '{new_text}'")
        
        print(f"Texto atualizado: {updated_text[:100]}...")
        
        # Encontrar área do texto
        text_area = self.find_main_text_area()
        if not text_area:
            print("Área do texto não encontrada")
            return False
        
        page = self.document[0]
        
        # REMOVER COMPLETAMENTE o texto original
        print(f"Removendo área: {text_area}")
        page.draw_rect(text_area, color=(1, 1, 1), fill=(1, 1, 1))
        
        # Calcular posição inicial para o novo texto
        start_x = text_area.x0 + 5
        start_y = text_area.y0 + font_size + 5
        
        # Inserir novo texto com quebra de linha
        try:
            self._insert_formatted_text(
                page, 
                updated_text, 
                start_x, 
                start_y, 
                font_name, 
                font_size, 
                text_color,
                text_area.width - 10  # Largura disponível
            )
            print("Texto inserido com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao inserir texto: {e}")
            return False
    
    def _insert_formatted_text(self, page, text: str, start_x: float, start_y: float,
                             font_name: str, font_size: float, 
                             color: Tuple[float, float, float], max_width: float):
        """Insere texto formatado com quebra de linha"""
        
        # Dividir texto em palavras
        words = text.split()
        
        # Estimar caracteres por linha
        char_width = font_size * 0.55  # Estimativa para Helvetica
        chars_per_line = int(max_width / char_width)
        
        # Criar linhas
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_with_space = word + " "
            if current_length + len(word_with_space) <= chars_per_line:
                current_line.append(word)
                current_length += len(word_with_space)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word) + 1
        
        # Adicionar última linha
        if current_line:
            lines.append(" ".join(current_line))
        
        # Inserir cada linha
        line_spacing = font_size * 1.3
        current_y = start_y
        
        for i, line in enumerate(lines):
            print(f"Inserindo linha {i+1}: {line[:50]}...")
            try:
                page.insert_text(
                    fitz.Point(start_x, current_y),
                    line,
                    fontname=font_name,
                    fontsize=font_size,
                    color=color
                )
                current_y += line_spacing
            except Exception as e:
                print(f"Erro na linha {i+1}: {e}")
                # Continuar com as outras linhas
                current_y += line_spacing
    
    def save(self, output_path: str) -> bool:
        """Salva o documento modificado"""
        if not self.document:
            return False
        
        try:
            self.document.save(output_path)
            print(f"Documento salvo: {output_path}")
            return True
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            return False
    
    def close(self):
        """Fecha o documento"""
        if self.document:
            self.document.close()
            self.document = None


def main():
    """Executa a reescrita completa"""
    rewriter = CompletePDFRewriter()
    
    # Definir todas as substituições
    replacements = {
        "Marcelo de Freitas Ferreira": "Fernando Augusto Vargas Rodrigues Paes",
        "46 anos": "36 anos", 
        "agosto de 1979": "maio de 1989"
    }
    
    input_file = "pdfs/Fernando_Augusto_Vargas_Rodrigues_Paes.pdf"
    output_file = "pdfs/Fernando_Augusto_Vargas_Rodrigues_Paes_complete.pdf"
    
    print("=== REESCRITA COMPLETA E HOMOGÊNEA ===")
    print(f"Arquivo de entrada: {input_file}")
    print(f"Arquivo de saída: {output_file}")
    print("Substituições:")
    for old, new in replacements.items():
        print(f"  '{old}' → '{new}'")
    print()
    
    if rewriter.load(input_file):
        print("✅ PDF carregado com sucesso!")
        
        if rewriter.rewrite_complete_homogeneous(
            replacements, 
            font_name="helv",  # Helvetica
            font_size=12.0,
            text_color=(0, 0, 0)  # Preto
        ):
            print("✅ Texto reescrito de forma homogênea!")
            
            if rewriter.save(output_file):
                print("✅ Arquivo salvo com sucesso!")
                print(f"\n🎉 CONCLUÍDO! Verifique o arquivo: {output_file}")
            else:
                print("❌ Erro ao salvar arquivo")
        else:
            print("❌ Erro ao reescrever texto")
        
        rewriter.close()
    else:
        print("❌ Erro ao carregar PDF")


if __name__ == "__main__":
    main()
