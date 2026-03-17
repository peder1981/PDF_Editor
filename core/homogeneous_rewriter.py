#!/usr/bin/env python3
"""
Homogeneous PDF Text Rewriter
Reescreve texto completo de forma homogênea com fonte consistente
"""

import fitz
import re
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TextBlock:
    """Representa um bloco de texto completo"""
    original_text: str
    new_text: str
    rect: fitz.Rect
    font: str
    fontsize: float
    color: Tuple[float, float, float]
    page_num: int


class HomogeneousRewriter:
    """Reescritor homogêneo de texto em PDFs"""
    
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
    
    def extract_main_paragraph(self) -> Optional[TextBlock]:
        """Extrai o parágrafo principal do atestado"""
        if not self.document:
            return None
        
        page = self.document[0]  # Primeira página
        text_dict = page.get_text("dict")
        
        # Procurar pelo parágrafo que contém "Atesto para os devidos fins"
        for block in text_dict["blocks"]:
            if "lines" in block:
                full_text = ""
                first_span = None
                last_span = None
                
                # Concatenar todo o texto do bloco
                for line in block["lines"]:
                    for span in line["spans"]:
                        if first_span is None:
                            first_span = span
                        last_span = span
                        full_text += span["text"] + " "
                
                # Verificar se é o parágrafo principal
                if "Atesto para os devidos fins" in full_text:
                    # Calcular retângulo que engloba todo o parágrafo
                    if first_span and last_span:
                        rect = fitz.Rect(
                            first_span["bbox"][0],  # x0
                            first_span["bbox"][1],  # y0
                            last_span["bbox"][2],   # x1
                            last_span["bbox"][3]    # y1
                        )
                        
                        return TextBlock(
                            original_text=full_text.strip(),
                            new_text="",  # Será preenchido depois
                            rect=rect,
                            font=first_span["font"],
                            fontsize=first_span["size"],
                            color=first_span["color"],
                            page_num=0
                        )
        
        return None
    
    def create_updated_text(self, original_text: str, replacements: dict) -> str:
        """Cria texto atualizado com todas as substituições"""
        updated_text = original_text
        
        # Aplicar todas as substituições
        for old_text, new_text in replacements.items():
            updated_text = updated_text.replace(old_text, new_text)
        
        return updated_text
    
    def rewrite_paragraph_homogeneous(self, replacements: dict, 
                                    target_font: str = "Calibri", 
                                    target_fontsize: float = 12.0) -> bool:
        """Reescreve o parágrafo principal de forma homogênea"""
        if not self.document:
            return False
        
        # Extrair parágrafo principal
        text_block = self.extract_main_paragraph()
        if not text_block:
            print("Não foi possível encontrar o parágrafo principal")
            return False
        
        print(f"Texto original encontrado: {text_block.original_text[:100]}...")
        
        # Criar texto atualizado
        updated_text = self.create_updated_text(text_block.original_text, replacements)
        print(f"Texto atualizado: {updated_text[:100]}...")
        
        page = self.document[0]
        
        # Remover texto original cobrindo com retângulo branco
        expanded_rect = fitz.Rect(
            text_block.rect.x0 - 5,
            text_block.rect.y0 - 5,
            text_block.rect.x1 + 5,
            text_block.rect.y1 + 15
        )
        page.draw_rect(expanded_rect, color=(1, 1, 1), fill=(1, 1, 1))
        
        # Inserir novo texto de forma homogênea
        try:
            # Calcular posição inicial
            start_point = fitz.Point(text_block.rect.x0, text_block.rect.y0 + target_fontsize)
            
            # Inserir texto com quebras de linha apropriadas
            self._insert_text_with_wrapping(
                page, 
                updated_text, 
                start_point, 
                target_font, 
                target_fontsize,
                text_block.rect.width,
                text_block.color
            )
            
            return True
            
        except Exception as e:
            print(f"Erro ao inserir texto: {e}")
            # Fallback: inserir texto simples
            try:
                page.insert_text(
                    text_block.rect.tl,
                    updated_text,
                    fontname="helv",
                    fontsize=target_fontsize,
                    color=text_block.color
                )
                return True
            except Exception as e2:
                print(f"Erro no fallback: {e2}")
                return False
    
    def _insert_text_with_wrapping(self, page, text: str, start_point: fitz.Point,
                                 font: str, fontsize: float, max_width: float,
                                 color: Tuple[float, float, float]):
        """Insere texto com quebra de linha automática"""
        
        words = text.split()
        lines = []
        current_line = []
        
        # Estimar largura de caractere (aproximação)
        char_width = fontsize * 0.6  # Aproximação para Calibri
        max_chars_per_line = int(max_width / char_width)
        
        current_length = 0
        for word in words:
            word_length = len(word) + 1  # +1 para o espaço
            
            if current_length + word_length <= max_chars_per_line:
                current_line.append(word)
                current_length += word_length
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
        
        # Adicionar última linha
        if current_line:
            lines.append(" ".join(current_line))
        
        # Inserir cada linha
        line_height = fontsize * 1.2  # Espaçamento entre linhas
        current_y = start_point.y
        
        for line in lines:
            try:
                page.insert_text(
                    fitz.Point(start_point.x, current_y),
                    line,
                    fontname=font if font != "Calibri" else "helv",  # Fallback para helv
                    fontsize=fontsize,
                    color=color
                )
                current_y += line_height
            except Exception as e:
                print(f"Erro ao inserir linha '{line[:30]}...': {e}")
                # Tentar com fonte padrão
                page.insert_text(
                    fitz.Point(start_point.x, current_y),
                    line,
                    fontname="helv",
                    fontsize=fontsize,
                    color=color
                )
                current_y += line_height
    
    def save(self, output_path: str) -> bool:
        """Salva o documento modificado"""
        if not self.document:
            return False
        
        try:
            self.document.save(output_path)
            return True
        except Exception as e:
            print(f"Erro ao salvar PDF: {e}")
            return False
    
    def close(self):
        """Fecha o documento"""
        if self.document:
            self.document.close()
            self.document = None


def main():
    """Função principal para teste"""
    rewriter = HomogeneousRewriter()
    
    # Definir substituições
    replacements = {
        "Marcelo de Freitas Ferreira": "Fernando Augusto Vargas Rodrigues Paes",
        "46 anos": "36 anos",
        "agosto de 1979": "maio de 1989"
    }
    
    input_file = "pdfs/Fernando_Augusto_Vargas_Rodrigues_Paes.pdf"
    output_file = "pdfs/Fernando_Augusto_Vargas_Rodrigues_Paes_homogeneous.pdf"
    
    if rewriter.load(input_file):
        print("PDF carregado com sucesso!")
        
        if rewriter.rewrite_paragraph_homogeneous(replacements):
            print("Texto reescrito com sucesso!")
            
            if rewriter.save(output_file):
                print(f"Arquivo salvo: {output_file}")
            else:
                print("Erro ao salvar arquivo")
        else:
            print("Erro ao reescrever texto")
        
        rewriter.close()
    else:
        print("Erro ao carregar PDF")


if __name__ == "__main__":
    main()
